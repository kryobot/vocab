#!/usr/bin/env python3
"""Validates all vocabulary lists in listen/ and writes manifest.json.

Run locally with `python3 scripts/build_manifest.py` or let the GitHub Action do it.
Exits with an error (and the GitHub Action turns red) if a list has mistakes.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIST_DIR = ROOT / "listen"
KNOWN_KEYS = {"title", "from", "to", "profiles"}


def strip_comment(line: str) -> str:
    match = re.search(r"[ \t]#", line)
    return line[: match.start()] if match else line


def clean(text: str) -> str:
    return " ".join(text.split())


def parse(path: Path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = text.split("\n")
    meta = {"title": path.stem, "from": "de", "to": "en", "profiles": []}
    errors, entries, seen = [], [], {}
    i = 0

    if lines and lines[0].strip() == "---":
        i = 1
        closed = False
        while i < len(lines):
            line = lines[i].strip()
            i += 1
            if line == "---":
                closed = True
                break
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                errors.append(f"Zeile {i}: unbekannte Kopfzeile „{line}“")
                continue
            key, value = line.split(":", 1)
            key, value = key.strip().lower(), strip_comment(value).strip()
            if key not in KNOWN_KEYS:
                errors.append(f"Zeile {i}: unbekannter Schlüssel „{key}“ (erlaubt: {', '.join(sorted(KNOWN_KEYS))})")
            elif key == "profiles":
                meta["profiles"] = [p.strip() for p in value.strip("[] ").split(",") if p.strip()]
            elif value:
                meta[key] = value if key == "title" else value.lower()
        if not closed:
            errors.append("Kopfbereich wird nicht mit --- abgeschlossen")

    while i < len(lines):
        number = i + 1
        line = lines[i].strip()
        i += 1
        if not line or line.startswith("#"):
            continue
        line = strip_comment(line)
        pair, _, hint = line.partition("|")
        if "=" not in pair:
            errors.append(f"Zeile {number}: kein „=“ gefunden: „{line}“")
            continue
        front, back = (clean(p) for p in pair.split("=", 1))
        if not front or not back:
            errors.append(f"Zeile {number}: Vorder- oder Rückseite ist leer")
            continue
        key = clean(front).lower()
        if key in seen:
            errors.append(f"Zeile {number}: „{front}“ steht schon in Zeile {seen[key]}")
            continue
        seen[key] = number
        entries.append((front, back, clean(hint)))

    if not entries:
        errors.append("Die Liste enthält keine Vokabeln")
    return text, meta, entries, errors


def main() -> int:
    lists, problems = [], []
    for path in sorted(LIST_DIR.rglob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        text, meta, entries, errors = parse(path)
        problems += [f"{relative}: {e}" for e in errors]
        lists.append({
            "id": path.relative_to(LIST_DIR).with_suffix("").as_posix(),
            "path": relative,
            "title": meta["title"],
            "from": meta["from"],
            "to": meta["to"],
            "profiles": meta["profiles"],
            "count": len(entries),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        })

    if problems:
        print("Fehler in den Vokabellisten:\n")
        print("\n".join(f"  ✗ {p}" for p in problems))
        return 1

    manifest = {
        "version": 1,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lists": lists,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(item["count"] for item in lists)
    print(f"✓ {len(lists)} Listen mit {total} Vokabeln → manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
