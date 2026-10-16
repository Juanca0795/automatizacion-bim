# Revit

Área para proyectos que automatizan Autodesk Revit, como scripts, complementos, integración con la API y recursos de proyecto.

Agrupa cada iniciativa en su propia carpeta cuando haya varias. Documenta las versiones de Revit y del entorno de ejecución probadas, requisitos, instalación, uso y validación. Mantén aquí solo el código y los recursos propios del proyecto; describe por separado cualquier requisito de la aplicación anfitriona.

## Subcategorías previstas

| Ruta futura | Finalidad |
| --- | --- |
| `01-scripts-api/` | Scripts que usan la API de Revit sin depender de una extensión concreta. |
| `02-pyrevit/` | Extensiones y comandos pyRevit. |
| `03-dynamo-revit/` | Grafos Dynamo ejecutados con Revit como aplicación anfitriona. |
| `04-complementos/` | Complementos instalables de Revit, incluidos los desarrollados con .NET. |

Esta numeración describe destinos futuros: crea una subcarpeta solo para un proyecto real. El directorio anterior `pyrevit/` se conserva como documentación existente; cualquier traslado requerirá una decisión explícita. Cada proyecto deberá mantener su propia documentación, dependencias, configuración y pruebas. Los grafos Dynamo para Civil 3D corresponden a `02-civil-3d/`.
