---
name: bim-environment-setup
description: Diagnosticar, instalar, recuperar, reconstruir y sincronizar de forma controlada el entorno de automatización BIM en computadoras Windows mediante Juanca0795/automatizacion-bim. Usar para migrar de PC, localizar Codex y sus skills, recuperar el repositorio y comparar o instalar skills versionadas preservando personalizaciones y credenciales.
---

# Entorno BIM portable

## Revisar y localizar

- Leer las instrucciones globales y AGENTS.md del repositorio, revisar Git y las instrucciones locales aplicables. No modificar AGENTS.md ni skills ajenas al alcance solicitado.
- Usar exclusivamente `Juanca0795/automatizacion-bim`; identificar su estructura y skills disponibles en `07-documentacion/skills-codex/`, incluidas `pyqgis-automation` y `civil3d-automation` cuando existan. No inventar recursos faltantes ni copiar proyectos ejecutables dentro de las skills.
- Resolver rutas dinámicamente: carpeta de proyectos elegida por el usuario o `$HOME/Proyectos/automatizacion-bim`; directorio de datos de Codex explícito, luego `$env:CODEX_HOME`, luego `$HOME/.codex`. Distinguir ubicación del ejecutable y directorio de datos. Si hay perfiles alternativos o ambigüedad, mostrar candidatos y resolver antes de instalar.
- No fijar nombres de equipo, usuario, unidad ni rutas del creador. Utilizar `$HOME`, `$env:USERPROFILE`, `$env:LOCALAPPDATA` o `$env:APPDATA` según el recurso, y `Join-Path`/rutas literales para espacios. No modificar variables globales para adaptar el equipo.

## Diagnosticar y proponer

- Leer el README y script mantenidos en `06-automatizaciones/01-scripts-generales/bim-environment-setup/` dentro del clon seleccionado. No duplicarlos en esta skill. Si no están disponibles, explicar que deben recuperarse de una versión publicada/autorizada o transferirse de forma explícita; no simular su existencia.
- Usar `Entorno-Bim.ps1 -Action Diagnose` para consultar Git, Python, Node.js, npm, Codex CLI y registros de QGIS, Civil 3D, Revit y Dynamo. No abrir aplicaciones ni instalar/actualizar componentes automáticamente. Distinguir «no detectado» de «no instalado» y confirmar manualmente versiones del anfitrión, Dynamo integrado, paquetes, licencias y motores.
- Usar `Recover`, `Compare` o `Install` sin `-Apply` como vista previa; `-Apply -WhatIf` también debe evitar escrituras. Mostrar rutas resueltas, archivos afectados y acción antes de solicitar aprobación. Para ejecución automatizada por el agente, obtener aprobación explícita antes de usar Apply; no considerar autorización la mera consulta o vista previa.

## Recuperar repositorio y estructura

- Si falta el repositorio, ofrecer clonar únicamente la URL autorizada en una carpeta ausente elegida por el usuario. Si existe cualquier contenido, no clonarlo encima. El README proporciona el arranque antes de disponer del script.
- Si ya existe, verificar raíz exacta, origin, estado local, rama y upstream. No actualizar un árbol con cambios. Actualizar solo con autorización y fast-forward; detenerse ante divergencia o configuración inesperada. No usar reset --hard, clean, stash automático ni sobrescribir cambios locales.
- Reconstruir desde archivos versionados preservando las siete categorías y sus README. No crear carpetas vacías ni restaurar archivos borrados sobre trabajo local sin revisar el efecto y obtener aprobación. No copiar configuraciones dependientes de otro equipo como si fueran portables.

## Comparar e instalar skills

- Inventariar skills locales y comparar contenido con la fuente versionada mediante SHA-256, incluidos archivos faltantes, diferentes y locales extra. No tratar diferencias de hash como autorización de reemplazo.
- Instalar solo skills ausentes tras autorización, directamente en `<CodexHome>/skills/<nombre>/`, sin anidar `<nombre>/<nombre>`. Conservar `SKILL.md`, `agents/` y `references/`; verificar hashes al terminar y repetir comparación para comprobar idempotencia.
- Si la carpeta ya existe, incluso incompleta, mostrar diferencias y preservar todo. El script no reemplaza ni combina skills existentes. Para sincronización solicitada, presentar un plan por archivo y obtener aprobación concreta; conservar personalizaciones y no eliminar extras por rutina. Si no puede determinarse qué conservar, pedir la decisión necesaria.
- Esta versión del script admite únicamente SKILL.md, agents y references; rechaza enlaces/junctions y nombres de archivos de secretos. Revisar manualmente contenidos y cualquier recurso adicional antes de adaptar el instalador. Un filtro de nombres no garantiza ausencia de información sensible.
- No copiar autenticación, tokens, contraseñas, credenciales ni la carpeta `.codex` completa. No leer secretos para diagnosticar rutas. No publicar configuraciones locales ni sincronizar hacia GitHub sin autorización.
- Si falla la copia, informar la instalación parcial y conservar evidencia; no borrar ni sobrescribir automáticamente al reintentar. Si la sesión no permite escribir en el destino operativo, mantener la copia versionada, preparar una temporal permitida y proporcionar el procedimiento portable del README usando el clon como fuente.

## Validar y entregar

- Ejecutar `tests/Test-Entorno.ps1` del proyecto: sintaxis, fixtures de carpetas faltantes/existentes, contenido idéntico/personalizado/extra, nombres de autenticación, rutas con espacios y unidades alternativas y vista previa. No instalar en skills reales ni hacer commits o llamadas de red como parte de pruebas sin autorización.
- Comprobar también instalación en un CodexHome temporal aislado y repetición sin cambios cuando sea posible. Tratar las unidades simuladas como pruebas de resolución de rutas, no como recuperación física en esas unidades.
- Validar esta skill con quick_validate de skill-creator si está disponible, sin instalar dependencias. Revisar enlaces, metadatos y precedencia de instrucciones. No afirmar recuperación en otra PC ni funcionamiento de aplicaciones BIM a partir del diagnóstico.
- Informar estructura, archivos afectados, rutas operativa/versionada/temporal, procedimiento de otra PC, comprobaciones aprobadas y pendientes, limitaciones e instalaciones manuales. Revisar Git al terminar. No crear repositorios, commits, push ni publicar; cualquier sincronización requiere aprobación previa sobre archivos concretos.
