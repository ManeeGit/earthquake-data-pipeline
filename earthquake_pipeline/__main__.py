"""Run with: python -m earthquake_pipeline offline"""

import argparse
import json
import logging
from pathlib import Path

from earthquake_pipeline.extract import capture_fixture

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Earthquake Data Pipeline — milestone 1")
    commands = parser.add_subparsers(dest="command", required=True)
    offline = commands.add_parser("offline", help="Capture a labeled synthetic fixture")
    offline.add_argument(
        "--fixture", type=Path,
        default=PROJECT_ROOT / "fixtures" / "synthetic_earthquakes.json",
    )
    offline.add_argument("--raw-dir", type=Path, default=Path("data/raw/offline"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    try:
        capture_dir = capture_fixture(args.fixture, args.raw_dir)
    except (OSError, ValueError, OverflowError) as exc:
        parser.exit(1, f"Extraction failed: {exc}\n")

    receipt = json.loads((capture_dir / "metadata.json").read_text(encoding="utf-8"))
    print("SYNTHETIC DEMO — invented events; no USGS request made")
    print(f"Captured features: {receipt['feature_count']}")
    print(f"Requested UTC start: {receipt['requested_start_utc']}")
    print(f"Requested UTC end (exclusive): {receipt['requested_end_utc']}")
    print(f"Raw JSON: {capture_dir / 'response.json'}")
    print(f"Receipt: {capture_dir / 'metadata.json'}")


if __name__ == "__main__":
    main()
