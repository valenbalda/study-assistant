# Study Assistant – Python

Asistente de estudio desarrollado en Python que ayuda a identificar patrones de error,
generar simulacros de examen a partir de apuntes y ofrecer recomendaciones de estudio
basadas en el desempeño del estudiante.

---

## Funcionalidades

- Registro de errores por materia, tema y tipo
- Persistencia de datos en archivo JSON
- Dashboard con:
  - temas con mayor cantidad de errores
  - tipos de error más frecuentes
  - recomendaciones automáticas de estudio
- Generación de preguntas desde apuntes en texto
- Simulacro de examen con autoevaluación
- Registro automático de errores durante el simulacro

---

## Enfoque del proyecto

Este proyecto no es un simple organizador de tareas.
Está orientado al **aprendizaje activo**, poniendo el foco en:

- detección de errores reales
- mejora continua
- análisis del desempeño
- simulación de situaciones de examen

---

## Tecnologías utilizadas

- Python 3
- Manejo de archivos (JSON)
- Programación modular
- Análisis básico de datos
- Interfaz por consola

---

## Cómo ejecutar el proyecto

1. Clonar o descargar el repositorio
2. Abrir una terminal en la carpeta raíz
3. Ejecutar:

```bash
python src/main.py
```

---

## Estructura del proyecto

```
study-assistant/
├── src/
│   ├── main.py
│   ├── storage.py
│   ├── analytics.py
│   ├── question_gen.py
│   └── simulator.py
├── data/
│   ├── errors.json
│   └── notes/
│       └── ejemplo_apuntes.txt
└── README.md
```

---

## Autora

Proyecto desarrollado por **Valentina Baldasarre**  
Estudiante de Ingeniería Informática
