# CONFIGURACIÓN
param([string]$ScriptPath = (Join-Path $PSScriptRoot '../Entorno-Bim.ps1'))
$ErrorActionPreference = 'Stop'
$ScriptPath = (Resolve-Path -LiteralPath $ScriptPath).Path
$testRoot = Join-Path ([IO.Path]::GetTempPath()) ('bim-setup-test-' + [guid]::NewGuid())

function Assert-True($Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}

# EJECUCIÓN: fixtures aislados; no instala en Codex ni usa la red.
$tokens = $null
$errors = $null
[void][Management.Automation.Language.Parser]::ParseFile($ScriptPath, [ref]$tokens, [ref]$errors)
Assert-True (-not $errors.Count) 'Sintaxis PowerShell inválida.'
. $ScriptPath -LibraryOnly
New-Item -ItemType Directory -Path $testRoot | Out-Null
$source = Join-Path $testRoot 'Usuario distinto/Proyecto con espacios/skill'
$destination = Join-Path $testRoot 'Otro usuario/Codex personalizado/skills/skill'
New-Item -ItemType Directory -Path (Join-Path $source 'agents') -Force | Out-Null
Set-Content -LiteralPath (Join-Path $source 'SKILL.md') -Value 'contenido de prueba'
Set-Content -LiteralPath (Join-Path $source 'agents/openai.yaml') -Value 'interface: {}'
$missing = @(Compare-Skill $source $destination)
Assert-True ($missing.Count -eq 2 -and @($missing | Where-Object State -ne 'Missing').Count -eq 0) 'Clasificación de destino faltante.'
Assert-True (-not (Test-Path -LiteralPath $destination)) 'Comparar creó el destino.'
New-Item -ItemType Directory -Path $destination -Force | Out-Null
Get-ChildItem -LiteralPath $source -Force | Copy-Item -Destination $destination -Recurse
$equal = @(Compare-Skill $source $destination)
Assert-True (@($equal | Where-Object State -ne 'Equal').Count -eq 0) 'Archivos idénticos clasificados incorrectamente.'
Set-Content -LiteralPath (Join-Path $destination 'SKILL.md') -Value 'personalizado'
Set-Content -LiteralPath (Join-Path $destination 'references-local.md') -Value 'conservar'
$rejected = $false
try { $null = Compare-Skill $source $destination } catch { $rejected = $true }
Assert-True $rejected 'Debe rechazar contenido fuera del manifiesto permitido.'
# Usar otro fixture para las diferencias permitidas, sin borrar el anterior.
$destination = Join-Path $testRoot 'Perfil alternativo/skills/skill'
New-Item -ItemType Directory -Path $destination -Force | Out-Null
Get-ChildItem -LiteralPath $source -Force | Copy-Item -Destination $destination -Recurse
Set-Content -LiteralPath (Join-Path $destination 'SKILL.md') -Value 'personalizado'
New-Item -ItemType Directory -Path (Join-Path $destination 'references') | Out-Null
Set-Content -LiteralPath (Join-Path $destination 'references/local.md') -Value 'conservar'
$different = @(Compare-Skill $source $destination)
Assert-True (@($different | Where-Object State -eq 'Different').Count -eq 1) 'No detectó personalización.'
Assert-True (@($different | Where-Object State -eq 'LocalOnly').Count -eq 1) 'No detectó archivo local extra.'
$before = (Get-FileHash -LiteralPath (Join-Path $destination 'SKILL.md')).Hash
$null = Compare-Skill $source $destination
Assert-True ($before -eq (Get-FileHash -LiteralPath (Join-Path $destination 'SKILL.md')).Hash) 'Comparar modificó archivos.'
Set-Content -LiteralPath (Join-Path $source 'agents/auth.json') -Value '{}'
$rejected = $false
try { $null = Get-SkillManifest $source } catch { $rejected = $true }
Assert-True $rejected 'Debe rechazar archivos de autenticación.'
foreach ($path in @('D:\Usuarios\Ana Maria\Codex', 'E:\BIM\skills', (Join-Path $testRoot 'otro usuario'))) {
    Assert-True ((Resolve-CodexHome $path) -eq [IO.Path]::GetFullPath($path)) 'No respeta ruta configurable.'
}
$repoMissing = Join-Path $testRoot 'Repositorio ausente'
& $ScriptPath -Action Recover -RepositoryPath $repoMissing
Assert-True (-not (Test-Path -LiteralPath $repoMissing)) 'Vista previa de clonado creó archivos.'
& $ScriptPath -Action Recover -RepositoryPath $repoMissing -Apply -WhatIf
Assert-True (-not (Test-Path -LiteralPath $repoMissing)) 'WhatIf creó archivos.'
Write-Output "APROBADO: sintaxis, ausentes/iguales/diferentes/extra, no sobrescritura, rechazo de auth, rutas D/E y vista previa/WhatIf. Fixtures: $testRoot"
