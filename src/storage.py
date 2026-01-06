import json
from pathlib import Path

DB_PATH = Path("data/errors.json")


def ensure_db() -> None:
    """Asegura que exista data/errors.json (si no existe, lo crea como lista vacía)."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        DB_PATH.write_text("[]", encoding="utf-8")


def load_errors() -> list[dict]:
    """Carga la lista de errores desde el JSON."""
    ensure_db()
    content = DB_PATH.read_text(encoding="utf-8").strip()
    if not content:
        return []
    return json.loads(content)


def save_errors(errors: list[dict]) -> None:
    """Guarda la lista de errores en el JSON."""
    ensure_db()
    DB_PATH.write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
