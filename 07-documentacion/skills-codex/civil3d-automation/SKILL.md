---
name: civil3d-automation
description: Desarrollar, revisar, ejecutar, depurar y optimizar automatizaciones de Autodesk Civil 3D para ingeniería civil e infraestructura. Usar para Dynamo/Python, AutoLISP/Visual LISP, C# con Civil 3D o AutoCAD .NET API, COM/ActiveX compatible y scripts SCR, incluyendo objetos civiles, DWG, CSV, LandXML, metrados y reportes.
---

# Automatización Civil 3D

## Revisar contexto y alcance

- Leer `~/.codex/AGENTS.md`, el AGENTS.md del repositorio y las instrucciones locales aplicables. Respetar su precedencia y la autorización del usuario; esta skill aporta criterios técnicos sin reemplazarlas.
- Inspeccionar Git, código, README y pruebas pertinentes antes de modificar. Reutilizar implementaciones existentes, preservar funciones ajenas al cambio y evitar refactorizaciones no solicitadas.
- En `Juanca0795/automatizacion-bim`, consultar `02-civil-3d/README.md` y `06-automatizaciones/README.md`. Guardar proyectos específicos en `02-civil-3d/`, Dynamo de Civil 3D en su subcategoría prevista cuando exista un proyecto real y solo utilidades compartidas en `06-automatizaciones/`. No usar sus directorios históricos como destino de nuevos grafos de plataforma.
- Mantener esta skill separada de los scripts ejecutables. Su copia versionada corresponde a `07-documentacion/skills-codex/civil3d-automation/` y la operativa a `~/.codex/skills/civil3d-automation/`. No copiar proyectos dentro de la skill ni modificar otras skills o AGENTS.md.
- Identificar versión y actualización de Civil 3D, objetivo, objetos de entrada, salida esperada, entorno disponible y código previo. Reutilizar información conocida; preguntar solo por requisitos indispensables. Crear instrucciones de skill no exige que ya exista un script ni conocer una versión concreta.
- Antes de producir código dependiente de versión, verificar API, entorno e interoperabilidad mediante instalación, referencias locales o documentación oficial de Autodesk correspondiente. Distinguir requisito de compatibilidad verificada; no presentar documentación consultada como prueba de ejecución.

## Elegir tecnología

Usar la opción que cumpla el objetivo con el entorno y las capacidades comprobadas. Si alternativas cambian significativamente el trabajo, explicar brevemente la elección y resolver la preferencia antes de implementar varias soluciones.

| Tecnología | Preferir para | Verificar antes de generar y ejecutar |
| --- | --- | --- |
| Dynamo y nodo Python | Flujos visuales y automatización en el contexto de Civil 3D | Versiones de Civil 3D/Dynamo, motor Python real, paquetes, nodos y acceso a API disponibles. |
| AutoLISP / Visual LISP | Rutinas interactivas y comandos sobre el dibujo | Funciones disponibles, soporte del objeto civil y, si se usa, acceso ActiveX de esa versión. |
| C# y Civil 3D .NET API | Herramientas mantenibles con acceso a objetos civiles | SDK/ensamblados instalados, runtime y framework objetivo, arquitectura y miembros públicos disponibles. |
| AutoCAD .NET API | Entidades y servicios de base del dibujo | Qué parte requiere Civil 3D; una entidad AutoCAD no equivale a un objeto civil especializado. |
| COM/ActiveX | Integraciones existentes o capacidades expuestas comprobadas | Registro, versión, ProgID, bitness, interfaces y propiedades realmente disponibles. |
| SCR y comandos nativos | Secuencias deterministas de comandos accesibles por línea | Nombres, opciones, idioma, estado inicial y disponibilidad de alternativas sin diálogos. |
| Python externo | Cálculos, CSV u orquestación con un puente explícito | Intérprete, puente compatible, dependencias y contexto real. No asumir acceso directo al DWG o API administrada. |

- Leer [references/tecnologias-y-validacion.md](references/tecnologias-y-validacion.md) al implementar una tecnología, trabajar con objetos civiles o planificar pruebas de anfitrión.
- No inventar métodos, comandos, nodos, wrappers, ProgID o versiones. No sustituir un objeto civil por geometría AutoCAD si se pierden relaciones o semántica sin acordar ese resultado.
- No instalar paquetes, runtimes ni dependencias sin autorización. Respetar configuración y bloqueos del proyecto.

## Implementar y entregar

- Centralizar parámetros editables al inicio o en una configuración identificada, con secciones **CONFIGURACIÓN** y **EJECUCIÓN** adaptadas al lenguaje. En Dynamo, agrupar nodos de entrada con nombres, unidades, tipos, formatos y valores permitidos; documentar `IN` y `OUT` del nodo Python.
- Priorizar dibujo activo y objetos cargados/seleccionados. Validar documento, base de datos, documento civil, identidad y tipo de objeto antes de operar. No pedir una ruta al DWG activo; pedir rutas únicamente para entradas externas, exportaciones o ejecución de archivos guardados.
- Validar unidades lineales/angulares, CRS, orden de ejes, UCS/WCS, elevaciones y progresivas según el flujo. No asumir que coordenadas numéricas, INSUNITS o una etiqueta UTM definen por sí solos el sistema de referencia ni que todas las funciones usan las mismas unidades.
- Mantener estilos y estándares existentes. Resolver nombres de forma inequívoca y comprobar relaciones entre objetos, referencias externas y capacidad de escritura. No reparar, reconstruir, reasignar ni sincronizar objetos fuera del alcance autorizado.
- Separar cálculos y validación de datos de los adaptadores que acceden a Civil 3D cuando aporte claridad o permita pruebas independientes. No convertir una corrección puntual en una reorganización.
- Mostrar mensajes claros de inicio, cantidades previstas, resultado, advertencias y error. Explicar la causa probable de un fallo con la evidencia disponible, distinguiendo hipótesis de diagnóstico confirmado.
- Entregar el código completo actualizado cuando se soliciten correcciones, salvo petición expresa de fragmentos o únicamente un prompt. Incluir requisitos, configuración y procedimiento exacto de ejecución, comando o punto de entrada y resultado esperado.
- Ofrecer ejecución directa cuando el entorno lo admita y mediante archivo externo como alternativa. No presentar Python genérico como pegable en la línea de comandos de Civil 3D, ni C# como ejecutable sin compilar y cargar. Si la tecnología exige archivo o compilación, explicarlo.
- Documentar en el README del proyecto objetivo, software/API/intérprete, versiones verificadas, dependencias, entradas/salidas, ejemplos seguros, uso directo/externo, limitaciones y validación manual. Enlazar convenciones comunes en vez de copiarlas.

## Proteger dibujos y datos

- No modificar DWG originales sin autorización. Para operaciones destructivas, recomendar copia de trabajo y presentar objetos, propiedades y destinos afectados antes de aplicar. Preferir informe o previsualización cuando aún no esté autorizado el cambio.
- No eliminar objetos, capas, estilos, Property Sets ni propiedades, sobrescribir archivos o guardar automáticamente sin autorización suficiente. No repetir confirmaciones de acciones ya autorizadas; conservar las salvaguardas funcionales existentes.
- Usar transacciones y bloqueo de documento según contexto y API; no imponer bloqueos o gestores de transacciones de otra tecnología. No guardar/revertir trabajo ajeno ni considerar una transacción como reversión de archivos exportados o cambios COM externos.
- Ante un fallo, revertir lo propio cuando sea posible, liberar recursos/restaurar estado y comunicar resultados parciales o incertidumbre. No afirmar atomicidad de un lote sin comprobar sus efectos.
- No activar Dynamo en modo automático para un flujo que escriba repetidamente sin control. Evitar duplicados al repetir ejecuciones; definir qué se crea, actualiza o conserva y cómo se identifica.
- Optimizar solo dentro del alcance solicitado o cuando sea necesario para completarlo: filtrar objetos, reducir cruces COM/API, cachear consultas estables, diferir reconstrucciones con autorización y medir antes/después con datos comparables. No paralelizar acceso a objetos de AutoCAD/Civil 3D suponiendo que su API es segura entre hilos; aislar cálculos puros cuando corresponda.

## Validar y cerrar

- Ejecutar pruebas existentes pertinentes y comprobaciones estáticas con herramientas disponibles. Comprobar lógica independiente, conversiones, archivos de entrada y casos de error con datos seguros. Usar dobles de API solo identificándolos como simulaciones.
- Compilar C# únicamente si existen runtime, SDK y referencias adecuados; no instalar ni descargar para hacerlo sin autorización. Una compilación correcta no prueba funcionamiento dentro de Civil 3D.
- Registrar qué pruebas requieren Civil 3D y ejecutarlas solo cuando exista un entorno autorizado. Si no se dispone de él, dejarlas pendientes; no afirmar compatibilidad, funcionamiento ni resultados de metrados sin evidencia.
- Revisar Git al finalizar e informar archivos creados/modificados/eliminados, comprobaciones aprobadas/fallidas/pendientes y límites de validación. No crear repositorios, hacer commits, push ni publicar sin autorización explícita; antes de sincronizar, mostrar archivos afectados y solicitar aprobación.
