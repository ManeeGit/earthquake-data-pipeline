# Learning journal

## 2026-11-04 — milestone 1: offline capture

Status: built and verified; waiting for the learner's exercise and two answers.
Milestones 2–5 have not been implemented.

### Starting point and decisions

- Inspected the project folder: empty. No existing project files or applicable
  ancestor AGENTS.md files were found. All project changes are inside this folder.
- Detected ARM64 and Python 3.14.6. Created `.venv` with the existing interpreter;
  no global packages were installed. Bootstrap pip is 26.1.2.
- Selected DuckDB 1.4.3 and pytest 9.0.2 after checking official documentation and
  PyPI release metadata. DuckDB has a CPython 3.14 macOS ARM64 wheel. Pinned both
  and all four pytest dependencies in `requirements.txt`; recorded Python in
  `.python-version`. No pandas or additional runtime library is needed now.
- Use two clearly invented events for deterministic offline work. A numeric and
  a missing magnitude introduce the distinction between a measurement and an
  unknown value without implementing transformation early.
- Preserve the source bytes and keep retrieval metadata beside them. Use a real
  local source URL and explicitly record that no HTTP request occurred.
- Use explicit UTC timestamps and a declared daily window. Keep occurrence,
  revision and retrieval time conceptually separate.
- Keep a new raw capture on every run. Later database idempotency will be enforced
  by event ID and update timestamp; it does not mean deleting capture history.
- Keep extraction independent of database loading and reports. Verified DuckDB
  can execute SQL, but no event table was created in this milestone.

### Evidence from actual execution

- `.venv/bin/python -m earthquake_pipeline offline` succeeded: 2 features,
  864 bytes, logged extraction elapsed time 0.029693 seconds.
- Capture: `data/raw/offline/20261104T203437589912Z_3ab7fab5/`.
- Retrieval time: `2026-11-04T20:34:37.589912+00:00`.
- Requested fixture window: `2024-01-01T00:00:00+00:00` to
  `2024-01-02T00:00:00+00:00`, end exclusive.
- Saved raw bytes matched the source exactly. SHA-256:
  `c8e3af573add5dc93dcca4c957e5c6364719125be331765f47b840a472f89cf5`.
- Parsed first event: `synthetic-001`, magnitude 2.5, coordinates
  `[-122.5, 38.5, 7.0]`. Second magnitude parsed as Python `None`.
- `.venv/bin/python -m pytest -q`: **15 passed in 0.03s**. Tests cover fixture
  parsing, null magnitude preservation, source bytes and metadata, capture
  history, empty input, invalid containers and missing/bad fixture labels/dates.
- `.venv/bin/python -m pip check`: `No broken requirements found.`
- SQL compatibility check: `SELECT 42 AS answer` returned `[(42,)]` with an
  in-memory DuckDB connection limited to 256 MB and one thread.
- Python confirmed it was inside a virtual environment. Installed versions:
  DuckDB 1.4.3, pytest 9.0.2, iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0,
  Pygments 2.19.2.

These are real execution results with synthetic input, not earthquake observations.

### Environment finding to carry into live mode

A read-only metadata lookup using the existing Python's `urllib.request` failed
with `CERTIFICATE_VERIFY_FAILED` against PyPI. macOS `curl` and pip succeeded with
certificate verification enabled. Nothing changed the global certificate setup.
Before milestone 4, configure a verified project-local certificate solution and
test HTTPS; pin any dependency added for it. Never work around this by disabling
verification. This issue does not affect the offline demo or tests.

### Learning checkpoint

Exercise: copy `fixtures/synthetic_earthquakes.json` to
`fixtures/my_earthquakes.json`, change only `synthetic-001`'s magnitude from 2.5
to 3.1, and run the offline command with `--fixture` pointing to the copy. Inspect
the printed raw file and report its feature count and first magnitude.

1. Why keep our retrieval metadata in a separate file from the raw JSON?
2. What would go wrong if we changed a missing magnitude (`null`) to `0`?

Learner response: pending. Do not begin milestone 2 before discussing the response.

### Next steps after the response

Explain and implement only milestone 2: flattening, UTC conversion, required IDs,
timestamps and coordinates, missing/invalid magnitude rules, quarantine records
with reasons, and tests using synthetic edge cases. Explain the data flow and
success criteria before coding, show actual input/output, then give one exercise
and two questions and pause again.

Later checkpoints: duplicate/revision semantics in milestone 3; bounded requests,
truncation detection, inclusive USGS endtime, verified HTTPS, empty responses and
API failures in milestone 4; counts, magnitude summaries, top ten and CSV/terminal
reports in milestone 5. Add stage counts and timings as each stage is built.

## 2026-11-04 — prepare the GitHub portfolio repository

The learner requested a repository under ManeeGit and selected public visibility.
This publishing step does not advance the pipeline beyond milestone 1 or replace
the pending exercise and questions.

- Initialized a separate Git repository in the project directory because the
  Desktop is already an unrelated repository. No parent repository files were
  staged or changed.
- Configured the project-local author as ManeeGit with the account's GitHub
  no-reply email. The initial commit uses the actual current date.
- Reworked the README for a fresh clone and moved the guided walkthrough into
  `docs/milestone-01.md`; retained the original measured output.
- Added contribution guidance, changelog, MIT license, editor defaults, line
  ending rules and exclusions for local credentials, databases and build files.
- Added a GitHub Actions workflow using commit-pinned official actions,
  read-only repository permissions and a five-minute timeout. It runs tests and
  the synthetic demo only in public repositories, with no cached dependencies
  or uploaded artifacts; private copies skip it to avoid paid usage.
- Rechecked locally: 15 tests passed in 0.03s; pip reported no broken
  requirements; the demo captured 2 features and 864 bytes; documentation file
  links resolved. CI is not claimed as passing until GitHub runs it.

Publication target: `ManeeGit/earthquake-data-pipeline`. Remote publication and
CI verification are pending authentication at the time of this entry.

## 2026-11-04 — published and verified on GitHub

- Created the public repository:
  [ManeeGit/earthquake-data-pipeline](https://github.com/ManeeGit/earthquake-data-pipeline).
- Pushed the initial commit `916bb80a44b9280a3f7f0e1806ec20944de5f532` to `main`
  with 20 source and documentation files. No environment, generated captures or
  unrelated Desktop files were published.
- Verified the uploaded Git tree matched the local committed tree exactly:
  `374e6c3558f615866d3a33e0f81476ef02447784`.
- Confirmed public visibility, default branch `main`, project description and
  relevant repository topics.
- The first [GitHub verification run](https://github.com/ManeeGit/earthquake-data-pipeline/actions/runs/41909951061)
  completed successfully, including dependency checks, the offline pytest suite
  and the synthetic demo on Ubuntu.
- Added a live workflow-status badge to the README; its state comes from GitHub.

Next: discuss the pending milestone 1 exercise and questions before beginning
transformation and quarantine in milestone 2. Publication does not change the
implemented milestone scope.
