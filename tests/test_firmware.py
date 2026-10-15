import struct
import unittest
from matribox_lab.firmware import Firmware, catalog, compare, append_record
from matribox_lab.capture import unnibble


def record(ident=7, name=b"Test"):
    meta = bytearray(24)
    struct.pack_into("<I", meta, 8, ident)
    struct.pack_into("<HH", meta, 20, 0, len(name)+1)
    meta.extend(name+b"\0Drive\0")
    meta.extend(b"\xff" * (-len(meta) % 4))
    size = len(meta)+8
    struct.pack_into("<II", meta, 0, size, len(meta))
    return bytes(meta)+b"\x7fELFtest"


def image(records):
    cat = bytearray(28)
    struct.pack_into("<I", cat, 4, 28)
    struct.pack_into("<I", cat, 20, 1)
    struct.pack_into("<I", cat, 24, 28)
    cat.extend(struct.pack("<I", len(records)))
    slots = []
    for data in records:
        slots.append((len(cat), data))
        cat.extend(b"\0"*4)
    struct.pack_into("<I", cat, 8, len(cat))
    for slot, data in slots:
        struct.pack_into("<I", cat, slot, len(cat))
        cat.extend(data)
    struct.pack_into("<I", cat, 12, len(cat))
    fw = bytearray(80)
    fw[:4] = b"FRMW"
    for i, payload in enumerate([b"CODE", bytes(cat), b"DATA", b"CONF"]):
        struct.pack_into("<II", fw, 48+i*8, len(fw)-48, len(payload))
        fw.extend(payload)
    return bytes(fw)


class FirmwareTests(unittest.TestCase):
    def test_relative_base_and_catalog(self):
        fw = Firmware(image([record()]))
        self.assertEqual(fw.blocks[0]["start"], 80)
        self.assertEqual(fw.records[0]["name"], "Test")
        self.assertEqual(fw.records[0]["id"], "0x00000007")

    def test_append_preserves_original_record(self):
        fw = Firmware(image([record()]))
        result = append_record(fw, record(8, b"New"), group=0)
        rows = catalog(result)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["record_sha256"], fw.records[0]["record_sha256"])
        with self.assertRaises(ValueError):
            append_record(fw, record(), group=0)

    def test_reordered_ids_are_not_reported_as_added(self):
        a, b = record(7), record(8)
        result = compare(Firmware(image([a,b])), Firmware(image([b,a])))
        self.assertEqual(result["added"], [])
        self.assertEqual(result["removed"], [])
        self.assertTrue(all(r["record_identical"] for r in result["common"]))
        self.assertTrue(all(r["old_index"] != r["new_index"] for r in result["common"]))

    def test_rejects_truncated_blocks_and_bad_catalog_offsets(self):
        data = image([record()])
        with self.assertRaises(ValueError):
            Firmware(data[:-1])
        corrupt = bytearray(data)
        fw = Firmware(data)
        struct.pack_into("<I", corrupt, fw.blocks[1]["start"]+24, 0xFFFFFFF0)
        with self.assertRaises(ValueError):
            Firmware(corrupt)

    def test_nibble_validation(self):
        self.assertEqual(unnibble(bytes([15,0,7,15])), bytes([240,127]))
        for data in [bytes([1]), bytes([16,0])]:
            with self.assertRaises(ValueError):
                unnibble(data)


if __name__ == "__main__":
    unittest.main()
