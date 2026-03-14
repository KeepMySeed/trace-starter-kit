#!/usr/bin/env python3
"""Very small starter utility to generate a lightweight repo map.

This is intentionally simple. It scans the repository, collects file paths,
and records basic metadata. Teams can later replace it with a richer indexer
that extracts symbols, imports, ownership, or AST-level relationships.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "trace" / "graph" / "repo_map.json"
EXCLUDED_DIRS = {".git", "node_modules", "dist", "coverage", "__pycache__", ".venv", "venv"}
EXCLUDED_PREFIXES = {str((ROOT / "trace" / "graph").resolve())}


def should_skip(path: Path) -> bool:
    path_str = str(path.resolve())
    if any(path_str.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return True
    return any(part in EXCLUDED_DIRS for part in path.parts)


files = []
for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    if should_skip(path):
        continue
    rel = path.relative_to(ROOT)
    files.append(
        {
            "path": str(rel).replace("\\", "/"),
            "suffix": path.suffix,
            "size": path.stat().st_size,
        }
    )

repo_map = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "root": ROOT.name,
    "files": sorted(files, key=lambda item: item["path"]),
    "modules": [],
    "symbols": [],
    "dependencies": [],
    "notes": "Starter-level repo map. Extend this script to extract symbols and ownership.",
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(repo_map, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUTPUT}")
