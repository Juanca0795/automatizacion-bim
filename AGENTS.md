# Instrucciones para agentes

## Alcance y estructura

- Trata este repositorio como un espacio compartido para proyectos de automatización BIM. Conserva las áreas existentes y coloca cada cambio en la carpeta de plataforma correspondiente.
- Antes de crear archivos, inspecciona el proyecto y sus instrucciones locales. No inventes automatizaciones, resultados, versiones compatibles ni requisitos.
- Mantén las soluciones modulares: separa lógica independiente de los adaptadores que necesitan Revit, Dynamo, pyRevit, Civil 3D, QGIS, IFC u otros visores.
- Si un área contiene proyectos distintos, agrúpalos en subcarpetas con nombres claros y un README por proyecto. No añadas estructura vacía ni archivos de configuración sin una necesidad concreta.

## Cambios y dependencias

- Conserva el idioma y el estilo de los documentos existentes; para documentación nueva usa español claro.
- No instales ni declares dependencias salvo que la tarea lo requiera. Si hacen falta, identifica el gestor apropiado para ese proyecto, respeta sus archivos de bloqueo y documenta las versiones y pasos de instalación.
- No supongas que el entorno BIM está disponible en el sistema operativo actual. Distingue las comprobaciones que requieren una aplicación anfitriona de las que pueden ejecutarse localmente.
- Protege datos, modelos y archivos del usuario. No elimines ni reemplaces contenido existente sin una instrucción explícita.
- Revisa `git status` antes de terminar y describe los archivos afectados. No afirmes que pruebas, exportaciones o validaciones se ejecutaron si no se ejecutaron.

## Documentación de cada proyecto

Incluye, cuando corresponda, propósito, plataforma y versiones probadas, requisitos, instrucciones de uso, entradas y salidas, y cómo validar el resultado. Registra limitaciones conocidas y pasos manuales necesarios. Evita copiar documentación general si basta un enlace al README del área.
