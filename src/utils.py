from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable


def ensure_parent_dir(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def read_jsonl(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []

    rows: list[dict] = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: str | Path, rows: Iterable[dict]) -> None:
    ensure_parent_dir(path)
    with Path(path).open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def stable_id(prefix: str, text: str) -> str:
    digest = hashlib.md5(text.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"

