# Limpieza de campos en capas vectoriales

Script PyQGIS para encontrar campos cuyos valores son inválidos en todos los registros. Permite usar una capa ya cargada en el proyecto actual de QGIS o cargar un archivo vectorial externo. Los candidatos se muestran antes de iniciar la edición; QGIS pide confirmación y deja los cambios pendientes para que el usuario los guarde o descarte.

## Requisitos y compatibilidad

- QGIS de escritorio con consola Python y PyQGIS.
- Para una entrada externa, un archivo vectorial que pueda abrirse con el proveedor OGR de QGIS y que permita eliminar atributos.
- No requiere paquetes Python externos.
- No se han verificado versiones concretas de QGIS, Python ni proveedores en una instalación de escritorio.

## Configuración

Edita al inicio de `limpieza_campos.py`:

```python
# OPCIÓN 1: capa que ya está cargada en el proyecto de QGIS
CAPA_ENTRADA = "Paquete 33"

# OPCIÓN 2: archivo vectorial externo (si se indica, tiene prioridad)
RUTA_ENTRADA = None
# Ejemplo: r"C:\Proyectos\archivo.shp"

# True analiza y muestra los candidatos sin iniciar una edición
SOLO_PREVISUALIZAR = False
```

Deja `RUTA_ENTRADA = None` para buscar `CAPA_ENTRADA` en `QgsProject.instance()`. Para procesar un archivo, asigna a `RUTA_ENTRADA` su ruta real; esa opción tiene prioridad aunque `CAPA_ENTRADA` también tenga un valor. La capa externa se añade al proyecto solo después de confirmar una operación con candidatos.

## Uso

### Ejecutar directamente en QGIS

Abre el script en el editor Python de QGIS y ejecútalo con el proyecto deseado abierto. También puedes pegar el contenido completo del script en la consola Python y llamar `ejecutar()` después de definirlo. No hace falta una ruta al archivo de datos cuando se utiliza una capa ya cargada.

Si ejecutas el archivo desde la consola usando `runpy`, la ruta que sigue es la ubicación del **script Python**, no la ruta de entrada de los datos:

```python
# CONFIGURACIÓN: ubicación del archivo .py en este equipo
RUTA_SCRIPT = r"C:\ruta\automatizacion-bim\03-qgis\01-pyqgis\01-limpieza-campos\limpieza_campos.py"

# EJECUCIÓN
import runpy
runpy.run_path(RUTA_SCRIPT, run_name="__main__")
```

### Opción 1: capa cargada en el proyecto

Configura el script así:

```python
CAPA_ENTRADA = "Paquete 33"  # nombre exacto en el panel de capas
RUTA_ENTRADA = None
SOLO_PREVISUALIZAR = False
```

El script usa `QgsProject.instance().mapLayersByName(CAPA_ENTRADA)` y requiere que exista una sola coincidencia válida.

### Opción 2: archivo vectorial externo

Configura el script así y ejecútalo en QGIS:

```python
CAPA_ENTRADA = "Paquete 33"  # se ignora mientras RUTA_ENTRADA tenga una ruta
RUTA_ENTRADA = r"C:\Proyectos\levantamiento.shp"
SOLO_PREVISUALIZAR = False
```

El archivo debe existir y QGIS debe poder abrirlo como capa vectorial con OGR. El script valida la capa antes de analizarla. Tras confirmar candidatos, la añade al proyecto para que la sesión de edición siga disponible para revisión.

### Previsualización y confirmación

Primero revisa en la consola el número de registros analizados, los campos candidatos, los campos protegidos y los que se conservarán. Para hacer solo una previsualización, configura `SOLO_PREVISUALIZAR = True`; no se inicia una sesión de edición. Para preparar el borrado, déjalo en `False` y confirma el cuadro de diálogo de QGIS.

Los campos eliminados quedan pendientes de guardar en QGIS. Revisa la tabla de atributos y usa las opciones de QGIS para guardar o descartar los cambios; el script no ejecuta `commitChanges()`.

## Criterio de eliminación

Un campo es candidato solo si **todos** sus registros contienen valores inválidos: `NULL` de QGIS, `None`, texto vacío o compuesto por espacios, `#D`, ceros numéricos o ceros escritos como texto (por ejemplo, `0`, `00`, `0000.000`, `-0.0` y `0e5`).

Si al menos un registro contiene información válida, el campo se conserva. Por ejemplo: `0.8`, `0000.8`, `0.01`, `-0.5`, `100` o texto informativo. `#D` distingue mayúsculas de minúsculas; formatos no reconocidos como cero, por ejemplo `0,0`, se conservan por precaución. Una capa sin registros se rechaza.

Se conservan las claves primarias, los campos que no pertenecen al proveedor, los de solo lectura y los que tienen restricciones. Se comprueban las capacidades del proveedor y el resultado de la eliminación preparada; ante un error se revierte la sesión iniciada por el script cuando QGIS permite hacerlo.

## Seguridad y mensajes habituales

Trabaja con una copia de seguridad de la fuente antes de guardar cambios. Lee la lista de candidatos y confirma solo si quieres eliminarlos. Puedes establecer `SOLO_PREVISUALIZAR = True` para revisar sin editar. Si ocurre un error, el script lo informa en la consola y se detiene antes de borrar cuando no puede validar la entrada o los permisos.

- **No existe el archivo indicado en `RUTA_ENTRADA`:** corrige la ruta y verifica que el archivo sea accesible desde el equipo donde corre QGIS.
- **No se pudo cargar como capa vectorial compatible con OGR:** confirma que el formato sea vectorial y compatible con el proveedor OGR de tu instalación.
- **Se necesita exactamente una capa cargada:** corrige `CAPA_ENTRADA` o elimina/renombra las capas duplicadas; alternativamente, configura `RUTA_ENTRADA`.
- **Capa de solo lectura o con sesión de edición:** guarda o descarta los cambios previos y revisa los permisos y capacidades del proveedor.
- **El proveedor no admite eliminar atributos:** utiliza una fuente editable que permita cambios en la estructura de campos.
- **Falló la reversión de la edición:** revisa inmediatamente el estado de la capa en QGIS y no guardes hasta confirmar sus cambios.

## Pruebas

Desde la raíz del repositorio, ejecuta las pruebas unitarias con Python estándar, sin QGIS ni dependencias externas:

```bash
python3 -m unittest discover -s 03-qgis/01-pyqgis/01-limpieza-campos/tests -p 'test_*.py' -v
```

Las pruebas automatizadas cubren la clasificación original de valores, la protección de campos y la resolución de las dos formas de entrada, incluida la prioridad y el rechazo de rutas o capas inválidas. No ejecutan operaciones de edición en QGIS.

La validación manual pendiente requiere QGIS de escritorio: probar una capa cargada y un archivo externo, usar la previsualización, cancelar y confirmar el diálogo, y guardar o descartar cambios sobre una copia de datos. No se afirma que esa validación de escritorio se haya realizado.
