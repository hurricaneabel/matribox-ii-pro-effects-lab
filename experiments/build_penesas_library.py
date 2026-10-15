"""Build the exact documented uncompacted candidate offline; does not upload it."""
import argparse
import json
from pathlib import Path
from matribox_lab.firmware import Firmware, append_record, catalog, sha256, checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matribox-firmware", required=True)
    parser.add_argument("--record", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    fw = Firmware.read(args.matribox_firmware)
    record = Path(args.record).read_bytes()
    if sha256(fw.data) != "d9ebcb8d368c0c81a2c104b1853ae1de57a5dc86ac3d5c2aff3623ce13dc64a7":
        raise ValueError("Only the documented Matribox V1.2.2 is supported")
    if sha256(record) != "fb03f34851f1691a5fe45988d95638265d068bdc9fad3b36a1f7b90bba43e597":
        raise ValueError("Unexpected Penesas record")
    result = append_record(fw, record, group=3)
    rows = {(r["group"], r["index"]): r for r in catalog(result)}
    for old in fw.records:
        new = rows[(old["group"], old["index"])]
        if checked(fw.library, old["record_offset"], old["record_bytes"]) != checked(result, new["record_offset"], new["record_bytes"]):
            raise ValueError("Original record changed")
    expected = "72bba28a4239737d63e6a75b6762580dc77c4890de7b0ace81949995a9f6e6ac"
    if sha256(result) != expected:
        raise ValueError("Candidate does not reproduce the documented image")
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(result)
    print(json.dumps(dict(passed=True, sha256=expected, bytes=len(result),
                         original_records_unchanged=179, catalog_entries=180,
                         compacted_records=0, physical_access=False), indent=2))


if __name__ == "__main__":
    main()
