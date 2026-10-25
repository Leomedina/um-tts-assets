# UM TTS Assets (`um-tts-assets`)

Versioned Tabletop Simulator (TTS) asset repository for **Unmatched Evergreen** (`buffy`, `season-1`, `season-2`) and anonymized custom characters (`custom-character-1`).

All assets are served via raw GitHub URLs with cache-busting query strings (`?v=N`) so Tabletop Simulator automatically fetches updated card sheets and models without requiring manual Steam Cloud uploads.

---

## How to Update Assets & TTS Table JSON

Run `update_tts_assets.py` from `/Users/leomedina/Documents/unmatched/um-tts-assets`:

```bash
# Update a single group / season
python3 update_tts_assets.py --season buffy
python3 update_tts_assets.py --season season-1
python3 update_tts_assets.py --season season-2

# Update with a changelog note (e.g. when a card is added, removed, or rebalanced)
python3 update_tts_assets.py --season buffy --note "Added new card to Buffy deck / updated Willow values"

# Update all Evergreen seasons at once (buffy, season-1, season-2)
python3 update_tts_assets.py --all

# Preview changes without modifying files or pushing
python3 update_tts_assets.py --season season-1 --dry-run
```

### Changing the Target Tournament Table
When a new tournament table save is released, update the `TABLE_NAME` variable at the top of `update_tts_assets.py`:

```python
TABLE_NAME = "Unmatched Official Tournament Table April 2026 (Stars and Stripes, Hamlet fixed)"
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

## Changelog

All added, updated, or removed cards/sheets are logged below automatically by `update_tts_assets.py`.

<!-- CHANGELOG_ENTRIES_START -->

### 2026-10-25 (Initial Import)
- **Added:** Initial TTS card sheets for `um-evergreen/buffy` (`buffy.png`, `angel.png`, `spike.png`, `willow.png`, `abilities-buffy-set.png` at `v1`).
- **Added:** Initial TTS card sheets for `um-evergreen/season-1` (`arthur.png`, `bloody-mary.png`, `invisible-man.png`, `jekyll-and-hyde.png`, `medusa.png`, `sherlock.png` at `v1`).
- **Added:** Initial TTS card sheets for `um-evergreen/season-2` (`beowulf.png`, `bigfoot.png`, `dr-sattler.png`, `ghost-rider.png`, `she-hulk.png`, `spider-man.png`, `winter-soldier.png` at `v1`).
- **Added:** Initial anonymized TTS assets for `custom-character-1` (`cards-sheet.jpg`, `card-back.jpg`, `character-card-front.png`, `character-card-back.jpg`, `hero-mini.obj`, `health-dial.obj`, `hero-dial.png`, `sidekick-dial.png`, `sidekick-token.obj`, `sidekick-token.jpg` at `v1`).
