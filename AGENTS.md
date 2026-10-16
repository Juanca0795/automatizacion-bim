# Instrucciones para Codex

Estas instrucciones rigen el desarrollo, la revisión y el mantenimiento de los proyectos de automatización BIM del repositorio. Antes de trabajar, inspecciona el proyecto, sus instrucciones locales y el estado de Git. No inventes automatizaciones, resultados, compatibilidad ni requisitos.

## Organización

Conserva la numeración, los nombres y la ubicación de las siete categorías:

- `01-revit`: Revit, su API y pyRevit.
- `02-civil-3d`: proyectos de Civil 3D.
- `03-qgis`: proyectos de QGIS.
- `04-visores-bim`: visores e integraciones BIM.
- `05-ifc-openbim`: intercambio IFC y flujos OpenBIM.
- `06-automatizaciones`: scripts generales, grafos Dynamo y ejemplos.
- `07-documentacion`: guías y documentación transversal.

Coloca cada cambio en su categoría. Si una categoría reúne proyectos distintos, sepáralos en subcarpetas con nombres claros y un README por proyecto. No añadas carpetas vacías ni archivos de configuración sin una necesidad concreta. Mantén la documentación específica junto al proyecto y enlázala desde la documentación común cuando corresponda.

## Desarrollo y dependencias

- Escribe código modular, legible y reutilizable; separa la lógica independiente de los adaptadores que requieren aplicaciones BIM. Evita duplicación innecesaria.
- Usa nombres descriptivos para funciones, clases y variables. Respeta las convenciones del lenguaje y del proyecto. Añade comentarios en español cuando expliquen decisiones técnicas relevantes, no para repetir lo que expresa el código.
- Introduce dependencias solo cuando la tarea las necesite. Usa el gestor apropiado para el proyecto, respeta sus archivos de bloqueo y documenta versiones y pasos de instalación. No impongas dependencias globales a proyectos independientes.

## Configuración centralizada de parámetros y rutas de ejecución

Esta convención aplica globalmente a todos los proyectos y tecnologías del repositorio, incluidos Python, PyQGIS, Dynamo, pyRevit, Revit API, Civil 3D, C#, PowerShell, JavaScript, TypeScript y otros lenguajes o entornos que requieran entradas configurables.

- Agrupa al inicio del código los valores que el usuario deba cambiar o léelos de un archivo de configuración claramente identificado. Usa nombres idiomáticos para el lenguaje y describe qué valores debe editar. Por ejemplo: `RUTA_SCRIPT`, `RUTA_ENTRADA`, `RUTA_SALIDA`, `CARPETA_TRABAJO`, `CAPA_ENTRADA`, `NOMBRE_ARCHIVO` y `NOMBRE_MODELO`; adapta su estilo a cada lenguaje.
- Evita dispersar rutas, nombres y valores modificables entre funciones y comandos. Las funciones deben recibir esos valores como parámetros o depender de la configuración definida de forma explícita.
- Separa visualmente las secciones **CONFIGURACIÓN** y **EJECUCIÓN**. En la documentación, ofrece un bloque completo listo para copiar en la consola, terminal o aplicación anfitriona; coloca al principio las rutas y parámetros editables y señala cuáles se deben reemplazar.
- Usa sintaxis de rutas compatible con el lenguaje, el sistema operativo y la aplicación anfitriona. Valida entradas y permisos antes de escribir. No supongas rutas locales ni sobrescribas o elimines datos existentes sin autorización.
- No guardes credenciales o secretos en el código, ejemplos ni archivos de configuración versionados. Usa el mecanismo seguro disponible para el entorno.
- En entornos visuales como Dynamo, agrupa los valores configurables en nodos de entrada claramente nombrados, con unidades, formato y valores permitidos documentados. Aplica el mismo principio a los controles de entrada de otras aplicaciones.
- Cuando no se necesiten rutas de archivos, centraliza de igual forma las demás opciones que el usuario deba ajustar.

## Compatibilidad BIM

- Identifica la aplicación anfitriona, su versión, la API y el intérprete necesarios. Diferencia versiones requeridas de versiones verificadas; no afirmes compatibilidad sin evidencia.
- Distingue Python estándar del motor de Python de Dynamo, del entorno PyQGIS y del entorno de pyRevit. Comprueba el motor y sus bibliotecas antes de reutilizar código entre ellos.
- No supongas que Revit, Civil 3D u otras aplicaciones de escritorio están disponibles en la nube. Separa las comprobaciones que pueden ejecutarse localmente de las que requieren la aplicación anfitriona y documenta los pasos pendientes.

## Seguridad y control de cambios

- Conserva archivos, modelos y datos existentes. No elimines, sobrescribas ni reorganices archivos sin autorización explícita. Antes de un cambio estructural importante, presenta su alcance e impacto y confirma que la tarea lo autoriza.
- No incorpores credenciales, contraseñas ni información confidencial al código, la documentación, los ejemplos o el historial de Git. Evita incluir modelos y datos de clientes sin autorización.
- Para cambios significativos, trabaja en una rama independiente y prepara un pull request para revisión. Revisa `git status` antes de terminar y comunica los archivos creados, modificados o eliminados.

## Validación

- Ejecuta las pruebas existentes que sean pertinentes cuando el entorno lo permita. Valida las entradas, salidas y efectos de la automatización de forma acorde con su riesgo.
- Identifica las pruebas que requieren Revit, Civil 3D, QGIS u otra aplicación de escritorio y registra cómo ejecutarlas allí. Un chequeo de sintaxis o una prueba sin aplicación anfitriona no demuestra que el flujo BIM completo funciona.
- Informa qué comprobaciones pasaron, fallaron o quedaron sin ejecutar, junto con errores, advertencias y limitaciones. No afirmes que una automatización, exportación o integración funciona sin haberla probado.

## Documentación de cada proyecto

Incluye, cuando corresponda, un README con:

- Objetivo de la automatización.
- Software, API, intérprete y versiones compatibles verificadas.
- Requisitos y dependencias.
- Instrucciones de instalación y ejecución.
- Parámetros y formatos de entrada y salida.
- Ejemplos prácticos con datos seguros, cuando existan.
- Procedimiento de validación y pasos manuales necesarios.
- Limitaciones conocidas.

Conserva el idioma y el estilo de la documentación existente; redacta la nueva documentación en español claro. Evita duplicar instrucciones generales si basta un enlace al README de la categoría.

## Comunicación

Responde en español y explica brevemente las decisiones técnicas. Diferencia los cambios realizados de las recomendaciones pendientes. Solicita aclaraciones solo cuando falten requisitos técnicos esenciales que no puedan inferirse del proyecto.
