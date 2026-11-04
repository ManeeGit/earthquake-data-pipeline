# Architecture

Solid arrows show the implemented milestone. Dotted arrows show planned work.

```mermaid
flowchart TD
    F[Clearly labeled synthetic fixture] --> E[extract.py: capture_fixture]
    E --> R[Original response.json]
    E --> M[metadata.json: source, UTC dates, hash]
    E --> C[Terminal count and duration log]
    U[USGS API: one UTC day] -. milestone 4 .-> L[Bounded live extraction]
    L -.-> R
    L -.-> M
    R -. milestone 2 .-> T[transform.py: validate and flatten]
    T -. invalid records .-> Q[Quarantine with reasons and source capture]
    T -. valid rows .-> D[load.py: revision-aware event ID updates]
    D -. milestone 3 .-> DB[(DuckDB file)]
    DB -. milestone 5 .-> S[SQL files and report.py]
    S -.-> O[Terminal reports and CSV files]
```

Extraction obtains data; transformation decides how to interpret it; loading
changes database state; reporting reads that state. Keeping these stages separate
lets us test and rerun each one independently. Only `extract.py` exists today.

Data flow in milestone 1 is entirely local. The fixture and resulting captures
are small; each command finishes and exits. Later, DuckDB will use a conservative
memory limit and thread count suitable for an 8 GB machine. Offline/live captures
and databases will remain separate. No background service or scheduler is planned.
