# comparar_ollama_bloques.ps1

$modelos = @("codestral:latest", "codellama:7b", "gemma3:12b")

$codigo = Get-Content "codigo_tareasAA.py" -Raw

# Todas las preguntas del checklist
$preguntas = @(
    "¿El código es claro y comprensible?",
    "¿El código hace lo que se supone que debe hacer?",
    "¿Hay suficiente cobertura para las rutas críticas en el código?",
    "¿Están bien explicados los algoritmos o decisiones complejos?",
    "¿El código está adecuadamente comentado para mayor claridad?",
    "¿Existen suposiciones o limitaciones que deban documentarse?",
    "¿Podría un marco, API, biblioteca o servicio adicional mejorar la solución?",
    "¿Está el código en el nivel de abstracción correcto?",
    "¿El código es lo suficientemente modular?",
    "¿La solución propuesta está bien diseñada desde una perspectiva de usabilidad?",
    "¿El código sigue las convenciones de codificación y la guía de estilo del proyecto (convenciones de nomenclatura, espaciado, sangría, etc.)?",
    "¿Hay partes redundantes o innecesarias del código?",
    "¿Existe código duplicado que podría refactorizarse en una función/método reutilizable?",
    "¿Existen números o cadenas mágicos que deberían ser constantes o configuraciones?",
    "¿Las clases, módulos y funciones están bien organizados y tienen el tamaño apropiado?",
    "¿Se utilizan los patrones de diseño de forma apropiada y consistente?",
    "¿Existe una clara separación de preocupaciones (por ejemplo, UI, lógica empresarial, acceso a datos)?",
    "¿Se consideran y gestionan todos los casos extremos?",
    "¿Hay algún código muerto o comentado que deba eliminarse?",
    "¿Existen declaraciones de depuración o registro que deban eliminarse o ajustarse?",
    "¿Existen posibles vulnerabilidades de seguridad introducidas o expuestas en el código?",
    "¿Existen problemas de rendimiento o cuellos de botella evidentes?",
    "¿Puede simplificarse esta solución?",
    "¿Se utiliza un marco, una API, una biblioteca o un servicio que no debería utilizarse?",
    "¿Este código se adhiere a los principios de diseño y análisis orientados a objetos, como el principio de responsabilidad única, el principio de apertura-cierre, el principio de sustitución de Liskov, la segregación de interfaz o la inyección de dependencia?",
    "¿Se realiza correctamente el manejo de errores?",
    "¿Es el código comprobable?"
)

# Dividir preguntas en bloques de 10
$bloques = $preguntas | ForEach-Object -Begin { $i = 0 } -Process {
    [PSCustomObject]@{ Grupo = [math]::Floor($i / 10); Pregunta = $_ }
    $i++
} | Group-Object Grupo

$resultados = "resultados-comparativa.csv"
"modelo,bloque,tiempo_segundos" | Out-File -Encoding utf8 $resultados

function Probar-Modelo($modelo, $codigo, $bloque, $idBloque) {
    $listaPreguntas = ($bloque | ForEach-Object { "• " + $_ }) -join "`n"

    $prompt = @"
Evalúa el siguiente código fuente en Python con base en los siguientes criterios.
Por cada criterio:
1. Explica tu razonamiento con el detalle que consideres necesario.
2. Indica un veredicto estructurado: "Sí", "No" o "No aplica".

Criterios:
$listaPreguntas

Aquí está el código:

```python
$($codigo)

"@

$json = @{
    model = $modelo
    prompt = $prompt
    stream = $false
} | ConvertTo-Json -Compress

$tiempo = Measure-Command {
    $response = Invoke-RestMethod -Uri http://localhost:11434/api/generate `
                                  -Method Post -Body $json `
                                  -ContentType "application/json"
    $modeloSanitizado = $modelo -replace "[:\\/]", "_"
    $response.response | Out-File "respuesta_${modeloSanitizado}_bloque$idBloque.txt" -Encoding utf8
}

"$modelo,$idBloque,$($tiempo.TotalSeconds)" | Out-File -Encoding utf8 -Append $resultados
Write-Host "$([char]0x2705) ${modelo} - bloque ${idBloque}: $($tiempo.TotalSeconds) segundos"

}

foreach ($modelo in $modelos) {
$idBloque = 1
foreach ($bloque in $bloques) {
Probar-Modelo $modelo $codigo ($bloque.Group.Pregunta) $idBloque
$idBloque++
}
}

Write-Host "`nResultados guardados en $resultados"
