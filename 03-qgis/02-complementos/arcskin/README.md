# ArcSkin para QGIS

Código fuente completo del complemento ArcSkin 0.4.5 para QGIS. El contenido está organizado con la estructura que QGIS espera para instalar un complemento; no se conserva el ZIP original dentro del repositorio.

## Requisitos

- QGIS 3.40 o posterior compatible con Qt 6.
- Versión del complemento: `0.4.5`.
- La compatibilidad declarada por el paquete llega hasta QGIS 4.99.

## Instalar desde este repositorio

1. Descarga o clona el repositorio.
2. Copia la carpeta `arcskin` completa —incluidos `metadata.txt`, `resources/`, `i18n/` y todos los archivos Python— a la carpeta de complementos de tu perfil de QGIS.
3. Reinicia QGIS.
4. Activa **ArcSkin** desde **Complementos → Administrar e instalar complementos → Instalados**.

La carpeta de complementos se puede localizar desde QGIS en **Configuración → Perfiles de usuario → Abrir carpeta del perfil activo**. Dentro del perfil, la ubicación habitual es:

```text
python/plugins/
```

La carpeta final debe quedar así:

```text
python/plugins/arcskin/metadata.txt
```

No copies únicamente los archivos `.py`: los recursos visuales, traducciones, iconos y metadatos también son necesarios.

## Instalar usando un ZIP generado localmente

Si se necesita el formato de instalación de QGIS, comprime la carpeta `arcskin` respetando su nombre en la raíz del archivo:

```bash
cd 03-qgis/02-complementos
zip -r ArcSkin_0.4.5_ES_QGIS.zip arcskin
```

Después usa **Complementos → Administrar e instalar complementos → Instalar desde ZIP** y selecciona el archivo generado. El ZIP es un artefacto de distribución; no es necesario versionarlo junto al código fuente.

## Licencia y validación

Consulta `LICENSE` antes de redistribuir el complemento. La validación realizada en este repositorio comprueba que los archivos del paquete se pueden extraer y que el metadato declara QGIS 3.40 como versión mínima. La activación completa debe verificarse en una instalación de escritorio de QGIS.
