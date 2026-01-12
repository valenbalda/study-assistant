from uuid import uuid4
from datetime import datetime

from storage import load_errors, save_errors
from analytics import top_by, recommendations
from simulator import run_simulacrum


VALID_TYPES = {
    "conceptual",
    "procedure",
    "calculation",
    "reading",
    "distraction",
}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def input_int(prompt: str, min_v: int, max_v: int) -> int:
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
            if min_v <= v <= max_v:
                return v
        except ValueError:
            pass
        print(f"Ingresá un número entre {min_v} y {max_v}.")


def add_error() -> None:
    subject = input("Materia: ").strip()
    topic = input("Tema (ej: derivadas, cuantificadores, RT 54): ").strip()

    print("Tipos posibles: conceptual | procedure | calculation | reading | distraction")
    error_type = input("Tipo de error: ").strip().lower()
    if error_type not in VALID_TYPES:
        print("Tipo inválido. Se guarda como 'conceptual'.")
        error_type = "conceptual"

    severity = input_int("Severidad (1-5): ", 1, 5)
    note = input("Nota (opcional): ").strip()

    errors = load_errors()
    errors.append({
        "id": str(uuid4())[:8],
        "created_at": now_iso(),
        "subject": subject,
        "topic": topic,
        "error_type": error_type,
        "severity": severity,
        "note": note or None,
    })
    save_errors(errors)

    print("\n✅ Error registrado y guardado en data/errors.json.\n")


def list_errors() -> None:
    errors = load_errors()
    if not errors:
        print("\nNo hay errores cargados todavía.\n")
        return

    print("\n=== ERRORES REGISTRADOS ===")
    for e in errors[-10:]:
        print(
            f"- [{e['subject']}] {e['topic']} | "
            f"{e['error_type']} | sev={e['severity']} | {e['created_at']}"
        )
    print("")


def show_dashboard() -> None:
    errors = load_errors()
    print("\n=== DASHBOARD ===")
    print(f"Total de errores: {len(errors)}\n")

    print("Top temas:")
    top_topics = top_by(errors, "topic", n=5)
    if top_topics:
        for k, v in top_topics:
            print(f"- {k}: {v}")
    else:
        print("- (sin datos)")

    print("\nTop tipos de error:")
    top_types = top_by(errors, "error_type", n=5)
    if top_types:
        for k, v in top_types:
            print(f"- {k}: {v}")
    else:
        print("- (sin datos)")

    print("\nRecomendaciones:")
    for r in recommendations(errors):
        print(f"- {r}")
    print("")


def load_notes_text() -> str:
    print("\nApuntes: podés pegar texto y terminar con una línea 'END'.")
    print("O elegir (a) para cargar data/notes/ejemplo_apuntes.txt\n")
    mode = input("Pegás ahora (p) / Cargar archivo (a): ").strip().lower()

    if mode == "p":
        print("Pegá tus apuntes. Escribí END en una línea sola para terminar:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        return "\n".join(lines).strip()

    path = "data/notes/ejemplo_apuntes.txt"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"No encontré {path}. Crealo y probá de nuevo.")
        return ""


def run() -> None:
    while True:
        print("=== Study Assistant ===")
