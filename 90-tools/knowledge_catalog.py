#!/usr/bin/env python3
"""Dynamically inventory engineering knowledge without a hand-maintained catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tomllib

REPO_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_ROOTS = (
    REPO_ROOT / "03.1-engineering-disciplines",
    REPO_ROOT / "03.2-engineering-mechanisms",
    REPO_ROOT / "03.3-engineering-principles",
    REPO_ROOT / "04-architecture-candidates",
)
CARD_TYPES = {"discipline", "mechanism", "principle", "architecture"}


def parse_frontmatter(path: Path) -> dict:
    if path.suffix.lower() != ".md":
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("+++\n"):
        return {}
    end = text.find("\n+++\n", 4)
    if end < 0:
        raise ValueError(f"{path}: opening +++ has no closing +++")
    data = tomllib.loads(text[4:end])
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must be a TOML table")
    return data


def inventory(cards_only: bool = False, type_filter: str | None = None) -> list[dict]:
    missing = [path for path in KNOWLEDGE_ROOTS if not path.is_dir()]
    if missing:
        raise FileNotFoundError("knowledge root(s) not found: " + ", ".join(str(p) for p in missing))

    rows = []
    for root in KNOWLEDGE_ROOTS:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            meta = parse_frontmatter(path)
            card_type = meta.get("type")
            is_card = card_type in CARD_TYPES
            if cards_only and not is_card:
                continue
            if type_filter and card_type != type_filter:
                continue
            rows.append({
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "is_card": is_card,
                "id": meta.get("id"),
                "type": card_type,
                "name": meta.get("name"),
                "status": meta.get("status"),
                "last_reviewed": meta.get("last_reviewed"),
                "metadata": meta,
            })

    rows.sort(key=lambda row: (row["id"] is None, row["id"] or "", row["path"]))
    return rows


def to_markdown(rows: list[dict]) -> str:
    def esc(value: object) -> str:
        if value is None:
            return ""
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "# Dynamic knowledge catalog",
        "",
        f"Files: **{len(rows)}**",
        "",
        "| ID | Type | Name | Status | Path |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        kind = row["type"] or "support"
        lines.append(
            "| "
            + " | ".join([
                esc(row["id"]),
                esc(kind),
                esc(row["name"]),
                esc(row["status"]),
                f"`{esc(row['path'])}`",
            ])
            + " |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--type", choices=tuple(sorted(CARD_TYPES)))
    parser.add_argument("--cards-only", action="store_true")
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()

    try:
        rows = inventory(args.cards_only, args.type)
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"knowledge_catalog: {exc}", file=sys.stderr)
        return 2

    output = (
        to_markdown(rows)
        if args.format == "markdown"
        else json.dumps({
            "knowledge_roots": [path.relative_to(REPO_ROOT).as_posix() for path in KNOWLEDGE_ROOTS],
            "count": len(rows),
            "files": rows,
        }, indent=2) + "\n"
    )

    if args.write:
        target = args.write if args.write.is_absolute() else REPO_ROOT / args.write
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
