# UM TTS Assets (`um-tts-assets`)

Versioned Tabletop Simulator (TTS) asset repository for **Unmatched Evergreen** (`buffy`, `season-1`, `season-2`) and anonymized custom characters (`custom-character-1`).

All assets are served via raw GitHub URLs with cache-busting query strings (`?v=N`) so Tabletop Simulator automatically fetches updated card sheets and models without requiring manual Steam Cloud uploads.

---

## Season Changelogs & Balance Logs

Each season has its own dedicated changelog folder:

- **[Buffy Set Changelog & Balance Notes](changelogs/buffy/README.md)** (`changelogs/buffy/`)
- **[Season 1 Changelog & Balance Notes](changelogs/season-1/README.md)** (`changelogs/season-1/`)
- **[Season 2 Changelog & Balance Notes](changelogs/season-2/README.md)** (`changelogs/season-2/`)

---

## Workflow Scripts

This repository uses two separate scripts:

### 1. `update_tts_assets.py` (Sync Assets & Update TTS Table JSON)
Compares local TTS assets against the repo via SHA-256, copies changed files, bumps `?v=N` version numbers, pushes to GitHub, and updates the URLs in your TTS Tournament Table `.json` file.

```bash
# Update assets & TTS table JSON for a single season/group
python3 update_tts_assets.py --season buffy
python3 update_tts_assets.py --season season-1
python3 update_tts_assets.py --season season-2

# Update all Evergreen seasons at once
python3 update_tts_assets.py --all

# Preview without modifying files or pushing
python3 update_tts_assets.py --season season-1 --dry-run
```

> **Changing the Target Tournament Table:** Update `TABLE_NAME` at the top of `update_tts_assets.py` whenever a new tournament table save is released.

---

### 2. `update_balance_notes.py` (Generate Per-Season Changelogs from Local Balance Notes)
Reads the local `balance_notes.md` templates inside each `um_evergreen` season folder and generates the separate season changelog files under `changelogs/<season>/README.md`.

Local templates:
- `/Users/leomedina/Documents/unmatched/um_evergreen/_BuffyRework/balance_notes.md`
- `/Users/leomedina/Documents/unmatched/um_evergreen/_Season 1/balance_notes.md`
- `/Users/leomedina/Documents/unmatched/um_evergreen/_Season 2/balance_notes.md`

```bash
# Sync balance notes for a specific season into changelogs/<season>/README.md and push
python3 update_balance_notes.py --season buffy
python3 update_balance_notes.py --season season-1
python3 update_balance_notes.py --season season-2

# Sync all seasons' balance notes
python3 update_balance_notes.py --all
```
