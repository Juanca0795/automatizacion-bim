# Tecnologías y validación en Civil 3D

Leer solo los apartados correspondientes al flujo solicitado. Estas comprobaciones orientan la implementación; no constituyen compatibilidad verificada de ninguna versión.

## Procedimiento por tecnología

- **Dynamo/Python:** abrir Dynamo desde Civil 3D en el dibujo de trabajo, confirmar versiones y motor, revisar paquetes instalados y seleccionar ejecución manual durante pruebas. Proporcionar grafo o instrucciones completas de nodos, conexiones y entradas; pegar Python en el nodo del motor declarado, conectar entradas y revisar OUT/diagnósticos tras ejecutar. Si se entrega un `.py` externo, explicar el cargador real del nodo, rutas y paso de parámetros: un archivo Python por sí solo no es un grafo Dynamo. Distinguir wrappers de Dynamo de objetos .NET y documentar cualquier conversión. Elegir transacciones de acuerdo con el contexto real, no copiar gestores de Revit.
- **AutoLISP/Visual LISP:** definir un comando `c:NOMBRE` y explicar cómo invocarlo. Ofrecer pegado de expresiones completas cuando sea adecuado o guardar `.lsp`, cargar mediante APPLOAD o `(load ...)` y ejecutar el nombre del comando. Poner parámetros al inicio de la rutina; no inventar interfaces civiles desde propiedades genéricas de entidades. Usar captura de errores, liberar objetos COM adquiridos cuando corresponda y restaurar variables de sistema propias tanto al terminar como al cancelar. Respetar SECURELOAD y rutas de confianza; no desactivar seguridad para cargar código.
- **C#/.NET:** entregar código completo del comando y configuración de compilación necesaria. Resolver referencias desde la instalación/SDK correspondiente, por ejemplo ensamblados AutoCAD y Civil 3D realmente utilizados, sin fijar rutas ajenas ni mezclar versiones. Verificar framework/runtime, arquitectura y política de copia local; no redistribuir DLL de Autodesk por rutina. Compilar, abrir Civil 3D, cargar la DLL con NETLOAD cuando proceda y ejecutar el comando registrado. Distinguir contexto de comando, modeless, sesión y documento antes de aplicar bloqueos y transacciones. No conservar DBObjects abiertos fuera de su vida útil ni usar ObjectId de otra base de datos.
- **COM/ActiveX:** comprobar instancia concreta de Civil 3D, dibujo y objeto civil, interfaz expuesta y capacidad de escritura. No conectar silenciosamente con otra sesión ni asumir que un ProgID histórico sirve en otra versión. Explicar cómo lanzar el cliente o cargar la rutina anfitriona, qué instancia utilizará y qué ocurre si no existe. No confiar en la reversión de una transacción .NET para cambios hechos por COM.
- **SCR/comandos:** entregar texto completo del `.scr`, configuración inicial identificada con sintaxis válida y secuencia verificada para la versión. Un SCR no admite comentarios o variables arbitrarios como Python; centralizar sus valores literales al inicio cuando el comando lo permita o usar un generador/configuración explícita si se necesita. Guardar `.scr` y ejecutar SCRIPT desde el contexto esperado. Verificar espacios, comillas, respuestas, Enter finales y estado de comandos. Preferir comandos globales/opciones internacionalizadas y variantes por línea cuando estén disponibles, sin inventarlas. Restaurar variables modificadas, no desactivar seguridad ni incluir guardados o borrados no autorizados.
- **Python externo:** identificar por separado intérprete y puente real (por ejemplo interoperabilidad existente), validar instalación y conexión antes de proponer ejecución. Proporcionar comando y parámetros exactos para ese entorno. No afirmar que instalar Python o importar `clr` basta para acceder a Civil 3D.

## Comprobaciones por objeto y salida

| Alcance | Validar según la operación solicitada |
| --- | --- |
| Superficies TIN | Tipo real, datos/triángulos, contornos, huecos, límites de consulta y unidades Z. No extrapolar elevaciones fuera de la cobertura sin criterio explícito. |
| Alineamientos horizontales | Identidad, emplazamiento si corresponde, geometría, sentido, rango y ecuaciones de progresivas. No confundir distancia geométrica con progresiva rotulada. |
| Perfiles longitudinales y rasantes | Alineamiento asociado, tipo de perfil, rango, cotas, pendientes y PVIs/curvas cuando proceda; distinguir perfil de superficie y perfil de diseño. |
| Ensamblajes y subensamblajes | Punto de inserción, lados, unidades, códigos y parámetros; verificar que la API elegida permita consultar o editar la definición requerida. |
| Corredores | Líneas base, perfiles, regiones, ensamblajes, frecuencias, targets, dependencias y estado de reconstrucción; informar qué se reconstruirá. |
| Secciones transversales | Alineamiento, grupo/líneas de muestreo, progresivas, offsets, fuentes muestreadas y distinción entre datos y vistas de sección. |
| Redes de tuberías | Diferenciar redes por gravedad y presión, catálogos/listas de piezas, partes, conectividad, cotas y reglas; verificar capacidades de cada API para el tipo real. |
| Parcelas | Emplazamiento, topología, numeración, área y relaciones; evaluar cambios colaterales dentro del emplazamiento. |
| Puntos COGO | Identificador/número, duplicados, descripción, coordenadas y elevación, grupos y formato de importación; distinguir punto AutoCAD de punto COGO. |
| Etiquetas, estilos y conjuntos de códigos | Tipo y pertenencia del estilo, referencias y dependencias; conservar estándares y distinguir definición de estilo de asignación a un objeto. |
| Property Sets y datos personalizados | Mecanismo real: Property Sets, XData, diccionarios u otro. Verificar ensamblados/API aplicables, definiciones, tipos, unidades, aplicabilidad, valores automáticos y de solo lectura. No tratarlos como mecanismos intercambiables. |
| DWG | Versión, documento/base de datos, referencias externas/de datos, proxies y estado de escritura. No asumir que AutoCAD o una base de datos lateral permiten toda operación civil fuera del anfitrión. |
| CSV | Codificación, delimitador, separador decimal, cabeceras, tipos, ausentes, unidades y orden de coordenadas; validar primero sin escribir en el dibujo. |
| LandXML | Versión/esquema y contenido real, unidades/CRS cuando estén disponibles, capacidades del importador/exportador y pérdida de estilos/relaciones; no prometer ida y vuelta sin pérdidas. |
| Metrados y reportes | Método de cálculo, objetos y rango, unidades, corte/relleno y signos, tolerancias/redondeo y referencias. No equiparar volumen bruto con cantidad pagable sin reglas del proyecto. |

## Evidencia y pruebas

1. Registrar entorno y entrada segura, operación, salida esperada y tolerancias apropiadas. No usar DWG de clientes como datos de prueba sin autorización.
2. Fuera de Civil 3D, ejecutar pruebas existentes y verificar parsers, conversiones, cálculos puros y sintaxis/compilación cuando haya herramientas. No instalar dependencias por rutina. No crear pruebas que solo comprueben el texto de las instrucciones.
3. Dentro de Civil 3D, abrir una copia de trabajo y probar lectura, selección cancelada, objeto ausente/incompatible, documento no editable y entradas inválidas pertinentes. Confirmar que los casos rechazados no cambian el dibujo.
4. Para escrituras autorizadas, comparar cantidades, valores, relaciones, estilos y geometría antes/después; comprobar errores intermedios, estado de transacciones y repetición sin duplicados inesperados. Revisar persistencia al guardar/reabrir solo si ese guardado está autorizado.
5. Para importaciones/exportaciones, validar archivos reales y destinos sin sobrescribir; revisar contenido y pérdidas relevantes. Para metrados, contrastar con un cálculo o reporte de referencia independiente y su tolerancia.
6. Informar por separado validación estática, unitaria e integración. Declarar versiones efectivamente probadas y limitaciones observadas. Si solo se creó esta skill sin código ejecutable, no inventar pruebas unitarias ni resultados de ejecución del anfitrión.
