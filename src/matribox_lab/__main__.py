"""Read-only firmware/capture CLI. No MIDI writer is shipped in this release."""
import argparse
import json
from pathlib import Path
from .firmware import Firmware, compare


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    commands = ap.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("firmware")
    comparison = commands.add_parser("compare")
    comparison.add_argument("old")
    comparison.add_argument("new")
    capture = commands.add_parser("capture")
    capture.add_argument("pcapng")
    capture.add_argument("--expected-library", required=True)
    args = ap.parse_args()
    try:
        if args.command == "inspect":
            result = Firmware.read(args.firmware).summary()
        elif args.command == "compare":
            result = compare(Firmware.read(args.old), Firmware.read(args.new))
        else:
            from .capture import analyze
            result = analyze(Path(args.pcapng), Path(args.expected_library).read_bytes())
    except (OSError, ValueError) as exc:
        ap.exit(2, str(exc) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
