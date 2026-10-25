# UM TTS Assets (`um-tts-assets`)

Versioned Tabletop Simulator (TTS) asset repository for **Unmatched Evergreen** (`buffy`, `season-1`, `season-2`) and anonymized custom characters (`custom-character-1`).

All assets are served via raw GitHub URLs with cache-busting query strings (`?v=N`) so Tabletop Simulator automatically fetches updated card sheets and models without requiring manual Steam Cloud uploads.

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

### 2. `update_balance_notes.py` (Manage Local Balance Note Templates & Sync Scoped Changelog)
Reads the local `balance_notes.md` templates inside each `um_evergreen` season folder and updates the season/character-scoped `## Changelog` below.

- `_BuffyRework/balance_notes.md`
- `_Season 1/balance_notes.md`
- `_Season 2/balance_notes.md`

```bash
# Sync balance notes for a specific season into README.md and push
python3 update_balance_notes.py --season buffy
python3 update_balance_notes.py --season season-1
python3 update_balance_notes.py --season season-2

# Sync all seasons' balance notes
python3 update_balance_notes.py --all
```

---

## Current Asset Inventory

<!-- ASSET_INVENTORY_START -->
| Group / Season | Asset | Version | Raw URL |
| --- | --- | --- | --- |
| `custom-character-1` | `card-back.jpg` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/card-back.jpg?v=1) |
| `custom-character-1` | `cards-sheet.jpg` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/cards-sheet.jpg?v=1) |
| `custom-character-1` | `character-card-back.jpg` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/character-card-back.jpg?v=1) |
| `custom-character-1` | `character-card-front.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/character-card-front.png?v=1) |
| `custom-character-1` | `health-dial.obj` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/health-dial.obj?v=1) |
| `custom-character-1` | `hero-dial.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/hero-dial.png?v=1) |
| `custom-character-1` | `hero-mini.obj` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/hero-mini.obj?v=1) |
| `custom-character-1` | `sidekick-dial.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/sidekick-dial.png?v=1) |
| `custom-character-1` | `sidekick-token.jpg` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/sidekick-token.jpg?v=1) |
| `custom-character-1` | `sidekick-token.obj` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/custom-character-1/sidekick-token.obj?v=1) |
| `um-evergreen/buffy` | `abilities-buffy-set.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/buffy/abilities-buffy-set.png?v=1) |
| `um-evergreen/buffy` | `angel.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/buffy/angel.png?v=1) |
| `um-evergreen/buffy` | `buffy.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/buffy/buffy.png?v=1) |
| `um-evergreen/buffy` | `spike.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/buffy/spike.png?v=1) |
| `um-evergreen/buffy` | `willow.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/buffy/willow.png?v=1) |
| `um-evergreen/season-1` | `arthur.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-1/arthur.png?v=1) |
| `um-evergreen/season-1` | `bloody-mary.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-1/bloody-mary.png?v=1) |
| `um-evergreen/season-1` | `invisible-man.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-1/invisible-man.png?v=1) |
| `um-evergreen/season-1` | `jekyll-and-hyde.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-1/jekyll-and-hyde.png?v=1) |
| `um-evergreen/season-1` | `medusa.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-1/medusa.png?v=1) |
| `um-evergreen/season-1` | `sherlock.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-1/sherlock.png?v=1) |
| `um-evergreen/season-2` | `beowulf.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-2/beowulf.png?v=1) |
| `um-evergreen/season-2` | `bigfoot.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-2/bigfoot.png?v=1) |
| `um-evergreen/season-2` | `dr-sattler.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-2/dr-sattler.png?v=1) |
| `um-evergreen/season-2` | `ghost-rider.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-2/ghost-rider.png?v=1) |
| `um-evergreen/season-2` | `she-hulk.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-2/she-hulk.png?v=1) |
| `um-evergreen/season-2` | `spider-man.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-2/spider-man.png?v=1) |
| `um-evergreen/season-2` | `winter-soldier.png` | `v1` | [Link](https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets/um-evergreen/season-2/winter-soldier.png?v=1) |
<!-- ASSET_INVENTORY_END -->

---

## Changelog (Scoped by Season & Character)

<!-- CHANGELOG_ENTRIES_START -->
<!-- CHANGELOG_ENTRIES_END -->
