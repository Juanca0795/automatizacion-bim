# Automatización BIM

Repositorio general para organizar herramientas, flujos y documentación de automatización aplicados a BIM, diseño e ingeniería.

> Menos tareas repetitivas. Más control BIM.

El propósito es reducir tareas manuales y errores repetitivos, estandarizar procesos, mejorar la productividad y crear herramientas reutilizables para ingeniería, modelado y gestión BIM.

## Índice

| Categoría | Contenido |
| --- | --- |
| [01 Revit](01-revit/README.md) | Automatización para Revit y extensiones pyRevit. |
| [02 Civil 3D](02-civil-3d/README.md) | Herramientas para diseño y automatización en Civil 3D. |
| [03 QGIS](03-qgis/README.md) | Scripts, complementos e integración geoespacial con QGIS. |
| [04 Visores BIM](04-visores-bim/README.md) | Visores e integraciones de modelos BIM. |
| [05 IFC/OpenBIM](05-ifc-openbim/README.md) | Intercambio IFC y flujos de trabajo OpenBIM. |
| [06 Automatizaciones](06-automatizaciones/README.md) | Grafos Dynamo, scripts generales y ejemplos. |
| [07 Documentación](07-documentacion/README.md) | Guías, notas técnicas y convenciones comunes. |

## Tecnologías previstas

El repositorio contempla Python, Dynamo, Revit y Revit API, IFC, QGIS, Civil 3D y Git. Esta lista describe el ámbito de interés; no implica que las herramientas o dependencias estén instaladas ni que la compatibilidad esté verificada.

Las áreas incluyen automatizaciones, flujos Dynamo, recursos Revit, utilidades Python, integración BIM + GIS y documentación. Cada proyecto debe identificar su plataforma, versiones probadas, requisitos, uso, entradas y salidas, y forma de validación.

## Organización y desarrollo

Mantén cada iniciativa en su categoría y agrupa proyectos separados solo cuando sea necesario. Separa la lógica reutilizable de los adaptadores que dependen de aplicaciones BIM. No hay todavía un flujo global de instalación o pruebas ni dependencias declaradas; consulta la documentación de cada proyecto antes de ejecutar archivos.

No añadas automatizaciones ficticias ni modelos o datos de clientes sin autorización. Declara dependencias y configuraciones solo cuando un proyecto concreto las necesite.

Sigue las instrucciones generales de [AGENTS.md](AGENTS.md). Estado del repositorio: **en desarrollo**.

## Categorías

Cada categoría tiene un README que describe su finalidad y las convenciones específicas.

```text
automatizacion-bim/
├── 01-revit/
├── 02-civil-3d/
├── 03-qgis/
├── 04-visores-bim/
├── 05-ifc-openbim/
├── 06-automatizaciones/
└── 07-documentacion/
```
