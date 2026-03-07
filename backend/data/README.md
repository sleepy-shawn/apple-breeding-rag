# Data Directory

This directory stores local datasets for ingestion at runtime.

By default, large data files under `backend/data/` are ignored by git.
Only small sample files are tracked for demo/testing.

Expected local paths (not tracked):
- `backend/data/papers/*.pdf`
- `backend/data/genes/genes.csv`
- `backend/data/genes/raw_candidates/*`
