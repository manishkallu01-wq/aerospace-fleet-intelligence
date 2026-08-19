# Raw data

The full NASA C-MAPSS archive is not committed to Git because it is unnecessary for the source repository and makes cloning heavier.

## Source

Download **NASA C-MAPSS Jet Engine Simulated Data** from:

https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data

Extract the archive and place the FD001 files in this directory.

The local result build needs:

```text
RUL_FD001.txt
```

The PySpark examples also expect the standard FD001 training/test files when you run the full transformation flow.

## Build the committed result

From the repository root:

```bash
python scripts/build_fd001_results.py
```

That reads `RUL_FD001.txt` and writes `reports/fd001_engine_rul.csv`.

Downloaded archives and full raw datasets are excluded from Git by `.gitignore`.

A small schema/reference document is kept in `data/reference/` so the project structure can be understood without the full source archive.
