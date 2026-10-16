# CONFIGURACIÓN: parámetros de esta ejecución; no modifica variables globales.
[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
param(
    [ValidateSet('Diagnose', 'Recover', 'Compare', 'Install')]
    [string]$Action = 'Diagnose',
    [string]$RepositoryPath = (Join-Path $HOME 'Proyectos/automatizacion-bim'),
    [string]$CodexHome,
    [string[]]$SkillNames = @(),
    [switch]$Update,
    [switch]$Apply,
    [switch]$LibraryOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepositoryUrl = 'https://github.com/Juanca0795/automatizacion-bim.git'

function Resolve-CodexHome {
    param([string]$ExplicitPath)
    if ($ExplicitPath) { return [IO.Path]::GetFullPath($ExplicitPath) }
    if ($env:CODEX_HOME) { return [IO.Path]::GetFullPath($env:CODEX_HOME) }
    return Join-Path $HOME '.codex'
}

function Assert-NoLink {
    param([string]$Path)
    $current = [IO.Path]::GetFullPath($Path)
    while ($current) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "No se siguen enlaces o junctions: $current"
            }
        }
        $parent = Split-Path -Parent $current
        if ($parent -eq $current) { break }
        $current = $parent
    }
}

function Get-SkillManifest {
    param([string]$Path)
    Assert-NoLink $Path
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) { return @{} }
    $manifest = @{}
    # Recorrer sin seguir enlaces y excluir autenticación/configuración de Codex.
    $pending = [Collections.Generic.Queue[string]]::new()
    $pending.Enqueue([IO.Path]::GetFullPath($Path))
    while ($pending.Count) {
        $directory = $pending.Dequeue()
        foreach ($item in Get-ChildItem -LiteralPath $directory -Force) {
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Enlace no permitido: $($item.FullName)"
            }
            $relative = $item.FullName.Substring([IO.Path]::GetFullPath($Path).TrimEnd('\','/').Length + 1).Replace('\','/')
            if ($relative -notmatch '^(SKILL\.md|agents(/.*)?|references(/.*)?)$' -or
                $item.Name -match '(?i)(^\.env|auth|token|credential|secret|password|\.pem$|\.key$)') {
                throw "Archivo o directorio fuera del contenido permitido; revisar manualmente: $relative"
            }
            if ($item.PSIsContainer) { $pending.Enqueue($item.FullName) }
            else { $manifest[$relative] = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash }
        }
    }
    return $manifest
}

function Compare-Skill {
    param([string]$Source, [string]$Destination)
    $left = Get-SkillManifest $Source
    $right = Get-SkillManifest $Destination
    foreach ($name in @(@($left.Keys) + @($right.Keys) | Sort-Object -Unique)) {
        $state = if (-not $left.ContainsKey($name)) { 'LocalOnly' }
                 elseif (-not $right.ContainsKey($name)) { 'Missing' }
                 elseif ($left[$name] -ne $right[$name]) { 'Different' }
                 else { 'Equal' }
        [pscustomobject]@{ File = $name; State = $state }
    }
}

function Invoke-RepositoryGit {
    param([string]$Path, [string[]]$Arguments)
    $result = & git -C $Path @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Git falló: $($Arguments -join ' '). Revisar localmente sin mostrar credenciales." }
    return $result
}

function Assert-Repository {
    param([string]$Path)
    Assert-NoLink $Path
    $top = [string](Invoke-RepositoryGit $Path @('rev-parse','--show-toplevel'))
    if ([IO.Path]::GetFullPath($top).TrimEnd('\','/') -ne [IO.Path]::GetFullPath($Path).TrimEnd('\','/')) {
        throw 'La ruta debe ser la raíz exacta del repositorio.'
    }
    $remote = [string](Invoke-RepositoryGit $Path @('remote','get-url','origin'))
    if ($remote -notmatch '^(https://github\.com/Juanca0795/automatizacion-bim(?:\.git)?|git@github\.com:Juanca0795/automatizacion-bim(?:\.git)?)$') {
        throw 'Origin no corresponde al repositorio autorizado.'
    }
}

function Get-EnvironmentReport {
    foreach ($tool in @('git','python','node','npm','codex')) {
        $command = Get-Command $tool -ErrorAction SilentlyContinue
        $version = 'No detectado en PATH'
        if ($command) {
            try {
                $output = & $tool --version 2>&1
                $version = if ($LASTEXITCODE -eq 0) { ($output | Select-Object -First 1).ToString() } else { 'No se pudo consultar versión' }
            } catch { $version = 'Consulta fallida; comprobar manualmente' }
        }
        [pscustomobject]@{ Component = $tool; Version = $version }
    }
    $registered = @()
    foreach ($key in @('HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
                       'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
                       'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*')) {
        $registered += @(Get-ItemProperty $key -ErrorAction SilentlyContinue)
    }
    foreach ($product in @('QGIS','Civil 3D','Revit','Dynamo')) {
        $matches = @($registered | Where-Object { $_.PSObject.Properties['DisplayName'] -and $_.DisplayName -like "*$product*" })
        if (-not $matches.Count) {
            [pscustomobject]@{ Component = $product; Version = 'No detectado en registro; comprobar anfitrión/instalación manualmente' }
        }
        foreach ($entry in $matches) {
            $version = if ($entry.PSObject.Properties['DisplayVersion']) { $entry.DisplayVersion } else { 'Versión no registrada' }
            [pscustomobject]@{ Component = $entry.DisplayName; Version = $version }
        }
    }
}

# EJECUCIÓN: sin -Apply solo informa; -WhatIf nunca escribe.
if ($LibraryOnly) { return }
$RepositoryPath = [IO.Path]::GetFullPath($RepositoryPath)
$skillsRoot = Join-Path (Resolve-CodexHome $CodexHome) 'skills'
if ($Action -eq 'Diagnose') {
    Get-EnvironmentReport
    Write-Output "Codex home resuelto: $(Resolve-CodexHome $CodexHome)"
    Write-Output "Repositorio: $RepositoryPath"
    if (Test-Path -LiteralPath $skillsRoot -PathType Container) {
        Get-ChildItem -LiteralPath $skillsRoot -Directory | Select-Object Name
    }
    return
}
if ($Action -eq 'Recover') {
    Assert-NoLink $RepositoryPath
    if (-not (Test-Path -LiteralPath $RepositoryPath)) {
        Write-Output "Propuesto: clonar $RepositoryUrl en $RepositoryPath"
        if ($Apply -and $PSCmdlet.ShouldProcess($RepositoryPath, 'Clonar repositorio BIM')) {
            $parent = Split-Path -Parent $RepositoryPath
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
            & git clone -- $RepositoryUrl $RepositoryPath
            if ($LASTEXITCODE -ne 0) { throw 'Clonado fallido; revisar destino parcial, sin borrarlo automáticamente.' }
        }
        return
    }
    Assert-Repository $RepositoryPath
    $status = @(Invoke-RepositoryGit $RepositoryPath @('status','--porcelain'))
    if ($status.Count) { throw 'Hay cambios locales; no se actualizará. Revisar git status.' }
    if (-not $Update) { Write-Output 'Repositorio existente y limpio. Usar -Update para proponer actualización.'; return }
    $branch = [string](Invoke-RepositoryGit $RepositoryPath @('symbolic-ref','--short','HEAD'))
    $upstream = [string](Invoke-RepositoryGit $RepositoryPath @('rev-parse','--abbrev-ref','@{upstream}'))
    if ($upstream -ne "origin/$branch") { throw 'Upstream inesperado; resolver manualmente.' }
    Write-Output "Propuesto: actualizar $branch mediante fast-forward desde origin."
    if ($Apply -and $PSCmdlet.ShouldProcess($RepositoryPath, 'Actualizar con git pull --ff-only')) {
        Invoke-RepositoryGit $RepositoryPath @('pull','--ff-only','origin',$branch)
    }
    return
}
Assert-Repository $RepositoryPath
$sourceRoot = Join-Path $RepositoryPath '07-documentacion/skills-codex'
Assert-NoLink $sourceRoot
if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) { throw 'No existe el directorio de skills versionadas.' }
if (-not $SkillNames.Count) { $SkillNames = @(Get-ChildItem -LiteralPath $sourceRoot -Directory | Select-Object -ExpandProperty Name) }
foreach ($name in $SkillNames) {
    if ($name -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$') { throw "Nombre de skill inválido: $name" }
    $source = Join-Path $sourceRoot $name
    $destination = Join-Path $skillsRoot $name
    if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md') -PathType Leaf)) { throw "Falta SKILL.md en $name" }
    $comparison = @(Compare-Skill $source $destination)
    $comparison | Select-Object @{n='Skill';e={$name}}, File, State
    if ($Action -ne 'Install') { continue }
    if (Test-Path -LiteralPath $destination) {
        if (@($comparison | Where-Object State -ne 'Equal').Count) {
            Write-Warning "$name ya existe y difiere. No se reemplaza ni combina; revisar archivos y obtener aprobación específica."
        }
        continue
    }
    if ($Apply -and $PSCmdlet.ShouldProcess($destination, 'Instalar skill faltante')) {
        Assert-NoLink $skillsRoot
        # Crear sin -Force para impedir sobrescribir un destino aparecido durante la revisión.
        New-Item -ItemType Directory -Path $destination -ErrorAction Stop | Out-Null
        foreach ($file in Get-ChildItem -LiteralPath $source -Force) {
            Copy-Item -LiteralPath $file.FullName -Destination $destination -Recurse -ErrorAction Stop
        }
        $remaining = @(Compare-Skill $source $destination | Where-Object State -ne 'Equal')
        if ($remaining.Count) { throw "La verificación de $name falló; revisar instalación parcial sin eliminarla automáticamente." }
        Write-Output "Verificada: $name"
    }
}
