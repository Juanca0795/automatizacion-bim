# Limpieza de campos en capas vectoriales

Script para la consola Python de QGIS que identifica campos sin información en todos los registros de una capa cargada. Solo prepara el borrado de campos que superan las comprobaciones de seguridad; el usuario revisa y guarda o descarta la sesión de edición en QGIS.

## Requisitos y compatibilidad

- QGIS de escritorio con PyQGIS y consola Python. No se requiere instalar paquetes Python externos.
- Una capa vectorial cargada, con un nombre único en el proyecto y un proveedor que permita editar y eliminar atributos.
- Las versiones concretas de QGIS, Python y proveedores de datos aún no se han verificado en una instalación de escritorio. La lógica de clasificación sí puede probarse con Python estándar.

## Uso

1. Trabaja sobre una copia de la fuente de datos o crea una copia de seguridad antes de guardar cambios en QGIS.
2. Abre `limpieza_campos.py` y cambia `CAPA_ENTRADA = "Paquete 33"`, en la sección **CONFIGURACIÓN**, por el nombre exacto de la capa cargada en QGIS.
3. En la consola Python de QGIS, copia y ejecuta este bloque. Sustituye `RUTA_SCRIPT` por la ubicación real del archivo Python en tu equipo:

   ```python
   # CONFIGURACIÓN
   RUTA_SCRIPT = r"C:\ruta\automatizacion-bim\03-qgis\01-pyqgis\01-limpieza-campos\limpieza_campos.py"

   # EJECUCIÓN
   import runpy
   runpy.run_path(RUTA_SCRIPT, run_name="__main__")
   ```

4. Lee la lista de candidatos y campos conservados que aparece en la consola. Confirma el cuadro de diálogo solo si corresponde eliminar todos los candidatos.
5. Revisa la tabla de atributos. Los borrados quedan **pendientes de guardar**: usa las opciones de QGIS para guardar o descartar la edición. El script nunca llama a `commitChanges()`.

El script se detiene sin editar si no encuentra exactamente una capa con ese nombre, si no es vectorial o válida, si ya hay ediciones sin guardar, si el proveedor no permite eliminar atributos, si la capa está vacía o si la lectura de registros no coincide con el recuento informado.

## Criterio de eliminación

Un campo es candidato solo cuando **todos** sus registros tienen valores inválidos. Se consideran inválidos `NULL` de QGIS, `None`, texto vacío o solo espacios, `#D` y ceros numéricos o escritos como texto (por ejemplo, `0`, `00`, `0000.000`, `-0.0` y `0e5`). El texto se analiza tras quitar espacios exteriores; `#D` distingue mayúsculas de minúsculas.

Valores como `0.8`, `0000.8`, `0.01`, `-0.5`, `100` o cualquier texto informativo conservan el campo. Los formatos que el script no reconoce como cero, como `0,0`, también se conservan por precaución. Un campo sin registros no se clasifica como vacío: la operación se cancela.

Las claves primarias, los campos no pertenecientes directamente al proveedor, los de solo lectura y los que tienen restricciones se conservan. El proveedor puede proteger otros campos; si rechaza un borrado preparado, el script revierte su propia sesión de edición y muestra el error.

## Pruebas

Desde la raíz del repositorio, sin QGIS ni dependencias externas:

```bash
python3 -m unittest discover -s 03-qgis/01-pyqgis/01-limpieza-campos/tests -p 'test_*.py' -v
```

Las pruebas cubren la clasificación de valores, las mezclas de registros, la exclusión de índices protegidos y el rechazo de capas vacías o registros incompletos.

## Validación pendiente en QGIS

Probar con una copia de capa que incluya campos con todos los tipos de valor indicados, un campo con al menos un valor válido y una clave primaria. Comprobar la lista previa, cancelar el diálogo, confirmar el borrado preparado y ensayar tanto descartar como guardar la edición. Repetir con un proveedor de solo lectura y con una capa que ya tenga cambios pendientes.

No se ha ejecutado PyQGIS en Codex Cloud. El guardado final depende del proveedor de datos y puede fallar o tener restricciones adicionales: revisa los mensajes de QGIS antes de considerar persistida la limpieza. Los datos originales no se modificaron durante el desarrollo.
