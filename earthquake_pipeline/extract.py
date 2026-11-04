"""Milestone 1: capture a labeled synthetic fixture without changing its bytes."""

import hashlib
import json
import logging
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from time import perf_counter
from uuid import uuid4

logger = logging.getLogger(__name__)


def parse_features(raw: bytes) -> list:
    """Check the response container; event-level validation comes in milestone 2."""
    document = json.loads(raw)
    if not isinstance(document, dict) or document.get("type") != "FeatureCollection":
        raise ValueError("Expected a GeoJSON FeatureCollection")
    features = document.get("features")
    if not isinstance(features, list):
        raise ValueError("Expected 'features' to be a list (an empty list is valid)")
    return features


def capture_fixture(fixture_path: Path, raw_dir: Path) -> Path:
    """Save original bytes and a receipt. Return the new capture directory.

    This entry point accepts only labeled synthetic fixtures. The fixture's
    declared UTC day supplies the intended request window; no HTTP request or
    event filtering happens here. Invalid fixture containers fail before saving.
    """
    started = perf_counter()
    raw = fixture_path.read_bytes()
    retrieved_at = datetime.now(UTC)
    features = parse_features(raw)
    document = json.loads(raw)
    fixture_metadata = document.get("metadata")
    if not isinstance(fixture_metadata, dict) or fixture_metadata.get("synthetic") is not True:
        raise ValueError("Offline input must have metadata.synthetic set to true")
    try:
        day = date.fromisoformat(fixture_metadata["day_utc"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Fixture metadata.day_utc must be an ISO date") from exc
    start = datetime.combine(day, time.min, tzinfo=UTC)
    end = start + timedelta(days=1)

    # Keep every capture. This is separate from deduplicating database events.
    capture_id = retrieved_at.strftime("%Y%m%dT%H%M%S%fZ") + "_" + uuid4().hex[:8]
    capture_dir = raw_dir / capture_id
    capture_dir.mkdir(parents=True, exist_ok=False)
    (capture_dir / "response.json").write_bytes(raw)

    # Our receipt lives beside the source data; it is not inserted into it.
    receipt = {
        "source_mode": "synthetic_fixture",
        "source_url": fixture_path.resolve().as_uri(),
        "source_api_reference": "https://earthquake.usgs.gov/fdsnws/event/1/",
        "http_request_sent": False,
        "retrieved_at_utc": retrieved_at.isoformat(),
        "requested_start_utc": start.isoformat(),
        "requested_end_utc": end.isoformat(),
        "window_semantics": "start inclusive, end exclusive; declared fixture day",
        "feature_count": len(features),
        "byte_count": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    (capture_dir / "metadata.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    logger.info(
        "stage=extract source=synthetic_fixture rows=%d bytes=%d elapsed_seconds=%.6f",
        len(features), len(raw), perf_counter() - started,
    )
    return capture_dir
