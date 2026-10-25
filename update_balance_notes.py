#!/usr/bin/env python3
"""
Script 2 of 2: Balance Notes & Scoped Changelog Generator (`update_balance_notes.py`)

Manages the local per-season `balance_notes.md` templates in `um_evergreen/` and
syncs the season-scoped, per-character balance changelog into `um-tts-assets/README.md`.

(For syncing TTS image/model assets and updating the TTS Table JSON, use `update_tts_assets.py`.)

Usage examples:
  # Sync balance notes for a specific season into README.md and push
  python3 update_balance_notes.py --season buffy
  python3 update_balance_notes.py --season season-1
  python3 update_balance_notes.py --season season-2

  # Sync all seasons' balance notes into README.md
  python3 update_balance_notes.py --all

  # Ensure local balance_notes.md templates have sections for all characters
  python3 update_balance_notes.py --init-templates
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Base directories
UNMATCHED_DIR = Path("/Users/leomedina/Documents/unmatched")
EVERGREEN_DIR = UNMATCHED_DIR / "um_evergreen"
REPO_DIR = UNMATCHED_DIR / "um-tts-assets"
ASSETS_DIR = REPO_DIR / "assets"
VERSIONS_FILE = REPO_DIR / "versions.json"
README_FILE = REPO_DIR / "README.md"

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/Leomedina/um-tts-assets/main/assets"

CHANGELOG_START_MARKER = "<!-- CHANGELOG_ENTRIES_START -->"
CHANGELOG_END_MARKER = "<!-- CHANGELOG_ENTRIES_END -->"

SEASON_CONFIG: Dict[str, dict] = {
    "buffy": {
        "title": "Buffy Set",
        "notes_file": EVERGREEN_DIR / "_BuffyRework" / "balance_notes.md",
        "characters": [
            ("Buffy", "um-evergreen/buffy/buffy.png"),
            ("Angel", "um-evergreen/buffy/angel.png"),
            ("Spike", "um-evergreen/buffy/spike.png"),
            ("Willow", "um-evergreen/buffy/willow.png"),
        ],
    },
    "season-1": {
        "title": "Season 1",
        "notes_file": EVERGREEN_DIR / "_Season 1" / "balance_notes.md",
        "characters": [
            ("King Arthur", "um-evergreen/season-1/arthur.png"),
            ("Bloody Mary", "um-evergreen/season-1/bloody-mary.png"),
            ("Invisible Man", "um-evergreen/season-1/invisible-man.png"),
            ("Dr. Jekyll & Mr. Hyde", "um-evergreen/season-1/jekyll-and-hyde.png"),
            ("Medusa", "um-evergreen/season-1/medusa.png"),
            ("Sherlock Holmes", "um-evergreen/season-1/sherlock.png"),
        ],
    },
    "season-2": {
        "title": "Season 2",
        "notes_file": EVERGREEN_DIR / "_Season 2" / "balance_notes.md",
        "characters": [
            ("Beowulf", "um-evergreen/season-2/beowulf.png"),
            ("Bigfoot", "um-evergreen/season-2/bigfoot.png"),
            ("Dr. Sattler", "um-evergreen/season-2/dr-sattler.png"),
            ("Ghost Rider", "um-evergreen/season-2/ghost-rider.png"),
            ("She-Hulk", "um-evergreen/season-2/she-hulk.png"),
            ("Spider-Man", "um-evergreen/season-2/spider-man.png"),
            ("Winter Soldier", "um-evergreen/season-2/winter-soldier.png"),
        ],
    },
}


def load_versions() -> Dict[str, dict]:
    if VERSIONS_FILE.exists():
        with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def ensure_local_template(season_key: str, dry_run: bool) -> None:
    cfg = SEASON_CONFIG[season_key]
    notes_path: Path = cfg["notes_file"]
    title: str = cfg["title"]
    characters = cfg["characters"]

    if not notes_path.exists():
        lines = [
            f"# {title} — Balance Notes & Card Changes",
            "",
            "Edit the character sections below whenever you add, remove, or rebalance cards.",
            f"When you run `python3 update_balance_notes.py --season {season_key}`, non-empty notes here are automatically synced into the GitHub `README.md` changelog under **{title}**.",
            "",
        ]
        for char_name, _ in characters:
            lines.extend(
                [
                    f"## {char_name}",
                    "- **Hero / Passive Ability:**",
                    "- **Added Cards:**",
                    "- **Removed Cards:**",
                    "- **Card Balance Changes:**",
                    "",
                ]
            )
        if not dry_run:
            notes_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print(f"  [CREATED TEMPLATE] {notes_path}")
        return

    existing_text = notes_path.read_text(encoding="utf-8")
    appended = []
    for char_name, _ in characters:
        if f"## {char_name}" not in existing_text:
            appended.append(
                f"\n## {char_name}\n"
                f"- **Hero / Passive Ability:**\n"
                f"- **Added Cards:**\n"
                f"- **Removed Cards:**\n"
                f"- **Card Balance Changes:**\n"
            )
    if appended:
        if not dry_run:
            notes_path.write_text(existing_text.rstrip() + "\n" + "".join(appended), encoding="utf-8")
        print(f"  [UPDATED TEMPLATE] Added {len(appended)} missing character section(s) to {notes_path}")
    else:
        print(f"  [TEMPLATE OK     ] {notes_path}")


def parse_balance_notes(notes_path: Path) -> Dict[str, List[str]]:
    """
    Parses a season's balance_notes.md file into a dict mapping character name -> list
    of non-empty markdown lines. Empty template placeholders like `- **Added Cards:**`
    (with no text after the colon and no indented sub-items) are filtered out.
    """
    if not notes_path.exists():
        return {}

    lines = notes_path.read_text(encoding="utf-8").splitlines()
    sections: Dict[str, List[str]] = {}
    current_char: Optional[str] = None

    for line in lines:
        if line.startswith("## "):
            current_char = line[3:].strip()
            sections[current_char] = []
        elif current_char is not None:
            sections[current_char].append(line)

    cleaned_sections: Dict[str, List[str]] = {}
    for char_name, raw_lines in sections.items():
        kept: List[str] = []
        i = 0
        while i < len(raw_lines):
            line = raw_lines[i]
            stripped = line.strip()
            if not stripped:
                i += 1
                continue

            m = re.match(r"^-\s+\*\*[^*]+:\*\*\s*(.*)$", stripped)
            if m:
                inline_val = m.group(1).strip()
                sub_items: List[str] = []
                j = i + 1
                while j < len(raw_lines):
                    next_line = raw_lines[j]
                    if not next_line.strip():
                        j += 1
                        continue
                    if next_line.startswith("  ") or next_line.startswith("\t"):
                        if re.sub(r"^[-*]\s*", "", next_line.strip()):
                            sub_items.append(next_line.rstrip())
                        j += 1
                    else:
                        break
                if inline_val or sub_items:
                    kept.append(line.rstrip())
                    kept.extend(sub_items)
                i = j
            else:
                kept.append(line.rstrip())
                i += 1

        if kept:
            cleaned_sections[char_name] = kept

    return cleaned_sections


def build_season_markdown(season_key: str, versions: Dict[str, dict]) -> str:
    cfg = SEASON_CONFIG[season_key]
    season_title: str = cfg["title"]
    notes_path: Path = cfg["notes_file"]
    balance_by_char = parse_balance_notes(notes_path)

    start_marker = f"<!-- SEASON_CHANGELOG_START:{season_key} -->"
    end_marker = f"<!-- SEASON_CHANGELOG_END:{season_key} -->"

    out: List[str] = [start_marker, f"### {season_title}", ""]

    for char_name, repo_rel in cfg["characters"]:
        dest = ASSETS_DIR / repo_rel
        v_info = versions.get(repo_rel, {})
        ver = v_info.get("version", 1)
        last_updated = v_info.get("last_updated", "2026-10-25")
        history = v_info.get("history", [])

        if not dest.exists():
            out.append(f"#### {char_name} (`Removed`)")
            out.append(f"- **Asset Status:** Removed (`assets/{repo_rel}`)")
        else:
            out.append(f"#### {char_name} (`v{ver}` — updated {last_updated})")
            out.append(f"- **TTS Sheet:** [`assets/{repo_rel}?v={ver}`]({GITHUB_RAW_BASE}/{repo_rel}?v={ver})")

        if len(history) > 1:
            hist_str = ", ".join(f"`v{h['version']}` ({h['date']})" for h in history)
            out.append(f"- **Version History:** {hist_str}")

        char_notes = balance_by_char.get(char_name, [])
        if char_notes:
            out.extend(char_notes)
        else:
            out.append(f"- *No balance changes recorded yet (edit `{notes_path.parent.name}/balance_notes.md`).*")

        out.append("")

    # Also include any custom character sections added to balance_notes.md that aren't in the default list
    known_names = {c[0] for c in cfg["characters"]}
    for extra_char, extra_notes in balance_by_char.items():
        if extra_char not in known_names:
            out.append(f"#### {extra_char}")
            out.extend(extra_notes)
            out.append("")

    out.append(end_marker)
    return "\n".join(out)


def update_readme_changelog(selected_seasons: List[str], versions: Dict[str, dict], dry_run: bool) -> bool:
    if not README_FILE.exists():
        print(f"[!] {README_FILE} not found.")
        return False

    content = README_FILE.read_text(encoding="utf-8")
    orig_content = content

    # If the per-season markers don't exist yet inside CHANGELOG_ENTRIES, initialize all 3 blocks
    if "<!-- SEASON_CHANGELOG_START:" not in content:
        if CHANGELOG_START_MARKER in content and CHANGELOG_END_MARKER in content:
            before, rest = content.split(CHANGELOG_START_MARKER, 1)
            _, after = rest.split(CHANGELOG_END_MARKER, 1)
            all_blocks = "\n\n".join(
                build_season_markdown(sk, versions) for sk in ["buffy", "season-1", "season-2"]
            )
            content = f"{before}{CHANGELOG_START_MARKER}\n{all_blocks}\n{CHANGELOG_END_MARKER}{after}"

    # Update only the selected season block(s)
    for season_key in selected_seasons:
        start_marker = f"<!-- SEASON_CHANGELOG_START:{season_key} -->"
        end_marker = f"<!-- SEASON_CHANGELOG_END:{season_key} -->"
        new_block = build_season_markdown(season_key, versions)
        if start_marker in content and end_marker in content:
            before, rest = content.split(start_marker, 1)
            _, after = rest.split(end_marker, 1)
            content = f"{before}{new_block}{after}"

    if content != orig_content:
        if not dry_run:
            README_FILE.write_text(content, encoding="utf-8")
        return True
    return False


def git_commit_and_push_readme(selected_seasons: List[str], dry_run: bool, no_push: bool) -> None:
    if dry_run:
        print("\n[DRY-RUN] Skipping git commit & push.")
        return

    subprocess.run(
        ["git", "add", "README.md", "update_balance_notes.py"],
        cwd=REPO_DIR,
        check=True,
    )
    diff_cached = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_DIR)
    if diff_cached.returncode == 0:
        print("\n[GIT] No changes in README.md to commit.")
        return

    msg = f"Update balance notes changelog ({', '.join(selected_seasons)})"
    subprocess.run(["git", "commit", "-m", msg], cwd=REPO_DIR, check=True)
    print(f"\n[GIT] Committed: {msg}")

    if not no_push:
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True)
        print("[GIT] Pushed to origin/main.")


def main() -> None:
    valid_seasons = list(SEASON_CONFIG.keys())
    parser = argparse.ArgumentParser(
        description="Manage local per-season balance_notes.md templates and sync season/character changelogs to GitHub README.md."
    )
    parser.add_argument(
        "-s",
        "--season",
        action="append",
        choices=valid_seasons + ["all"],
        help=f"Season(s)/group(s) to sync: {', '.join(valid_seasons)}, or 'all'.",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Sync balance notes for all seasons (buffy, season-1, season-2).",
    )
    parser.add_argument(
        "--init-templates",
        action="store_true",
        help="Create or update local balance_notes.md template files in um_evergreen folders.",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Commit README.md changes locally but do not push to GitHub.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files or pushing.",
    )

    args = parser.parse_args()

    if not args.season and not args.all and not args.init_templates:
        parser.print_help()
        print("\n[!] Specify --season <buffy|season-1|season-2>, --all, or --init-templates.")
        sys.exit(1)

    if args.all or (args.season and "all" in args.season) or (args.init_templates and not args.season):
        selected_seasons = ["buffy", "season-1", "season-2"]
    else:
        selected_seasons = []
        for s in args.season or []:
            if s not in selected_seasons:
                selected_seasons.append(s)

    print(f"Seasons : {', '.join(selected_seasons)}")
    if args.dry_run:
        print("Mode    : DRY RUN")
    print("-" * 72)

    for s in selected_seasons:
        ensure_local_template(s, dry_run=args.dry_run)

    versions = load_versions()
    changed = update_readme_changelog(selected_seasons, versions, dry_run=args.dry_run)
    if changed:
        print("\n[README] Updated season/character changelog in README.md.")
    else:
        print("\n[README] README.md changelog is already up to date.")

    git_commit_and_push_readme(selected_seasons, dry_run=args.dry_run, no_push=args.no_push)


if __name__ == "__main__":
    main()
