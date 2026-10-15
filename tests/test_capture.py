import struct
import tempfile
import unittest
from pathlib import Path
from matribox_lab.capture import analyze


def nib(data):
    return bytes(v for b in data for v in (b >> 4, b & 15))


def block(kind, body):
    body += b"\0" * (-len(body) % 4)
    size = len(body) + 12
    return struct.pack("<II", kind, size) + body + struct.pack("<I", size)


def capture(negative=False, finish=True):
    ack = bytes.fromhex("f07e48037ff7")
    size = 1
    encoded = nib(b"x" + b"\xff"*179)
    data = bytes.fromhex("f07e480400") + encoded + nib(bytes([sum(encoded) % 256])) + b"\xf7"
    rows = [(True, bytes.fromhex("f07e4801514d452d323030f7")),
            (False, bytes.fromhex("f07e487f10f7")),
            (True, bytes.fromhex("f07e487f10f7")),
            (False, bytes.fromhex("f07e4802") + nib(struct.pack(">II", size, 1)) + b"\xf7"),
            (True, ack), (False, data),
            (True, bytes.fromhex("f07e48037ef7") if negative else ack),
            (False, bytes.fromhex("f07e48057bf7")), (True, ack),
            (False, bytes.fromhex("f07e4809f7"))]
    if finish:
        rows.append((True, ack))
    result = block(0x0A0D0D0A, struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1))
    result += block(1, struct.pack("<HHI", 249, 0, 65535))
    for i, (incoming, msg) in enumerate(rows):
        payload = bytearray()
        for at in range(0, len(msg), 3):
            chunk = msg[at:at+3]
            cin = 4 if at+3 < len(msg) else {1:5, 2:6, 3:7}[len(chunk)]
            payload.extend(bytes([cin]) + chunk.ljust(3, b"\0"))
        raw = struct.pack("<HQIHBHHBBI", 27, 0, 0, 0, 0, 1, 2,
                          0x83 if incoming else 3, 3, len(payload)) + payload
        result += block(6, struct.pack("<5I", 0, 0, i, len(raw), len(raw)) + raw)
    return result


class CaptureTests(unittest.TestCase):
    def check(self, data, expected=b"x"):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"test.pcapng"
            path.write_bytes(data)
            return analyze(path, expected)

    def test_complete_session_and_padding(self):
        result = self.check(capture())
        self.assertTrue(result["passed"])
        self.assertEqual(result["data_packets"], 1)
        self.assertTrue(result["library_only"])
        self.assertFalse(result["flash_readback"])

    def test_rejects_wrong_library(self):
        with self.assertRaises(ValueError):
            self.check(capture(), b"y")

    def test_rejects_negative_ack_and_missing_completion(self):
        for data in (capture(negative=True), capture(finish=False)):
            with self.assertRaises(ValueError):
                self.check(data)

    def test_rejects_truncated_pcapng(self):
        with self.assertRaises(ValueError):
            self.check(capture()[:-4])


if __name__ == "__main__":
    unittest.main()
