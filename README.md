# validation-LLM-checklist
Evaluación de modelos de lenguaje (Codellama, Codestral y Gemma) en tareas de validación estática de código mediante checklist. Incluye informe en LaTeX, gráficos y scripts de análisis en Python.

# Validación de LLMs con Checklist de Código

Este repositorio contiene el trabajo de evaluación de modelos de lenguaje (Codellama, Codestral y Gemma) aplicados a la **validación estática de código** a través de una **checklist de calidad de software**.

## Contenido
- `informe.tex` → Documento principal en LaTeX.  
- `figures/` → Gráficas generadas a partir de los resultados.  
- `scripts/` → Scripts en Python para procesar datos y crear las figuras.  
- `data/` → CSV y datasets usados en la evaluación.  

## Objetivos
- Reducir el esfuerzo manual en la validación de software.  
- Disminuir el margen de error humano.  
- Aportar retroalimentación rápida y contextualizada al desarrollador.  
- Comparar el rendimiento de distintos LLMs en tareas de revisión por checklist.  

## Resultados
- **Gemma** se presenta como el modelo más fiable y consistente, ideal como sustituto de la validación humana.  
- **Codellama** es el más rápido, aunque inestable y con menor precisión.  
- **Codestral** ocupa un punto intermedio, con un rendimiento aceptable pero variable.  

## Cómo reproducir
1. Compilar el informe en LaTeX (`informe.tex`).  
2. Ejecutar los scripts de Python en `scripts/` para generar las figuras.  

---
