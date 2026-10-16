# Automatización BIM

Repositorio general para organizar herramientas, flujos y documentación de automatización aplicados a BIM, diseño e ingeniería. Las carpetas describen áreas de trabajo; el repositorio no presupone una plataforma, versión o dependencia concreta. Cada proyecto debe documentar sus propios requisitos antes de añadirlos.

> Menos tareas repetitivas. Más control BIM.

El objetivo es reducir trabajo manual y errores repetitivos, estandarizar procesos, mejorar la productividad y crear herramientas reutilizables para ingeniería, modelado y gestión BIM.

El ámbito previsto incluye Python, Dynamo, Revit y su API, IFC/OpenBIM, QGIS, Civil 3D y visores BIM. Esta lista describe intereses del repositorio, no dependencias instaladas ni compatibilidad ya verificada.

## Áreas

| Carpeta | Contenido |
| --- | --- |
| [`revit/`](revit/README.md) | Automatizaciones y recursos relacionados con Autodesk Revit. |
| [`dynamo/`](dynamo/README.md) | Grafos y recursos para Dynamo. |
| [`pyrevit/`](pyrevit/README.md) | Extensiones y herramientas para pyRevit. |
| [`civil3d/`](civil3d/README.md) | Automatización para Autodesk Civil 3D. |
| [`qgis/`](qgis/README.md) | Herramientas y flujos de trabajo para QGIS. |
| [`ifc-openbim/`](ifc-openbim/README.md) | Intercambio IFC e iniciativas OpenBIM. |
| [`visores-bim/`](visores-bim/README.md) | Prototipos e integraciones de visores BIM. |
| [`scripts/`](scripts/README.md) | Utilidades generales que no pertenecen a una plataforma específica. |
| [`ejemplos/`](ejemplos/README.md) | Ejemplos pequeños y autocontenidos. |
| [`documentacion/`](documentacion/README.md) | Guías, decisiones y documentación transversal. |

## Organización de proyectos

Mantén cada herramienta en su área y agrupa los archivos por proyecto cuando una carpeta contenga más de una iniciativa. Incluye junto a cada proyecto un README con su propósito, plataforma y versión probadas, requisitos, uso, entradas y salidas, y validación manual o automatizada. Separa la lógica reutilizable de los adaptadores que dependen de aplicaciones BIM; evita declarar requisitos globales para proyectos que no los comparten.

No se incluyen automatizaciones de ejemplo que aparenten estar listas para producción. Las versiones y dependencias se documentarán cuando cada proyecto las defina. Los datos y modelos de clientes no deben incorporarse al repositorio sin autorización y revisión de su sensibilidad.

## Desarrollo

No hay todavía un flujo global de instalación o pruebas: el repositorio no declara dependencias ni una plataforma de ejecución común. Consulta el README del área o proyecto antes de ejecutar sus archivos. Añade configuraciones de herramientas solo cuando un proyecto concreto las necesite y documenta cómo usarlas.

## Contribuciones

Sigue las instrucciones de [`AGENTS.md`](AGENTS.md), limita cada cambio a su proyecto y conserva los archivos fuente y modelos de forma explícita: `.gitignore` no sustituye una revisión antes de confirmar cambios.
