"""FRMW and effect catalog reader, based on locally verified Matribox II Pro images."""
from __future__ import annotations
import hashlib
import struct
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def checked(data: bytes, start: int, size: int) -> bytes:
    if start < 0 or size < 0 or start + size > len(data):
        raise ValueError("Range exceeds input")
    return data[start:start + size]


def u32(data: bytes, offset: int) -> int:
    return struct.unpack("<I", checked(data, offset, 4))[0]


def catalog(data: bytes) -> list[dict]:
    groups = u32(data, 20)
    if not 0 < groups <= 16 or u32(data, 4) != 24 + 4 * groups:
        raise ValueError("Unsupported catalog header")
    if u32(data, 12) != len(data):
        raise ValueError("Catalog total length mismatch")
    table_end = u32(data, 8)
    if not 24 + 4 * groups <= table_end <= len(data):
        raise ValueError("Invalid catalog table length")
    result = []
    for group in range(groups):
        table = u32(data, 24 + group * 4)
        count = u32(data, table)
        if table + 4 + count * 4 > table_end:
            raise ValueError("Group exceeds catalog table")
        ids = set()
        for index in range(count):
            offset = u32(data, table + 4 + index * 4)
            size, elf_offset, ident = struct.unpack("<III", checked(data, offset, 12))
            if offset < table_end or not 24 <= elf_offset < size or ident in ids:
                raise ValueError("Invalid or duplicate record")
            ids.add(ident)
            record = checked(data, offset, size)
            elf = record[elf_offset:]
            if elf[:4] != b"\x7fELF":
                raise ValueError("Missing ELF signature")
            count_params = record[16]
            pool = 24 + count_params * 24
            if pool > elf_offset:
                raise ValueError("Parameter table exceeds metadata")
            def text(relative):
                start = pool + relative
                if start >= elf_offset:
                    raise ValueError("String exceeds metadata")
                end = record.find(b"\0", start, elf_offset)
                if end < 0:
                    raise ValueError("Unterminated metadata string")
                return record[start:end].decode("utf-8", errors="replace")
            model, category = struct.unpack_from("<HH", record, 20)
            params = []
            for p in range(count_params):
                at = 24 + p * 24
                name = struct.unpack_from("<H", record, at + 2)[0]
                low, high, step, default = struct.unpack_from("<4f", record, at + 4)
                params.append(dict(name=text(name), minimum=low, maximum=high,
                                   step=step, default=default,
                                   flags=record[at + 20:at + 24].hex()))
            result.append(dict(group=group, index=index, id=f"0x{ident:08x}",
                               name=text(model), category=text(category),
                               record_offset=offset, record_bytes=size,
                               elf_offset=elf_offset, elf_bytes=len(elf),
                               record_sha256=sha256(record), elf_sha256=sha256(elf),
                               parameters=params))
    return result


class Firmware:
    def __init__(self, data: bytes):
        if checked(data, 0, 4) != b"FRMW":
            raise ValueError("Not an FRMW firmware")
        self.data = data
        self.blocks = []
        for offset in range(0x30, 0x50, 8):
            relative, size = struct.unpack("<II", checked(data, offset, 8))
            start = relative + 0x30
            payload = checked(data, start, size)
            self.blocks.append(dict(start=start, bytes=size, sha256=sha256(payload)))
        self.library = checked(data, self.blocks[1]["start"], self.blocks[1]["bytes"])
        self.records = catalog(self.library)

    @classmethod
    def read(cls, path: str | Path) -> Firmware:
        return cls(Path(path).read_bytes())

    def summary(self) -> dict:
        return dict(bytes=len(self.data), sha256=sha256(self.data), blocks=self.blocks,
                    module_count=len(self.records),
                    group_counts=[sum(r["group"] == g for r in self.records)
                                  for g in range(u32(self.library, 20))],
                    records=self.records)


def compare(old: Firmware, new: Firmware) -> dict:
    a = {(r["group"], r["id"]): r for r in old.records}
    b = {(r["group"], r["id"]): r for r in new.records}
    common = []
    for key in a.keys() & b.keys():
        x, y = a[key], b[key]
        common.append(dict(group=key[0], id=key[1], name=y["name"],
                           old_index=x["index"], new_index=y["index"],
                           record_identical=x["record_sha256"] == y["record_sha256"],
                           elf_identical=x["elf_sha256"] == y["elf_sha256"],
                           parameters_identical=x["parameters"] == y["parameters"]))
    return dict(old_count=len(a), new_count=len(b),
                library_growth=len(new.library) - len(old.library),
                added=[r for k, r in b.items() if k not in a],
                removed=[r for k, r in a.items() if k not in b],
                common=sorted(common, key=lambda r: (r["group"], r["old_index"])))


def append_record(firmware: Firmware, record: bytes, group: int = 3) -> bytes:
    """Builds a raw candidate library, never a flash command or complete firmware."""
    size, elf_offset, ident = struct.unpack("<III", checked(record, 0, 12))
    if size != len(record) or not 24 <= elf_offset < size or record[elf_offset:elf_offset+4] != b"\x7fELF":
        raise ValueError("Invalid effect record")
    groups = u32(firmware.library, 20)
    if not 0 <= group < groups:
        raise ValueError("Unknown group")
    if any(r["group"] == group and int(r["id"], 16) == ident for r in firmware.records):
        raise ValueError("Effect ID already exists in group")
    result = bytearray(firmware.library[:24 + 4 * groups])
    slots = []
    for g in range(groups):
        records = [checked(firmware.library, r["record_offset"], r["record_bytes"])
                   for r in firmware.records if r["group"] == g]
        if g == group:
            records.append(record)
        struct.pack_into("<I", result, 24 + g * 4, len(result))
        result.extend(struct.pack("<I", len(records)))
        for data in records:
            slots.append((len(result), data))
            result.extend(b"\0" * 4)
    struct.pack_into("<I", result, 8, len(result))
    for slot, data in slots:
        if len(result) % 4:
            raise ValueError("Record alignment is not supported")
        struct.pack_into("<I", result, slot, len(result))
        result.extend(data)
    struct.pack_into("<I", result, 12, len(result))
    catalog(bytes(result))
    return bytes(result)
