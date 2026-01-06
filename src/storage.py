import json
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path("data/errors.json")


def ensure_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        DB_PATH.write_text("[]", encoding="utf-8")


def load_errors() -> List[Dict[str, Any]]:
    ensure_db()
    content = DB_PATH.read_text(encoding="utf-8").strip()
    if not content:
        return []
    return json.loads(content)


def save_errors(errors: List[Dict[str, Any]]) -> None:
    ensure_db()
    DB_PATH.write_text(
        json.dumps(errors, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
