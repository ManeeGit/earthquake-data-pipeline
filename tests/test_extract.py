"""All tests use local bytes and temporary directories; no network is needed."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from earthquake_pipeline.extract import capture_fixture, parse_features

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_earthquakes.json"


def test_parse_fixture_preserves_nested_values_and_missing_magnitude():
    features = parse_features(FIXTURE.read_bytes())
    assert [feature["id"] for feature in features] == ["synthetic-001", "synthetic-002"]
    assert features[0]["properties"]["mag"] == 2.5
    assert features[0]["geometry"]["coordinates"] == [-122.5, 38.5, 7.0]
    assert features[1]["properties"]["mag"] is None


def test_capture_preserves_bytes_and_records_provenance(tmp_path, caplog):
    before = datetime.now(UTC)
    with caplog.at_level("INFO"):
        capture_dir = capture_fixture(FIXTURE, tmp_path / "raw")
    after = datetime.now(UTC)
    saved = (capture_dir / "response.json").read_bytes()
    receipt = json.loads((capture_dir / "metadata.json").read_text())
    assert saved == FIXTURE.read_bytes()
    assert receipt["sha256"] == hashlib.sha256(saved).hexdigest()
    assert receipt["byte_count"] == len(saved)
    assert receipt["feature_count"] == 2
    assert receipt["source_mode"] == "synthetic_fixture"
    assert receipt["source_url"] == FIXTURE.resolve().as_uri()
    assert receipt["http_request_sent"] is False
    assert receipt["requested_start_utc"] == "2024-01-01T00:00:00+00:00"
    assert receipt["requested_end_utc"] == "2024-01-02T00:00:00+00:00"
    assert before <= datetime.fromisoformat(receipt["retrieved_at_utc"]) <= after
    assert "rows=2" in caplog.text
    assert "elapsed_seconds=" in caplog.text


def test_rerun_keeps_both_captures(tmp_path):
    first = capture_fixture(FIXTURE, tmp_path)
    original_receipt = (first / "metadata.json").read_bytes()
    second = capture_fixture(FIXTURE, tmp_path)
    assert first != second
    assert (first / "metadata.json").read_bytes() == original_receipt
    assert (first / "response.json").read_bytes() == (second / "response.json").read_bytes()


def test_empty_response_can_be_captured(tmp_path):
    document = json.loads(FIXTURE.read_bytes())
    document["features"] = []
    document["metadata"]["count"] = 0
    source = tmp_path / "empty.json"
    source.write_text(json.dumps(document))
    capture_dir = capture_fixture(source, tmp_path / "raw")
    receipt = json.loads((capture_dir / "metadata.json").read_text())
    assert receipt["feature_count"] == 0
    assert parse_features((capture_dir / "response.json").read_bytes()) == []


@pytest.mark.parametrize("raw", [
    b"not JSON", b"[]", b"{}",
    b'{"type": "FeatureCollection"}',
    b'{"type": "FeatureCollection", "features": null}',
    b'{"type": "FeatureCollection", "features": {}}',
])
def test_malformed_container_is_rejected(raw):
    with pytest.raises(ValueError):
        parse_features(raw)


@pytest.mark.parametrize("metadata", [None, {}, {"synthetic": False},
    {"synthetic": True}, {"synthetic": True, "day_utc": "not-a-date"}])
def test_missing_synthetic_label_or_bad_day_is_rejected(tmp_path, metadata):
    source = tmp_path / "bad-fixture.json"
    source.write_text(json.dumps({
        "type": "FeatureCollection", "metadata": metadata, "features": []
    }))
    with pytest.raises(ValueError):
        capture_fixture(source, tmp_path / "raw")
    assert not (tmp_path / "raw").exists()
