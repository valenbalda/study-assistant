import re
from typing import List, Dict


STOPWORDS = {
    "el", "la", "los", "las", "de", "del", "y", "o", "en", "un", "una",
    "para", "por", "con", "que", "se", "es", "son", "a", "al", "lo", "las"
}

TOPIC_HINTS = ("definición", "define", "se define", "consiste", "proceso", "paso", "método", "teorema", "ley", "propiedad")


def _clean_lines(text: str) -> List[str]:
    lines = [l.strip() for l in text.splitlines()]
    return [l for l in lines if l and len(l) > 15]


def _extract_candidates(text: str) -> List[str]:
    lines = _clean_lines(text)
    candidates = []
    for l in lines:
        low = l.lower()
        if any(h in low for h in TOPIC_HINTS) or l.endswith(":"):
            candidates.append(l)
    return candidates if candidates else lines


def _keywords(line: str) -> List[str]:
    tokens = re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ0-9]+", line)
    tokens = [t.lower() for t in tokens if t.lower() not in STOPWORDS and len(t) >= 4]
    seen = set()
    out = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out[:6]


def generate_questions_from_notes(text: str, limit: int = 15) -> List[Dict[str, str]]:
    """
    Genera preguntas simples a partir de apuntes en texto.
    Devuelve lista: {"kind": ..., "topic": ..., "question": ...}
    """
    candidates = _extract_candidates(text)
    questions: List[Dict[str, str]] = []

    for line in candidates:
        kws = _keywords(line)
        if not kws:
            continue

        topic = kws[0]

        questions.append({"kind": "definición", "topic": topic, "question": f"Definí '{topic}' y explicá por qué es importante."})

        if len(kws) >= 2:
            questions.append({"kind": "comparación", "topic": topic, "question": f"Compará '{kws[0]}' vs '{kws[1]}': diferencias y cuándo usar cada uno."})

        questions.append({"kind": "procedimiento", "topic": topic, "question": f"Explicá el procedimiento asociado a '{topic}' paso a paso con un ejemplo."})

        questions.append({"kind": "v/f", "topic": topic, "question": f"Verdadero o falso (justificá): '{topic}' siempre aplica en todos los casos."})

        if len(questions) >= limit:
            break

    return questions[:limit]
