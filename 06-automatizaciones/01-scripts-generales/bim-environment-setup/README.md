# Recuperación del entorno BIM en Windows

Diagnosticar herramientas, recuperar exclusivamente `Juanca0795/automatizacion-bim` y comparar/instalar skills versionadas. No instala aplicaciones ni copia la configuración completa de Codex. La fuente de las skills es `07-documentacion/skills-codex/`; los scripts se mantienen aquí, sin duplicarlos en las skills.

## Requisitos y configuración

Windows y PowerShell 7 para este procedimiento; Git para recuperación/comparación/instalación desde el repositorio. No se requiere Python para ejecutar el script. Las aplicaciones BIM, sus licencias, paquetes y motores se configuran manualmente según cada proyecto. Las pruebas de esta entrega se realizaron en la sesión local, no en otra PC. Windows PowerShell 5.1 no está verificado.

Parámetros al inicio de `Entorno-Bim.ps1`: `RepositoryPath` (por defecto `$HOME/Proyectos/automatizacion-bim`), `CodexHome`, `SkillNames`, `Action`, `Update` y `Apply`. No depende del nombre del equipo ni del usuario. `CodexHome` explícito tiene prioridad sobre `CODEX_HOME`; si ninguno existe usa `$HOME/.codex`, incluso si aún no se ha creado. La ruta del ejecutable Codex no identifica por sí sola su directorio de datos. Revisar el resultado si hay varios perfiles; no buscar ni leer credenciales.

## Recuperar en otra PC

Primero instalar manualmente Git/PowerShell si faltan. Elegir carpeta de proyectos y clonar solo tras revisar y autorizar el destino. Si ya existe, no repetir el clonado; ejecutar `git -C $REPOSITORIO status` y verificar origin antes de continuar. No descargar y ejecutar scripts directamente desde la web.

```powershell
# CONFIGURACIÓN: cambiar esta carpeta si se desea otra unidad o ubicación.
$CARPETA_PROYECTOS = Join-Path $HOME 'Proyectos'
$REPOSITORIO = Join-Path $CARPETA_PROYECTOS 'automatizacion-bim'

# EJECUCIÓN: solo para repositorio ausente y tras autorizar este clonado.
if (Test-Path -LiteralPath $REPOSITORIO) { throw 'Destino existente; revisar antes de continuar.' }
New-Item -ItemType Directory -Path $CARPETA_PROYECTOS -Force | Out-Null
git clone -- https://github.com/Juanca0795/automatizacion-bim.git $REPOSITORIO
if ($LASTEXITCODE -ne 0) { throw 'Clonado fallido; revisar destino parcial sin borrarlo.' }
```

Los archivos nuevos deben haberse publicado con autorización para estar disponibles al clonar. Esta entrega no realiza commits ni push. Git recupera los directorios versionados: no se crean carpetas vacías para aplicaciones aún sin proyectos. No reconstruir una carpeta borrada sobre trabajo local; revisar y aprobar esa restauración por separado.

Desde el clon revisado, usar:

```powershell
# CONFIGURACIÓN
$REPOSITORIO = Join-Path $HOME 'Proyectos/automatizacion-bim'
$SCRIPT = Join-Path $REPOSITORIO '06-automatizaciones/01-scripts-generales/bim-environment-setup/Entorno-Bim.ps1'
$CODEX_DATOS = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$SKILLS = @('pyqgis-automation', 'civil3d-automation', 'bim-environment-setup')

# EJECUCIÓN: diagnóstico y comparación, sin escrituras.
& $SCRIPT -Action Diagnose -RepositoryPath $REPOSITORIO -CodexHome $CODEX_DATOS
& $SCRIPT -Action Compare -RepositoryPath $REPOSITORIO -CodexHome $CODEX_DATOS -SkillNames $SKILLS

# Simulación de instalación, incluso con Apply.
& $SCRIPT -Action Install -RepositoryPath $REPOSITORIO -CodexHome $CODEX_DATOS -SkillNames $SKILLS -Apply -WhatIf

# Tras revisar los archivos: solicita confirmación antes de cada skill faltante.
& $SCRIPT -Action Install -RepositoryPath $REPOSITORIO -CodexHome $CODEX_DATOS -SkillNames $SKILLS -Apply

# Verificación posterior; todas las entradas instaladas deben figurar Equal.
& $SCRIPT -Action Compare -RepositoryPath $REPOSITORIO -CodexHome $CODEX_DATOS -SkillNames $SKILLS
```

No cambiar políticas globales de ejecución, PATH ni seguridad para ejecutar el script. Si la política corporativa lo impide, resolver mediante el mecanismo autorizado.

## Recuperación y actualizaciones posteriores

`-Action Recover` propone clonar si falta el destino; sin `-Apply` no escribe. En un repositorio existente exige raíz exacta, origin autorizado y ausencia de cambios locales. Para actualizar, añadir `-Update`; revisar primero sin Apply y luego aplicar con confirmación. Solo admite upstream de la rama actual en origin y `pull --ff-only`. Una divergencia se detiene; no usa reset/clean ni guarda cambios locales automáticamente. El pull requiere red y puede actualizar archivos ya versionados, incluidas skills: revisar la procedencia y autorización antes de aplicarlo.

`Compare` informa `Missing`, `Equal`, `Different` y `LocalOnly` con SHA-256. `Install` crea solo skills ausentes y conserva su estructura sin duplicar el nombre de carpeta. Si ya hay una carpeta, incluso incompleta, informa diferencias y no combina, reemplaza ni elimina. Revisar manualmente los archivos indicados y obtener aprobación específica para cualquier reemplazo o sincronización; después volver a comparar. No existe sincronización automática de vuelta a GitHub.

Por seguridad esta versión admite únicamente `SKILL.md`, `agents/` y `references/`. Rechaza junctions/enlaces, archivos con nombres de autenticación/secretos y otros contenidos; skills con scripts/assets requieren revisión y adaptación autorizada. El filtro de nombres no demuestra ausencia de secretos dentro de un archivo: revisar contenido antes de versionar/copiar. No lee auth.json, tokens ni toda la carpeta `.codex`.

## Diagnóstico y limitaciones

Consulta versiones CLI mediante `--version` y busca QGIS, Civil 3D, Revit y Dynamo en el registro de desinstalación de Windows (usuario y equipo, 32/64 bits). No abre aplicaciones. Un registro no prueba instalación funcional; una aplicación portable o Dynamo integrado puede no aparecer. Confirmar versiones desde la aplicación anfitriona cuando falten o haya varias instalaciones. No comprueba licencias, plugins, motores, paquetes ni compatibilidad de automatizaciones.

La instalación copia archivos por etapas y verifica hashes después. Si falla por permisos o interrupción, puede quedar una carpeta parcial: se conserva para diagnóstico y una segunda ejecución no la sobrescribe. `-WhatIf` y la omisión de `-Apply` no prueban permisos reales de escritura ni conectividad. No se verificó clonación/pull reales ni recuperación en otra PC.

## Validación

Ejecutar desde PowerShell 7:

```powershell
# CONFIGURACIÓN
$REPOSITORIO = Join-Path $HOME 'Proyectos/automatizacion-bim'
$PRUEBA = Join-Path $REPOSITORIO '06-automatizaciones/01-scripts-generales/bim-environment-setup/tests/Test-Entorno.ps1'
# EJECUCIÓN
& $PRUEBA
```

Las pruebas crean fixtures en una carpeta temporal identificada y los conservan; no tocan skills reales, no hacen commits ni usan la red. Cubren sintaxis, carpetas ausentes/existentes, contenido idéntico/personalizado/extra, rechazo de auth, comparación sin escrituras y simulación de rutas con espacios y unidades D/E sin acceder a esas unidades. Validar manualmente en otra PC el diagnóstico, repositorio real, permisos, confirmaciones, CODEX_HOME/perfil personalizado, cancelación y reconocimiento de skills en una nueva sesión de Codex.
