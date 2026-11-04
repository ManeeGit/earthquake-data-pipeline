# Changelog

## Unreleased

### Milestone 1 — offline capture

- Added a two-event synthetic USGS-shaped GeoJSON fixture.
- Added a command-line offline capture with byte-preserved raw JSON and a
  separate UTC retrieval receipt, counts and SHA-256 fingerprint.
- Preserved prior captures on reruns and logged row counts and elapsed time.
- Added 15 offline test cases covering parsing, missing magnitude, empty input,
  malformed containers, provenance and capture history.
- Pinned dependencies for Python 3.14.6 and verified DuckDB on macOS ARM64.
- Added architecture, data dictionary, a guided lesson and learning journal.
- Prepared public-repository CI, contribution guidance and an MIT license.

### Planned

Transformation and quarantine, revision-aware DuckDB loading, bounded live
extraction, and SQL/CSV reporting are reserved for milestones 2–5.
