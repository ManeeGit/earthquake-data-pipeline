# Milestone 1: capture before cleaning

A fixture is a small, fixed input that lets us work without an API connection.
Our fixture imitates the USGS GeoJSON structure but contains only invented events.
Extraction captures that input; cleaning and interpretation come later.

## Data flow

```text
Synthetic fixture → unchanged response.json + metadata.json → terminal count
```

## Success criteria

- Source and saved JSON match byte for byte.
- The receipt identifies the synthetic source, UTC window and retrieval time.
- A second run keeps the first capture intact.
- Empty lists work; malformed containers produce a clear error.
- Tests run offline and extraction logs a count and elapsed time.

## Walk through the implementation


1. Open [fixtures/synthetic_earthquakes.json](../fixtures/synthetic_earthquakes.json).
   The outer object is a `FeatureCollection`. Its `features` list contains two
   invented events. `synthetic-001` has magnitude `2.5`; `synthetic-002` has `null`.
2. Read `parse_features` in [extract.py](../earthquake_pipeline/extract.py).
   `json.loads` turns JSON into Python objects. It checks the outer container and
   list, leaving individual event validation for milestone 2. JSON `null` becomes
   Python `None`; it is not replaced with zero.
3. Read `capture_fixture` in the same file. `read_bytes` and `write_bytes` preserve
   the source exactly. `datetime.now(UTC)` records when we read it. A separate
   metadata file avoids editing the original. SHA-256 is a fingerprint we can
   compare to detect changed bytes. A unique directory preserves previous runs.
4. Read [test_extract.py](../tests/test_extract.py). `assert` expresses an expected
   result; `tmp_path` gives each test a temporary directory. The tests check byte
   preservation, provenance, parsing, missing magnitude, empty data, malformed
   containers, required fixture labels/dates, and reruns. They make no HTTP calls.
5. [__main__.py](../earthquake_pipeline/__main__.py) connects the command-line arguments
   to extraction and prints the capture paths. It exits with an error for a bad
   fixture instead of announcing a successful capture.

Malformed fixture containers are rejected before writing a capture. Malformed
individual events are currently retained unchanged. Their quarantine rules come
in milestone 2; live response archival and API failure handling come in milestone 4.

## Exercise and questions


Copy the fixture, then change only `synthetic-001`'s magnitude from `2.5` to `3.1`
in the copy:

```sh
cp fixtures/synthetic_earthquakes.json fixtures/my_earthquakes.json
# Edit fixtures/my_earthquakes.json in your editor, then run:
.venv/bin/python -m earthquake_pipeline offline --fixture fixtures/my_earthquakes.json
```

Open the new `response.json` at the printed path. Tell me the captured count and
the magnitude saved for `synthetic-001`.

1. Why keep our retrieval metadata in a separate file from the raw JSON?
2. What would go wrong if we changed a missing magnitude (`null`) to `0`?

We pause here until you reply. The next milestone is transformation and validation.
