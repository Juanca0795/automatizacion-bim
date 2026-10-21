# QGIS

Área para complementos, scripts e integraciones con QGIS. Documenta versiones probadas de QGIS/Python, proveedores de datos necesarios, instalación, uso y validación de cada proyecto.

No se incluyen datos geográficos de ejemplo ni dependencias por defecto.

## Subcategorías

| Subcategoría | Finalidad |
| --- | --- |
| `01-pyqgis/` | Scripts de procesamiento y automatización con PyQGIS. |
| `02-complementos/` | Complementos de QGIS. |
| `03-integracion-bim-gis/` | Flujos que conectan datos BIM y geoespaciales. |

Crea nuevas rutas solo cuando exista un proyecto real. Mantén en cada proyecto sus requisitos, configuración, datos de prueba seguros y pruebas, indicando las versiones de QGIS y Python verificadas.

Primer proyecto: [limpieza de campos en capas vectoriales](01-pyqgis/01-limpieza-campos/README.md).

## ArcSkin

[ArcSkin para QGIS](02-complementos/arcskin/README.md) es el complemento de interfaz inspirado en ArcGIS Pro incluido en este repositorio. Detecta el idioma configurado en QGIS y adapta sus pestañas, paneles y herramientas; incluye traducciones propias para español.

Para instalarlo, descarga o genera el ZIP completo del complemento y usa **Complementos → Instalar a partir de ZIP** en QGIS. La carpeta debe conservar `arcskin` como raíz e incluir `metadata.txt`, `resources/`, `i18n/` y los archivos Python.
