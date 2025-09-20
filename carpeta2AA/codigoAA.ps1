# comparar_por_pregunta.ps1

$modelos = @("codestral:latest", "codellama:7b", "gemma3:12b")
$codigo = Get-Content "codigo_tareasAA.py" -Raw
$preguntas = Get-Content "preguntas.txt"
$resultados = "resultados_por_pregunta.csv"

if (-not (Test-Path "respuestas")) {
    New-Item -ItemType Directory -Path "respuestas" | Out-Null
}

"modelo,pregunta,tiempo_segundos" | Out-File -Encoding utf8 $resultados

function Probar-Pregunta($modelo, $pregunta, $codigo) {
    $prompt = @"
Responde solo con 'Sí', 'No' o 'No aplica' a la siguiente pregunta sobre este código:

$pregunta

```python
$codigo
"@ 

$json = @{
    model = $modelo
    prompt = $prompt
    stream = $false
} | ConvertTo-Json -Compress

$safeName = ($pregunta.Substring(0, [Math]::Min(30, $pregunta.Length)) -replace '[^a-zA-Z0-9]', '')
$modeloSanitizado = $modelo -replace '[:\\/]', '_'
if ([string]::IsNullOrWhiteSpace($safeName)) { $safeName = "pregunta" }
$rutaArchivo = Join-Path "respuestas" ("$modeloSanitizado-$safeName.txt")

$tiempo = Measure-Command {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" `
                                  -Method Post -Body $json -ContentType "application/json"
    $response.response | Out-File -FilePath $rutaArchivo -Encoding utf8
}

"$modelo,`"$pregunta`",$([math]::Round($tiempo.TotalSeconds,2))" | Out-File -Encoding utf8 -Append $resultados
Write-Host "$([char]0x2705) ${modelo} - $safeName`:` $([math]::Round($tiempo.TotalSeconds,2)) segundos"


}

foreach ($modelo in $modelos) {
foreach ($pregunta in $preguntas) {
Probar-Pregunta $modelo $pregunta $codigo
}
}

Write-Host "`nTiempos guardados en $resultados"