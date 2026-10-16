---
name: pyqgis-automation
description: Desarrollar, revisar, ejecutar y depurar scripts Python para QGIS mediante PyQGIS. Usar para automatizaciones sobre capas cargadas o archivos vectoriales, validación de campos y geometrías, procesamiento y correcciones con ejecución directa en QGIS o alternativa mediante archivos .py.
---

# Automatización PyQGIS

## Revisar antes de actuar

- Leer `~/.codex/AGENTS.md`, el AGENTS.md del repositorio y las instrucciones locales aplicables. Respetar su precedencia y el alcance autorizado. No sustituir esas reglas por esta skill.
- Inspeccionar Git, código, README y pruebas pertinentes. En `Juanca0795/automatizacion-bim`, mantener scripts ejecutables en `03-qgis/` y las skills separadas. No mover ni duplicar proyectos, modificar otras skills ni editar AGENTS.md sin solicitud explícita.
- Consultar `03-qgis/README.md`. Para limpieza de campos, leer `03-qgis/01-pyqgis/01-limpieza-campos/README.md`, su implementación y pruebas en lugar de copiarlas. No generalizar sus criterios de limpieza a otras tareas.
- Identificar objetivo, salida esperada, versión real de QGIS, Python y proveedor; comprobar Qt si afecta a la tarea. Obtener versiones dentro de QGIS mediante `Qgis.QGIS_VERSION` y `sys.version` cuando sea posible. Reutilizar datos conocidos y preguntar solo por requisitos indispensables ausentes.
- Distinguir versiones requeridas de verificadas. Consultar documentación oficial correspondiente a la versión si hay dudas sobre firmas, enumeraciones o cambios Qt/QGIS. No asumir compatibilidad entre Python estándar, PyQGIS, Dynamo y pyRevit.

## Desarrollar y corregir

- Conservar funciones y arquitectura ajenas a la corrección. Separar lógica independiente de adaptadores PyQGIS cuando facilite la validación, sin refactorizar por rutina.
- Entregar código completo actualizado al corregir, salvo petición expresa de fragmentos o únicamente un prompt. Explicar brevemente causa, solución y efecto.
- Centralizar opciones editables al principio bajo `# CONFIGURACIÓN`, con `CAPA_ENTRADA` primero cuando corresponda. Separar `# EJECUCIÓN`; pasar los valores a funciones sin dispersar rutas ni parámetros.
- Priorizar `QgsProject.instance()` y `mapLayersByName(CAPA_ENTRADA)`. Requerir una coincidencia inequívoca: no elegir silenciosamente la primera capa con nombre duplicado; permitir un identificador explícito si hace falta.
- No pedir rutas de datos para capas cargadas ni `RUTA_SCRIPT` para pegar código. Usar rutas solo para entradas externas, exportaciones o ejecutar un archivo guardado. Mantener la precedencia de entradas ya existente; rechazar una entrada explícita inválida sin sustituirla silenciosamente.
- No instalar dependencias sin autorización. Usar `qgis.PyQt` para Qt dentro de QGIS.

## Validar datos

- Comprobar existencia, tipo vectorial, `isValid()`, proveedor, campos e índices. Distinguir campos físicos, unidos y virtuales; comprobar capacidades y permisos necesarios antes de editar o escribir.
- Para operaciones espaciales, validar tipos de geometría, geometrías nulas/vacías, CRS y unidades; evaluar validez geométrica si el algoritmo lo necesita. No reparar geometrías ni reproyectar sin explicitarlo y sin autorización suficiente.
- Distinguir `None`, NULL de QGIS, variantes nulas, texto vacío, espacios, cero y False. No usar `if not valor` como comprobación universal de ausencia. Elegir la comprobación de nulidad disponible en la versión real y evitar comparaciones ambiguas con NULL.
- Definir valores inválidos según la tarea. Conservar números válidos como `0.8` y `"0000.8"`. Diferenciar booleanos y números. No interpretar separadores decimales, NaN, infinitos o marcadores de texto sin una política explícita.
- En el proyecto existente de limpieza, conservar su condición: basta un registro válido para conservar un campo; una capa vacía no justifica eliminar campos. Mantener el tratamiento existente de NULL, espacios, ceros y marcadores.
- Mostrar inicio, alcance, cantidades, advertencias y resultado. Emitir errores accionables; añadir trazas para depuración cuando sean útiles, sin revelar credenciales o fuentes confidenciales.

## Controlar edición y rendimiento

- Antes de eliminar o sobrescribir, presentar candidatos y efecto. Obtener autorización para la operación concreta; no reiterar una autorización ya suficiente. Mantener confirmaciones funcionales existentes y usar previsualización, respaldo o salida nueva según el riesgo.
- No guardar ni revertir ediciones ajenas. Identificar sesiones previas y registrar la sesión iniciada por el script. Comprobar retornos de inicio de edición, modificaciones, guardado y reversión; informar si el estado final es incierto.
- Preferir el búfer de edición cuando permita revisar y descartar. Las escrituras directas del proveedor pueden persistir inmediatamente: justificar su uso y verificar autorización. No ejecutar `commitChanges()` ni reemplazar destinos existentes salvo que el alcance lo autorice. Conservar el guardado manual del proyecto existente.
- Proteger claves, campos restringidos, de solo lectura, virtuales o unidos según la operación. No asumir que índices de capa y proveedor coinciden. Revalidar el esquema tras modificar campos.
- Recorrer entidades con iteradores; evitar materializar capas completas innecesariamente. Pedir atributos mínimos y `NoGeometry` si no se necesitan geometrías. Aplicar filtros, índices espaciales o lotes cuando aporten valor, sin cambiar el conjunto de datos evaluado ni omitir controles de seguridad.

## Entregar y ejecutar

- Proporcionar código autocontenido para pegar y ejecutar desde el editor de la consola Python de QGIS con el proyecto abierto. Recomendar ese editor para bloques multilínea. No depender de imports relativos o archivos auxiliares para la opción directa.
- Definir un punto de entrada claro e incluir la llamada necesaria. Explicar si el modo elegido usa `__main__`, evitando ejecutar dos veces.
- Ofrecer también ejecución del archivo `.py` desde QGIS. Marcar la ruta siguiente como ejemplo reemplazable; los parámetros del script se editan en su sección de configuración:

```python
# CONFIGURACIÓN: reemplazar por la ruta real del script guardado.
RUTA_SCRIPT = r"C:\ruta\script.py"

# EJECUCIÓN: pegar en la consola Python de QGIS.
from pathlib import Path
import runpy

if not Path(RUTA_SCRIPT).is_file():
    raise FileNotFoundError("No existe RUTA_SCRIPT: " + RUTA_SCRIPT)
runpy.run_path(RUTA_SCRIPT, run_name="__main__")
```

- No asumir que `init_globals` reemplaza asignaciones del archivo: diseñar explícitamente una interfaz externa si se necesita. No presentar ese bloque como ejecución en Python estándar.
- Preparar ejecución autónoma con `QgsApplication` solo si se solicita y se conoce el entorno. No inicializar otra aplicación dentro de QGIS.
- Documentar junto al proyecto objetivo, requisitos, versiones verificadas, parámetros, entradas/salidas, ejecución directa y alternativa, ejemplos seguros, limitaciones y pasos manuales. Enlazar reglas comunes sin copiarlas.

## Validar y comunicar

- Ejecutar pruebas existentes pertinentes con el intérprete disponible, sin instalar paquetes. Validar sintaxis sin ejecutar el punto de entrada. Probar lógica independiente con casos representativos de nulos simulados, vacíos, ceros, valores válidos y entradas erróneas cuando corresponda. Identificar simulaciones como tales.
- Validar manualmente en QGIS sobre datos seguros: capa cargada, nombres ausentes/duplicados, tipo incorrecto, campos faltantes, geometría/CRS si corresponde, previsualización, cancelación, confirmación y guardar/descartar. Probar entrada externa y permisos cuando el flujo los use.
- Si QGIS no está disponible, dejar esas pruebas pendientes. No equiparar pruebas unitarias o sintaxis con validación del flujo GIS completo. No modificar datos reales para probar sin autorización.
- Revisar `git status` y comunicar archivos afectados, pruebas aprobadas/fallidas/pendientes y limitaciones. No hacer commits, push ni publicar sin autorización explícita. Antes de sincronizar con GitHub, mostrar archivos afectados y solicitar aprobación.
