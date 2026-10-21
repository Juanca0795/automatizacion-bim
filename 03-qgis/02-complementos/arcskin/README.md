# ArcSkin para QGIS

Código fuente completo del complemento ArcSkin 0.4.5 para QGIS. El contenido está organizado con la estructura que QGIS espera para instalar un complemento; no se conserva el ZIP original dentro del repositorio.

ArcSkin identifica el idioma configurado en la interfaz de QGIS y traduce sus pestañas, paneles y herramientas para que coincidan con ese idioma. Incluye traducciones propias para español; en otros idiomas utiliza las traducciones disponibles de QGIS y del complemento.

## Requisitos

- QGIS 3.40 o posterior compatible con Qt 6.
- Versión del complemento: `0.4.5`.
- La compatibilidad declarada por el paquete llega hasta QGIS 4.99.

## Instalación

La instalación se realiza desde un ZIP mediante **Complementos → Instalar a partir de ZIP**.

1. Descarga el ZIP del complemento desde la sección **Releases** o créalo a partir de esta carpeta.
2. En QGIS, abre **Complementos → Instalar a partir de ZIP**.
3. Selecciona el archivo ZIP y confirma la instalación.
4. Activa ArcSkin desde **Complementos → Administrar e instalar complementos → Instalados**.

## Generar el ZIP desde el código fuente

Si el repositorio no incluye un ZIP publicado, genera uno respetando `arcskin` como carpeta raíz:

```bash
cd 03-qgis/02-complementos
zip -r ArcSkin_0.4.5_ES_QGIS.zip arcskin
```

Después selecciona el archivo generado en **Complementos → Instalar a partir de ZIP**. No basta con comprimir únicamente los archivos `.py`: también deben incluirse `metadata.txt`, `resources/`, `i18n/` y la licencia.

## Licencia y validación

Consulta `LICENSE` antes de redistribuir el complemento. La validación realizada en este repositorio comprueba que los archivos del paquete se pueden extraer y que el metadato declara QGIS 3.40 como versión mínima. La activación completa debe verificarse en una instalación de escritorio de QGIS.
