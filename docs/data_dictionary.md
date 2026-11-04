# Data dictionary

Milestone 1 preserves all source values unchanged. The table below describes the
planned cleaned schema for milestones 2–3; these database columns do not exist yet.
Each JSON path is relative to one object in `features`.

| Planned column | Source JSON path | Meaning and units | Planned missing/invalid handling |
| --- | --- | --- | --- |
| `event_id` | `id` | Opaque source event identifier, stored as text | Require a nonempty string; quarantine invalid IDs |
| `event_time_utc` | `properties.time` | Event occurrence; source is Unix milliseconds since 1970-01-01 UTC | Require a valid numeric timestamp; convert to timezone-aware UTC |
| `updated_at_utc` | `properties.updated` | Last revision time; source is Unix milliseconds | Require a valid timestamp; compare this when deciding whether to update |
| `magnitude` | `properties.mag` | Logarithmic magnitude value, not a distance or linear energy measurement | Absent/null means unknown and becomes SQL NULL; invalid types or non-finite numbers go to quarantine; zero and negative values can be valid |
| `location` | `properties.place` | Human-readable location description | Allow absent/null; do not invent a description |
| `longitude` | `geometry.coordinates[0]` | Decimal degrees east; western values are negative | Require a finite number in [-180, 180] |
| `latitude` | `geometry.coordinates[1]` | Decimal degrees north; southern values are negative | Require a finite number in [-90, 90] |
| `depth_km` | `geometry.coordinates[2]` | Depth in kilometers | Require a finite number; do not reject negative values solely for being negative |

JSON numbers must be actual numbers; booleans will not qualify. Required fields
that are absent or invalid will quarantine the event with reasons and a reference
to its capture. Quarantine is a place to inspect rejected records, not silent
deletion. Magnitude summaries will state how many events have known magnitudes;
they will not claim that an average magnitude is average energy.

## Reading the fixture

The fixture contains only invented events. Its first `time`, `1704067200000`,
represents `2024-01-01T00:00:00+00:00`; `updated` is ten minutes later. The second
event occurs at `2024-01-01T01:00:00+00:00` and has a missing magnitude.

`[-122.5, 38.5, 7.0]` means longitude -122.5°, latitude 38.5°, depth 7.0 km.
Coordinates are longitude first. JSON `null`, Python `None`, and SQL `NULL` are the
representations we will use for an unknown magnitude at successive stages.

UTC is independent of the Mac's America/Chicago timezone. `+00:00` explicitly
means UTC; `Z` is another notation for it. The intended daily window includes
midnight at the start and excludes the next midnight. This gives each event one
daily window. USGS documents its API `endtime` as inclusive, so live extraction
and transformation must account for that boundary in milestone 4. No event-time
filter runs in milestone 1.

## Retrieval receipt, implemented now

| Field | Meaning |
| --- | --- |
| `source_mode` | `synthetic_fixture`; makes invented data explicit |
| `source_url` | Actual local fixture URL; will be an exact request URL in live mode |
| `source_api_reference` | USGS documentation URL, not a claim that we fetched from USGS |
| `http_request_sent` | False for offline capture |
| `retrieved_at_utc` | Actual timezone-aware time when fixture bytes were read |
| `requested_start_utc`, `requested_end_utc` | Intended UTC day from fixture metadata, not retrieval time |
| `window_semantics` | Explains the intended inclusive start and exclusive end |
| `feature_count` | Number of entries in the list, before validation or deduplication |
| `byte_count` | Size of the original JSON in bytes |
| `sha256` | Fingerprint of those bytes, useful for checking preservation |

The fixture's `metadata.synthetic` and `metadata.day_utc` are project-specific
labels; they are not fields we expect the USGS API to provide.

References: [USGS GeoJSON structure](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php),
[USGS query parameters and time boundaries](https://earthquake.usgs.gov/fdsnws/event/1/).
