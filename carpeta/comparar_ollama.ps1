# comparar_ollama.ps1

$modelos = @("codestral:latest", "codellama:7b", "gemma3:12b")

$codigo = Get-Content "codigo_tareas.py" -Raw



$prompt = @"
Evalúa el siguiente código fuente en Python con base en los siguientes criterios.
Para cada criterio:
1. Explica tu razonamiento con el detalle que consideres necesario en español.
2. Indica un veredicto estructurado: "Sí" o "No".

Criterios:
• ¿El código es claro y comprensible?
• ¿El código hace lo que se supone que debe hacer?
• ¿Hay suficiente cobertura para las rutas críticas en el código?
• ¿Están bien explicados los algoritmos o decisiones complejos?
• ¿El código está adecuadamente comentado para mayor claridad?
• ¿Existen suposiciones o limitaciones que deban documentarse?
• ¿Podría un marco, API, biblioteca o servicio adicional mejorar la solución?
• ¿Está el código en el nivel de abstracción correcto?
• ¿El código es lo suficientemente modular?
• ¿La solución propuesta está bien diseñada desde una perspectiva de usabilidad?
• ¿El código sigue las convenciones de codificación y la guía de estilo del proyecto (convenciones de nomenclatura, espaciado, sangría, etc.)?
• ¿Hay partes redundantes o innecesarias del código?
• ¿Existe código duplicado que podría refactorizarse en una función/método reutilizable?
• ¿Existen números o cadenas mágicos que deberían ser constantes o configuraciones?
• ¿Las clases, módulos y funciones están bien organizados y tienen el tamaño apropiado?
• ¿Se utilizan los patrones de diseño de forma apropiada y consistente?
• ¿Existe una clara separación de preocupaciones (por ejemplo, UI, lógica empresarial, acceso a datos)?
• ¿Se consideran y gestionan todos los casos extremos?
• ¿Hay algún código muerto o comentado que deba eliminarse?
• ¿Existen declaraciones de depuración o registro que deban eliminarse o ajustarse?
• ¿Existen posibles vulnerabilidades de seguridad introducidas o expuestas en el código?
• ¿Existen problemas de rendimiento o cuellos de botella evidentes?
• ¿Puede simplificarse esta solución?
• ¿Se utiliza un marco, una API, una biblioteca o un servicio que no debería utilizarse?
• ¿Este código se adhiere a los principios de diseño y análisis orientados a objetos, como el principio de responsabilidad única, el principio de apertura-cierre, el principio de sustitución de Liskov, la segregación de interfaz o la inyección de dependencia?
• ¿Se realiza correctamente el manejo de errores?
• ¿Es el código comprobable?

Aquí está el código:

```python
$($codigo)

"@

$resultados = "resultados-comparativa.csv"
"modelo,tiempo_segundos" | Out-File -Encoding utf8 $resultados

function Probar-Modelo($modelo, $prompt) {
$json = @{
model = $modelo
prompt = $prompt
stream = $false
} | ConvertTo-Json -Compress

$tiempo = Measure-Command {
    $response = Invoke-RestMethod -Uri http://localhost:11434/api/generate -Method Post -Body $json -ContentType "application/json"
    $modeloSanitizado = $modelo -replace "[:\\/]", "_"
    $response.response | Out-File "respuesta_$modeloSanitizado.txt" -Encoding utf8
}

"$modelo,$($tiempo.TotalSeconds)" | Out-File -Encoding utf8 -Append $resultados
Write-Host "$([char]0x2705) ${modelo}: $($tiempo.TotalSeconds) segundos"
}

foreach ($modelo in $modelos) {
Probar-Modelo $modelo $prompt
}
