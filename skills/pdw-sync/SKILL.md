---
name: pdw-sync
description: "Manually trigger the Personal Data Warehouse sync — pulls Obsidian daily-note tasks and Google Sheets (morning form, workouts, leetcode, purchases, job search) into Postgres on thebigbox, then reports per-source results."
version: 1.0.0
author: jadu
platforms: [macos]
metadata:
  hermes:
    tags: [data, etl, postgres, obsidian, sheets]
    config:
      pdw.project_path: /Users/jadu/projects/personal-data-warehouse
---

# PDW Sync

Manual trigger for the Personal Data Warehouse ETL. Nightly cron (`pdw-nightly-sync`, 3:00 AM) runs the same pipeline automatically — this skill is for on-demand runs.

## What it does

Runs the append-only sync: Obsidian daily notes + five Google Sheets → PostgreSQL (`pdw` database, Docker container `pdw-pg` on thebigbox, reached via SSH tunnel). Idempotent — safe to run any time; already-ingested rows are skipped.

## How to run

Full sync (default):

```bash
cd /Users/jadu/projects/personal-data-warehouse && .venv/bin/python sync.py --trigger manual --source all
```

Single source if Aiden asks (e.g. "just sync workouts"):

```bash
cd /Users/jadu/projects/personal-data-warehouse && .venv/bin/python sync.py --trigger manual --source workout
```

Valid sources: `notes`, `morning`, `workout`, `leetcode`, `purchases`, `jobsearch`, `all`.

## Reporting

The command prints a JSON summary. Relay it conversationally, one line per source:
"Workouts: 12 new rows (349 parsed). Purchases: 3 new. Notes: 0 new, all caught up. ..."

- `inserted` = new rows added this run; `parsed` = total rows seen in source.
- If `ok` is false or exit code is 1: quote the failing source's `error` field verbatim and tell Aiden which sources still succeeded.
- If connection fails entirely: thebigbox or its SSH tunnel is down — say so.

## Rules

- Never edit the database directly; only run sync.py.
- Never modify source sheets or notes.
- Exit code 0 = success, 1 = at least one source failed.
