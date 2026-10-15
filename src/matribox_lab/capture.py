"""Offline USBPcap/PCAPNG verifier for a complete library session."""
import struct
from pathlib import Path
from .firmware import checked, sha256

ACK = bytes.fromhex("f07e48037ff7")


def unnibble(data):
    if len(data) % 2 or any(v > 15 for v in data):
        raise ValueError("Invalid nibble encoding")
    return bytes(data[i] * 16 + data[i+1] for i in range(0, len(data), 2))


def messages(path):
    data = Path(path).read_bytes()
    offset, packet, interfaces, pending, output = 0, 0, [], {}, []
    while offset < len(data):
        kind, size = struct.unpack("<II", checked(data, offset, 8))
        if size < 12 or size % 4:
            raise ValueError("Invalid PCAPNG block length")
        block = checked(data, offset, size)
        if struct.unpack_from("<I", block, size-4)[0] != size:
            raise ValueError("PCAPNG block trailer mismatch")
        body = block[8:-4]
        offset += size
        if kind == 0x0A0D0D0A:
            if body[:4] != bytes.fromhex("4d3c2b1a"):
                raise ValueError("Only little-endian PCAPNG is supported")
            if pending:
                raise ValueError("Incomplete SysEx across PCAPNG section")
            interfaces = []
        elif kind == 1:
            interfaces.append(struct.unpack("<H", checked(body, 0, 2))[0])
        elif kind == 6:
            packet += 1
            iface, _, _, cap, original = struct.unpack("<5I", checked(body, 0, 20))
            if iface >= len(interfaces) or interfaces[iface] != 249:
                raise ValueError("Expected USBPcap linktype 249")
            if cap != original:
                raise ValueError("Truncated capture packet")
            raw = checked(body, 20, cap)
            if len(raw) < 27:
                continue
            hl, _, _, _, _, bus, dev, ep, typ, length = struct.unpack_from("<HQIHBHHBBI", raw)
            if hl < 27:
                raise ValueError("Invalid USBPcap header")
            payload = checked(raw, hl, length)
            if typ != 3 or not payload:
                continue
            if len(payload) % 4:
                raise ValueError("Unaligned USB-MIDI payload")
            for pos in range(0, len(payload), 4):
                event = payload[pos:pos+4]
                cin = event[0] & 15
                if cin not in (4, 5, 6, 7):
                    continue
                key = (bus, dev, ep, event[0] >> 4)
                chunk = event[1:1+{4:3, 5:1, 6:2, 7:3}[cin]]
                if chunk[0] == 0xF0:
                    if key in pending:
                        raise ValueError("Overlapping SysEx messages")
                    pending[key] = bytearray()
                if key not in pending:
                    raise ValueError("Orphan SysEx fragment; capture may be incomplete")
                pending[key].extend(chunk)
                if cin != 4:
                    msg = bytes(pending.pop(key))
                    if msg[-1] != 0xF7:
                        raise ValueError("Unterminated SysEx")
                    output.append((bus, dev, bool(ep & 128), packet, msg))
    if pending:
        raise ValueError("Capture ended inside SysEx")
    return output, sha256(data)


def analyze(path, expected_library):
    rows, capture_hash = messages(path)
    devices = {(bus, dev) for bus, dev, incoming, _, msg in rows
               if incoming and msg.startswith(bytes.fromhex("f07e4801514d452d323030"))}
    if len(devices) != 1:
        raise ValueError("Expected one QME-200 identification; capture from before identification")
    selectors, chunks, awaiting, count, size = [], [], None, None, None
    data_acks, finish_ack, selected, failures = 0, False, None, []
    for bus, dev, incoming, packet, msg in rows:
        if (bus, dev) not in devices:
            continue
        if not incoming:
            if msg.startswith(bytes.fromhex("f07e487f")):
                selected = msg[4]
                selectors.append(selected)
            if selected != 16:
                continue
            if msg.startswith(bytes.fromhex("f07e4802")):
                if count is not None:
                    raise ValueError("Multiple library announcements")
                size, count = struct.unpack(">II", unnibble(msg[4:-1]))
                awaiting = "announcement"
            elif msg.startswith(bytes.fromhex("f07e4804")):
                index = len(chunks)
                if awaiting is not None or count is None or len(msg) != 368 or msg[4] != index % 128:
                    raise ValueError("Unexpected or missing library packet")
                if sum(msg[5:-3]) % 256 != unnibble(msg[-3:-1])[0]:
                    raise ValueError("Library packet checksum mismatch")
                chunk = unnibble(msg[5:-3])
                expected = expected_library[index*180:(index+1)*180].ljust(180, b"\xff")
                if chunk != expected:
                    raise ValueError("Captured data differs from expected library")
                chunks.append(chunk)
                awaiting = index
            elif msg == bytes.fromhex("f07e48057bf7"):
                if awaiting is not None:
                    raise ValueError("Block end before data acknowledgement")
                awaiting = "end"
            elif msg == bytes.fromhex("f07e4809f7"):
                awaiting = "finish"
        elif selected == 16:
            if msg == ACK:
                if isinstance(awaiting, int):
                    data_acks += 1
                elif awaiting == "finish":
                    finish_ack = True
                elif awaiting not in ("announcement", "end"):
                    raise ValueError("Unassigned positive acknowledgement")
                awaiting = None
            elif msg == bytes.fromhex("f07e48037ef7"):
                failures.append(packet)
    rebuilt = b"".join(chunks)
    if size != len(expected_library) or count != len(chunks) or data_acks != count:
        raise ValueError("Incomplete library session or incorrect announcement")
    if rebuilt[:size] != expected_library or any(v != 255 for v in rebuilt[size:]):
        raise ValueError("Library reconstruction mismatch")
    if failures or not finish_ack or awaiting is not None:
        raise ValueError("Session rejected or completion acknowledgement missing")
    return dict(passed=True, capture_sha256=capture_hash, library_sha256=sha256(expected_library),
                library_bytes=size, data_packets=count, data_acknowledgements=data_acks,
                selectors=selectors, library_only=selectors == [16],
                finish_acknowledged=finish_ack, negative_acknowledgements=len(failures),
                flash_readback=False, physical_access=False)
