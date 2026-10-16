# Automatizaciones

Categoría para flujos y utilidades reutilizables que no son documentación general ni proyectos que deban vivir en una categoría de plataforma dedicada. Incluye Dynamo, scripts generales y ejemplos autocontenidos.

Usa las subcarpetas existentes según el propósito del contenido. Documenta versiones probadas, requisitos, uso, entradas y salidas y validación por proyecto. No declares dependencias globales para herramientas que no las comparten.

## Subcategorías previstas

| Ruta futura | Finalidad |
| --- | --- |
| `01-scripts-generales/` | Utilidades que no dependen de una aplicación BIM específica. |
| `02-flujos-transversales/` | Automatizaciones que coordinan más de una herramienta o formato. |
| `03-ejemplos/` | Ejemplos pequeños y autocontenidos de proyectos reales. |

Crea una ruta solo cuando exista un proyecto real. Cada proyecto mantiene sus propias dependencias, configuración, pruebas y documentación. Los directorios anteriores `scripts/`, `ejemplos/` y `dynamo/` se conservan como documentación existente; no se renombran ni se usan para nuevos grafos de una aplicación anfitriona.

Para nuevos proyectos, ubica Dynamo para Revit en `01-revit/03-dynamo-revit/` y Dynamo para Civil 3D en `02-civil-3d/02-dynamo-civil-3d/` cuando sus proyectos existan. No compartas una configuración de paquetes entre ambos entornos sin verificar la compatibilidad.
