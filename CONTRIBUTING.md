# Contributing

This is a learning project maintained by ManeeGit. Changes should make the
pipeline easier to understand and verify while respecting its small milestones.

## Local setup

Follow the [README](README.md#getting-started) to create `.venv` and install the
pinned dependencies. Run these checks from the repository root before proposing
a change:

```sh
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
.venv/bin/python -m earthquake_pipeline offline
git diff --check
```

The tests and demo use synthetic data and require no network after installation.
The demo creates ignored files under `data/`; those files are not source code.

## Scope a change

- Keep each change focused on one behavior or documentation improvement.
- Describe the problem, resulting behavior and checks actually run.
- Add meaningful tests when behavior changes, using local fixtures or mocked
  requests. Do not make test results depend on the live USGS service.
- Label invented events and example results clearly. Do not present planned
  features or unmeasured results as implemented or verified.
- Update the learning journal and relevant documentation when a decision changes.
- Keep later milestones separate until the learner has completed the current
  exercise and discussion.

## Files to keep local

Do not commit virtual environments, local credentials, generated captures,
database files or reports. Raw receipts contain local source paths, so inspect
any example before intentionally publishing it. A minimal synthetic fixture
usually communicates a bug more clearly than a large data dump.

Dependency updates should have exact pins, an explanation of compatibility, and
a passing test run. GitHub Actions references are pinned to full commit IDs;
update their version comments when changing those pins.
