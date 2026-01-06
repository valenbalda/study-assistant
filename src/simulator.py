import random
from uuid import uuid4
from datetime import datetime
from typing import Set

from storage import load_errors, save_errors
from question_gen import generate_questions_from_notes


VALID_ERROR_TYPES: Set[str] = {"conceptual", "procedure", "calculation", "reading", "distraction"}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def run_simulacrum(subject: str, notes_text: str, n_questions: int = 10) -> None:
    questions = generate_questions_from_notes(notes_text, limit=max(15, n_questions))
    if not questions:
        print("No pude generar preguntas. Pegá apuntes más largos o con definiciones/procesos.")
        return

    chosen = random.sample(questions, k=min(n_questions, len(questions)))
    errors = load_errors()

    print("\n=== SIMULACRO ===")
    print(f"Materia: {subject} | Preguntas: {len(chosen)}")
    print("Autoevaluación: 1=la respondí bien, 0=fallé / dudé mucho.\n")

    for i, q in enumerate(chosen, 1):
        print(f"[{i}] ({q['kind']}) Tema: {q['topic']}")
        print(q["question"])
        ans = input("¿Bien (1) / Mal (0)? ").strip()

        if ans == "0":
            errors.append({
                "id": str(uuid4())[:8],
                "created_at": now_iso(),
                "subject": subject,
                "topic": q["topic"],
                "error_type": "conceptual",
                "severity": 3,
                "note": "Registrado desde simulacro (fallé o dudé).",
            })
            print("-> Registré un error conceptual (sev=3). Luego podés editarlo si querés.\n")
        else:
            print("-> OK.\n")

    save_errors(errors)
    print("Simulacro finalizado. Errores guardados en data/errors.json.\n")
