from uuid import uuid4
from datetime import datetime

from storage import load_errors, save_errors


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
    for e in errors[-10:]:  # últimos 10
        print(f"- [{e['subject']}] {e['topic']} | {e['error_type']} | sev={e['severity']} | {e['created_at']}")
    print("")


def run() -> None:
    while True:
        print("=== Study Assistant ===")
        print("1) Registrar error")
        print("2) Ver últimos errores")
        print("0) Salir")
        opt = input("Opción: ").strip()

        if opt == "1":
            add_error()
        elif opt == "2":
            list_errors()
        elif opt == "0":
            print("Listo.")
            break
        else:
            print("Opción inválida.\n")


if __name__ == "__main__":
    run()
