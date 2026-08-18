# Raw data

The repository intentionally does **not** commit the full NASA C-MAPSS archive. It is public source data and can be several files/large enough to create unnecessary repository weight.

Use `scripts/download_cmapss.py` to retrieve the source locally. Keep downloaded archives and extracted full datasets under this directory; `.gitignore` excludes them.

A small schema/sample contract is kept in `data/reference/` so the pipeline remains understandable without requiring the full source archive.

Source: NASA C-MAPSS Jet Engine Simulated Data.
