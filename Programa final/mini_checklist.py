import requests
import json
import csv
from pathlib import Path

# ==============================
# CONFIG
# ==============================
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma3:12b"    # El modelo elegido
CHECKLIST_FILE = "preguntas.txt"
CODE_FILE = "codigo_tareas.py"
OUTPUT_FILE = "resultados_final.csv"

PROMPT_TEMPLATE = """Responde solo con 'Sí', 'No' o 'No aplica' a la siguiente pregunta sobre este código:

Pregunta:
{pregunta}

Código:
```python
{codigo}

Responde ÚNICAMENTE con: Sí | No | No aplica
"""

def load_file(path: str) -> str:
    """Lee un archivo de texto y devuelve su contenido como string."""
    return Path(path).read_text(encoding="utf-8")

def ask_ollama(model: str, prompt: str) -> str:
    """Envía prompt a Ollama y devuelve la respuesta del LLM."""
    payload = {"model": model, "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, data=json.dumps(payload))
    response.raise_for_status()
    return response.json().get("response", "").strip()

def main():
    codigo = load_file(CODE_FILE)
    preguntas = [p.strip() for p in load_file(CHECKLIST_FILE).splitlines() if p.strip()]

    resultados = []

    for i, pregunta in enumerate(preguntas, 1):
        prompt = PROMPT_TEMPLATE.format(pregunta=pregunta, codigo=codigo)
        print(f"[{i}/{len(preguntas)}] {pregunta}")

    
        try:
            respuesta = ask_ollama(DEFAULT_MODEL, prompt)
        except Exception as e:
            respuesta = f"ERROR: {e}"
    

        print(f" -> {respuesta}\n")

        resultados.append({"pregunta": pregunta, "respuesta": respuesta})

    # Guardar en CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["pregunta", "respuesta"])
        writer.writeheader()
        writer.writerows(resultados)

    print(f"\n📊 Resultados guardados en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()