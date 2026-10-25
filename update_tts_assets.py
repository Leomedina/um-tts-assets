#!/usr/bin/env python3
"""
Script 1 of 2: Asset Sync & TTS Table JSON Updater (`update_tts_assets.py`)

Syncs local Unmatched TTS assets from um_evergreen to the GitHub repo (um-tts-assets),
checks which files changed via SHA-256, bumps cache-busting versions (?v=N),
updates the Asset Inventory in README.md, commits/pushes to GitHub, and updates
the Unmatched Official Tournament Table JSON file.

(For syncing character balance notes / changelogs, use `update_balance_notes.py`.)

Usage examples:
  python3 update_tts_assets.py --season buffy
  python3 update_tts_assets.py --season season-1
  python3 update_tts_assets.py --season season-2
  python3 update_tts_assets.py --all
  python3 update_tts_assets.py --season season-1 --dry-run
"""

import argparse
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# ==============================================================================
# CONFIGURATION — Change TABLE_NAME when a new tournament table is released
# ==============================================================================
TABLE_NAME = "Unmatched Official Tournament Table April 2026 (Stars and Stripes, Hamlet fixed)"

# Base directories
UNMATCHED_DIR = Path("/Users/leomedina/Documents/unmatched")
TTS_FOLDER = UNMATCHED_DIR / "TTS"
TTS_SAVES_FOLDER = Path.home() / "Library" / "Tabletop Simulator" / "Saves"
EVERGREEN_DIR = UNMATCHED_DIR / "um_evergreen"
NARUTO_DIR = UNMATCHED_DIR / "Naruto"
REPO_DIR = UNMATCHED_DIR / "um-tts-assets"
ASSETS_DIR = REPO_DIR / "assets"
VERSIONS_FILE = REPO_DIR / "versions.json"

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets"


# ==============================================================================
# SEASON FOLDERS & FIGHTER MAPPING DEFINITIONS
# ==============================================================================
SEASON_SOURCE_DIRS: Dict[str, Tuple[Path, str]] = {
    "buffy": (EVERGREEN_DIR / "_BuffyRework" / "_final_tts", "um-evergreen/buffy"),
    "season-1": (EVERGREEN_DIR / "_Season 1" / "_final_tts", "um-evergreen/season-1"),
    "season-2": (EVERGREEN_DIR / "_Season 2" / "_final_tts", "um-evergreen/season-2"),
}

SEASON_ASSETS: Dict[str, List[dict]] = {
    "buffy": [
        {
            "name": "Buffy",
            "source": EVERGREEN_DIR / "_BuffyRework" / "_final_tts" / "Buffy.png",
            "repo_rel": "um-evergreen/buffy/buffy.png",
            "fighter_guids": ["758e7d"],
            "deck_slot": "176",
        },
        {
            "name": "Angel",
            "source": EVERGREEN_DIR / "_BuffyRework" / "_final_tts" / "Angel.png",
            "repo_rel": "um-evergreen/buffy/angel.png",
            "fighter_guids": ["8ae8f5"],
            "deck_slot": "176",
        },
        {
            "name": "Spike",
            "source": EVERGREEN_DIR / "_BuffyRework" / "_final_tts" / "Spike.png",
            "repo_rel": "um-evergreen/buffy/spike.png",
            "fighter_guids": ["b9d8a4"],
            "deck_slot": "176",
        },
        {
            "name": "Willow",
            "source": EVERGREEN_DIR / "_BuffyRework" / "_final_tts" / "WillowV2.png",
            "repo_rel": "um-evergreen/buffy/willow.png",
            "fighter_guids": ["9e79df"],
            "deck_slot": "176",
        },
        {
            "name": "Buffy Set Abilities",
            "source": EVERGREEN_DIR / "_BuffyRework" / "_final_tts" / "Abilities_BuffySet.png",
            "repo_rel": "um-evergreen/buffy/abilities-buffy-set.png",
            "fighter_guids": ["758e7d", "8ae8f5", "b9d8a4", "9e79df"],
            "deck_slot": "3",
        },
    ],
    "season-1": [
        {
            "name": "King Arthur",
            "source": EVERGREEN_DIR / "_Season 1" / "_final_tts" / "Arthur.png",
            "repo_rel": "um-evergreen/season-1/arthur.png",
            "fighter_guids": ["1d8e72"],
            "deck_slot": "176",
        },
        {
            "name": "Bloody Mary",
            "source": EVERGREEN_DIR / "_Season 1" / "_final_tts" / "BloodyMary.png",
            "repo_rel": "um-evergreen/season-1/bloody-mary.png",
            "fighter_guids": ["a3a6c6"],
            "deck_slot": "176",
        },
        {
            "name": "Invisible Man",
            "source": EVERGREEN_DIR / "_Season 1" / "_final_tts" / "InvisibleMan.png",
            "repo_rel": "um-evergreen/season-1/invisible-man.png",
            "fighter_guids": ["384a8b"],
            "deck_slot": "176",
        },
        {
            "name": "Dr. Jekyll & Mr. Hyde",
            "source": EVERGREEN_DIR / "_Season 1" / "_final_tts" / "Jekyll&Hyde.png",
            "repo_rel": "um-evergreen/season-1/jekyll-and-hyde.png",
            "fighter_guids": ["3efaee"],
            "deck_slot": "176",
        },
        {
            "name": "Medusa",
            "source": EVERGREEN_DIR / "_Season 1" / "_final_tts" / "Medusa.png",
            "repo_rel": "um-evergreen/season-1/medusa.png",
            "fighter_guids": ["65070e"],
            "deck_slot": "176",
        },
        {
            "name": "Sherlock Holmes",
            "source": EVERGREEN_DIR / "_Season 1" / "_final_tts" / "Sherlock.png",
            "repo_rel": "um-evergreen/season-1/sherlock.png",
            "fighter_guids": ["248c8e"],
            "deck_slot": "176",
        },
        {
            "name": "Season 1 Abilities",
            "source": EVERGREEN_DIR / "_Season 1" / "_final_tts" / "Abilities_S1.png",
            "repo_rel": "um-evergreen/season-1/abilities-s1.png",
            "fighter_guids": ["1d8e72", "a3a6c6", "384a8b", "3efaee", "65070e", "248c8e"],
            "deck_slot": "3",
            "optional": True,
        },
    ],
    "season-2": [
        {
            "name": "Beowulf",
            "source": EVERGREEN_DIR / "_Season 2" / "_final_tts" / "beowulf.png",
            "repo_rel": "um-evergreen/season-2/beowulf.png",
            "fighter_guids": ["23da2d"],
            "deck_slot": "176",
        },
        {
            "name": "Bigfoot",
            "source": EVERGREEN_DIR / "_Season 2" / "_final_tts" / "Bigfoot.png",
            "repo_rel": "um-evergreen/season-2/bigfoot.png",
            "fighter_guids": ["5d4e2c"],
            "deck_slot": "176",
        },
        {
            "name": "Dr. Sattler",
            "source": EVERGREEN_DIR / "_Season 2" / "_final_tts" / "DrSattler.png",
            "repo_rel": "um-evergreen/season-2/dr-sattler.png",
            "fighter_guids": ["47f574"],
            "deck_slot": "176",
        },
        {
            "name": "Ghost Rider",
            "source": EVERGREEN_DIR / "_Season 2" / "other" / "9DD8E3460E69C6524BBB986C46F277C96608446C_Ghost Rider.png",
            "repo_rel": "um-evergreen/season-2/ghost-rider.png",
            "fighter_guids": ["61bda2"],
            "deck_slot": "176",
        },
        {
            "name": "She-Hulk",
            "source": EVERGREEN_DIR / "_Season 2" / "_final_tts" / "_She-Hulk.png",
            "repo_rel": "um-evergreen/season-2/she-hulk.png",
            "fighter_guids": ["04711f"],
            "deck_slot": "176",
        },
        {
            "name": "Spider-Man",
            "source": EVERGREEN_DIR / "_Season 2" / "_final_tts" / "Spider-man.png",
            "repo_rel": "um-evergreen/season-2/spider-man.png",
            "fighter_guids": ["828053"],
            "deck_slot": "176",
        },
        {
            "name": "Winter Soldier",
            "source": EVERGREEN_DIR / "_Season 2" / "_final_tts" / "_WinterSoldier.png",
            "repo_rel": "um-evergreen/season-2/winter-soldier.png",
            "fighter_guids": ["fe0138"],
            "deck_slot": "176",
        },
    ],
    # Note: Custom character assets only sync to the GitHub repo if requested;
    # custom character JSON files are intentionally NOT touched.
    "custom-character-1": [
        {
            "name": "Custom Character 1 - Hero Mini",
            "source": NARUTO_DIR / "Assets" / "naruto.obj",
            "repo_rel": "custom-character-1/hero-mini.obj",
            "fighter_guids": [],
            "deck_slot": None,
        },
        {
            "name": "Custom Character 1 - Hero Dial",
            "source": NARUTO_DIR / "Assets" / "naruto dial.png",
            "repo_rel": "custom-character-1/hero-dial.png",
            "fighter_guids": [],
            "deck_slot": None,
        },
        {
            "name": "Custom Character 1 - Sidekick Dial",
            "source": NARUTO_DIR / "uzumaki-naruto-cards" / "Components" / "gamabunta-dial.png",
            "repo_rel": "custom-character-1/sidekick-dial.png",
            "fighter_guids": [],
            "deck_slot": None,
        },
        {
            "name": "Custom Character 1 - Sidekick Token",
            "source": NARUTO_DIR / "uzumaki-naruto-cards" / "Components" / "gamabunta-token.jpg",
            "repo_rel": "custom-character-1/sidekick-token.jpg",
            "fighter_guids": [],
            "deck_slot": None,
        },
    ],
}


def slugify_filename(filename: str) -> str:
    stem = Path(filename).stem.lstrip("_")
    ext = Path(filename).suffix.lower()
    stem = stem.replace("&", "-and-")
    stem = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", stem)
    stem = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()
    return f"{stem}{ext}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_versions() -> Dict[str, dict]:
    if VERSIONS_FILE.exists():
        with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_versions(versions: Dict[str, dict]) -> None:
    with open(VERSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(versions, f, indent=2, sort_keys=True)
        f.write("\n")


def discover_unmapped_files(season: str, known_sources: Set[Path], known_repo_rels: Set[str]) -> List[dict]:
    extra_specs = []
    if season not in SEASON_SOURCE_DIRS:
        return extra_specs

    src_dir, repo_subdir = SEASON_SOURCE_DIRS[season]
    if not src_dir.exists():
        return extra_specs

    for p in sorted(src_dir.iterdir()):
        if p.name.startswith(".") or not p.is_file():
            continue
        if p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".obj"}:
            continue
        if p in known_sources:
            continue
        slug = slugify_filename(p.name)
        repo_rel = f"{repo_subdir}/{slug}"
        if repo_rel not in known_repo_rels:
            extra_specs.append(
                {
                    "name": p.stem.lstrip("_"),
                    "source": p,
                    "repo_rel": repo_rel,
                    "fighter_guids": [],
                    "deck_slot": None,
                }
            )
    return extra_specs


def get_table_paths() -> List[Path]:
    filename = TABLE_NAME if TABLE_NAME.endswith(".json") else f"{TABLE_NAME}.json"
    candidates = [
        TTS_FOLDER / filename,
        TTS_SAVES_FOLDER / filename,
    ]
    return [p for p in candidates if p.exists()]


def update_fighter_bag_urls(bag_obj: dict, deck_slot: str, new_url: str) -> int:
    replacements = 0

    def walk(node):
        nonlocal replacements
        if isinstance(node, dict):
            custom_deck = node.get("CustomDeck")
            if isinstance(custom_deck, dict) and deck_slot in custom_deck:
                slot_dict = custom_deck[deck_slot]
                if isinstance(slot_dict, dict) and slot_dict.get("FaceURL") != new_url:
                    slot_dict["FaceURL"] = new_url
                    replacements += 1
            for k, v in node.items():
                if k != "ChildObjects":
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(bag_obj.get("ContainedObjects", []))
    return replacements


def git_commit_and_push(changed_rel_paths: List[str], selected_seasons: List[str], dry_run: bool, no_push: bool) -> None:
    if dry_run:
        print("\n[DRY-RUN] Skipping git commit & push.")
        return

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    if not status:
        print("\n[GIT] Working tree clean — nothing new to commit.")
        return

    subprocess.run(
        ["git", "add", "assets", "versions.json", "README.md", "update_tts_assets.py"],
        cwd=REPO_DIR,
        check=True,
    )
    diff_cached = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_DIR)
    if diff_cached.returncode == 0:
        print("\n[GIT] No staged changes to commit.")
        return

    if changed_rel_paths:
        summary = ", ".join(Path(p).name for p in changed_rel_paths[:5])
        if len(changed_rel_paths) > 5:
            summary += f" (+{len(changed_rel_paths) - 5} more)"
        msg = f"Update TTS assets ({', '.join(selected_seasons)}): {summary}"
    else:
        msg = f"Update TTS asset versions ({', '.join(selected_seasons)})"

    subprocess.run(["git", "commit", "-m", msg], cwd=REPO_DIR, check=True)
    print(f"\n[GIT] Committed: {msg}")

    if not no_push:
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True)
        print("[GIT] Pushed to origin/main.")


def main() -> None:
    valid_seasons = list(SEASON_ASSETS.keys())
    parser = argparse.ArgumentParser(
        description="Sync local Unmatched TTS assets to GitHub and update the TTS Tournament Table JSON."
    )
    parser.add_argument(
        "-s",
        "--season",
        action="append",
        choices=valid_seasons + ["all"],
        help=f"Season(s)/group(s) to update: {', '.join(valid_seasons)}, or 'all'. Can be passed multiple times.",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Update all evergreen seasons/groups (buffy, season-1, season-2).",
    )
    parser.add_argument(
        "--force-bump",
        action="store_true",
        help="Force bump ?v=N version numbers even if file hashes have not changed.",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Commit changes locally in um-tts-assets but do not push to GitHub.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would change without modifying files or pushing.",
    )

    args = parser.parse_args()

    if not args.season and not args.all:
        parser.print_help()
        print("\n[!] Please specify which season to update (e.g. --season buffy, --season season-1, --season season-2) or use --all.")
        sys.exit(1)

    if args.all or (args.season and "all" in args.season):
        selected_seasons = ["buffy", "season-1", "season-2"]
    else:
        selected_seasons = []
        for s in args.season:
            if s not in selected_seasons:
                selected_seasons.append(s)

    today_str = datetime.date.today().isoformat()

    print(f"Target Table : {TABLE_NAME}")
    print(f"Seasons      : {', '.join(selected_seasons)}")
    if args.dry_run:
        print("Mode         : DRY RUN (no files will be modified)")
    print("-" * 72)

    versions = load_versions()
    changed_repo_files: List[str] = []
    json_updates_to_apply: List[Tuple[str, List[str], str, str]] = []

    for season in selected_seasons:
        print(f"\n=== Checking [{season}] ===")
        specs = list(SEASON_ASSETS[season])
        known_sources = {s["source"] for s in specs}
        known_repo_rels = {s["repo_rel"] for s in specs}

        extra_specs = discover_unmapped_files(season, known_sources, known_repo_rels)
        specs.extend(extra_specs)

        for spec in specs:
            name = spec["name"]
            src: Path = spec["source"]
            repo_rel: str = spec["repo_rel"]
            dest: Path = ASSETS_DIR / repo_rel
            optional: bool = spec.get("optional", False)

            if not src.exists():
                if dest.exists():
                    print(f"  [REMOVED                 ] {name:24s} -> removed assets/{repo_rel}")
                    changed_repo_files.append(repo_rel)
                    versions.pop(repo_rel, None)
                    if not args.dry_run:
                        dest.unlink()
                elif not optional:
                    print(f"  [MISSING                 ] {name:24s} -> local source not found at {src}")
                continue

            src_hash = sha256_file(src)
            dest_exists = dest.exists()
            dest_hash = sha256_file(dest) if dest_exists else None

            entry = versions.get(repo_rel, {})
            current_ver = int(entry.get("version", 1))
            last_updated = entry.get("last_updated", today_str)
            history: List[dict] = list(entry.get("history", [{"version": current_ver, "date": last_updated}]))

            if not dest_exists:
                new_ver = 1
                status_label = f"ADDED (v{new_ver})"
                file_changed = True
                last_updated = today_str
                history = [{"version": new_ver, "date": today_str}]
            elif src_hash != dest_hash:
                new_ver = current_ver + 1
                status_label = f"CHANGED (v{current_ver} -> v{new_ver})"
                file_changed = True
                last_updated = today_str
                history.append({"version": new_ver, "date": today_str})
            elif args.force_bump:
                new_ver = current_ver + 1
                status_label = f"FORCE-BUMPED (v{current_ver} -> v{new_ver})"
                file_changed = True
                last_updated = today_str
                history.append({"version": new_ver, "date": today_str})
            else:
                new_ver = current_ver
                status_label = f"UNCHANGED (v{new_ver})"
                file_changed = False

            print(f"  [{status_label:24s}] {name:24s} -> assets/{repo_rel}")

            if file_changed:
                changed_repo_files.append(repo_rel)
                if not args.dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if src_hash != dest_hash:
                        shutil.copy2(src, dest)

            versions[repo_rel] = {
                "version": new_ver,
                "sha256": src_hash,
                "last_updated": last_updated,
                "history": history,
            }

            if spec["fighter_guids"] and spec["deck_slot"]:
                github_url = f"{GITHUB_RAW_BASE}/{repo_rel}?v={new_ver}"
                json_updates_to_apply.append(
                    (name, spec["fighter_guids"], spec["deck_slot"], github_url)
                )

    if not args.dry_run:
        save_versions(versions)

    git_commit_and_push(
        changed_rel_paths=changed_repo_files,
        selected_seasons=selected_seasons,
        dry_run=args.dry_run,
        no_push=args.no_push,
    )

    if json_updates_to_apply:
        table_paths = get_table_paths()
        if not table_paths:
            print(
                f"\n[!] WARNING: Could not find '{TABLE_NAME}.json' in:\n"
                f"    - {TTS_FOLDER}\n"
                f"    - {TTS_SAVES_FOLDER}"
            )
            sys.exit(1)

        for table_path in table_paths:
            print(f"\n=== Updating TTS Table JSON: {table_path} ===")
            with open(table_path, "r", encoding="utf-8") as f:
                table_data = json.load(f)

            by_guid = {
                obj.get("GUID"): obj
                for obj in table_data.get("ObjectStates", [])
                if isinstance(obj, dict) and obj.get("GUID")
            }

            total_replacements = 0
            for name, guids, deck_slot, url in json_updates_to_apply:
                asset_replacements = 0
                for g in guids:
                    bag = by_guid.get(g)
                    if not bag:
                        print(f"  [WARN] Fighter GUID {g} ({name}) not found in table JSON!")
                        continue
                    asset_replacements += update_fighter_bag_urls(bag, deck_slot, url)

                if asset_replacements > 0:
                    print(f"  [UPDATED JSON] {name:24s} (slot {deck_slot:>3s}): {asset_replacements:2d} URL(s) -> {url}")
                else:
                    print(f"  [UP-TO-DATE  ] {name:24s} (slot {deck_slot:>3s}): already at {url}")
                total_replacements += asset_replacements

            if total_replacements > 0 and not args.dry_run:
                with open(table_path, "w", encoding="utf-8") as f:
                    json.dump(table_data, f, indent=2, ensure_ascii=False)
                print(f"  Saved {total_replacements} URL update(s) to {table_path.name}")
            elif total_replacements > 0 and args.dry_run:
                print(f"  [DRY-RUN] Would save {total_replacements} URL update(s) to {table_path.name}")
            else:
                print(f"  No JSON changes needed for {table_path.name}.")


if __name__ == "__main__":
    main()
