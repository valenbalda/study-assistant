from collections import Counter
from typing import List, Dict, Any, Tuple


def top_by(errors: List[Dict[str, Any]], key: str, n: int = 5) -> List[Tuple[str, int]]:
    c = Counter(
        str(e.get(key, "")).strip().lower()
        for e in errors
        if e.get(key)
    )
    return c.most_common(n)


def recommendations(errors: List[Dict[str, Any]]) -> List[str]:
    if not errors:
        return ["No hay errores registrados todavía. Cargá 5–10 errores reales para que el sistema pueda ayudarte."]

    type_counts = Counter(e.get("error_type") for e in errors if e.get("error_type"))
    topic_counts = Counter(str(e.get("topic", "")).strip().lower() for e in errors if e.get("topic"))

    recs: List[str] = []

    # Reglas simples pero útiles
    if type_counts.get("conceptual", 0) >= 3:
        recs.append("Muchos errores conceptuales: repasá teoría y hacé preguntas tipo oral (active recall).")
    if type_counts.get("calculation", 0) >= 3:
        recs.append("Muchos errores de cálculo: resolvé sets cortos cronometrados y revisá unidades/pasos.")
    if type_counts.get("procedure", 0) >= 3:
        recs.append("Errores de procedimiento: armá checklist de pasos y resolvé 3 ejercicios similares seguidos.")
    if type_counts.get("reading", 0) >= 2:
        recs.append("Errores de lectura: reescribí el enunciado en tus palabras y marcá datos clave.")
    if type_counts.get("distraction", 0) >= 2:
        recs.append("Distracciones: probá Pomodoro 25/5 y 1 objetivo por bloque.")

    # Tema más débil
    if topic_counts:
        top_topic, cnt = topic_counts.most_common(1)[0]
        recs.append(f"Tu tema más débil hoy es '{top_topic}' (errores: {cnt}). Hacé un mini-simulacro de ese tema.")

    if not recs:
        recs.append("Vas bien: seguí registrando errores y hacé repasos espaciados de los temas donde fallás.")

    return recs
