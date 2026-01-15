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
        try:
            v = int(input(prompt).strip())
            if min_v <= v <= max_v:
                return v
        except ValueError:
            pass
        print(f"Ingresá un número entre {min_v} y {max_v}.")


def add_error() -> None:
    subject = input("Materia: ").strip()
    topic = input("Tema: ").strip()

    print("Tipos posibles: conceptual | procedure | calculation | reading | distraction")
    error_type = input("Tipo de error: ").strip().lower()
    if error_type not in VALID_TYPES:
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

    print("\n✅ Error registrado.\n")


def list_errors() -> None:
    errors = load_errors()
    if not errors:
        print("\nNo hay errores cargados.\n")
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
    for k, v in top_by(errors, "topic", 5):
        print(f"- {k}: {v}")

    print("\nTop tipos de error:")
    for k, v in top_by(errors, "error_type", 5):
        print(f"- {k}: {v}")

    print("\nRecomendaciones:")
    for r in recommendations(errors):
        print(f"- {r}")
    print("")


def load_notes_text() -> str:
    print("\nApuntes:")
    print("p = pegar texto")
    print("a = usar data/notes/ejemplo_apuntes.txt")
    mode = input("Opción: ").strip().lower()

    if mode == "p":
        print("Pegá el texto. Escribí END para terminar:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        return "\n".join(lines)

    try:
        with open("data/notes/ejemplo_apuntes.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("No se encontró el archivo de apuntes.")
        return ""


def run() -> None:
    while True:
        print("=== Study Assistant ===")
        print("1) Registrar error")
        print("2) Ver últimos errores")
        print("3) Ver dashboard")
        print("4) Hacer simulacro")
        print("0) Salir")

        opt = input("Opción: ").strip()

        if opt == "1":
            add_error()
        elif opt == "2":
            list_errors()
        elif opt == "3":
            show_dashboard()
        elif opt == "4":
            subject = input("Materia: ").strip()
            notes = load_notes_text()
            if notes:
                n = input_int("Cantidad de preguntas (5-20): ", 5, 20)
                run_simulacrum(subject, notes, n)
        elif opt == "0":
            print("Listo.")
            break
        else:
            print("Opción inválida.\n")


if __name__ == "__main__":
    run()
