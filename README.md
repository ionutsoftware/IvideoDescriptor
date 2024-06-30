# Descripción de Video para Personas con Discapacidad Visual

Este programa utiliza la API de OpenAI para proporcionar descripciones detalladas y concisas de videos, facilitando la comprensión de su contenido a personas con discapacidad visual.

## ¿Para qué sirve?

Este programa está diseñado para analizar videos y generar una descripción detallada y comprensible de su contenido. La descripción se genera usando la inteligencia artificial de OpenAI, y está pensada para ser útil a personas que no pueden ver los videos por sí mismas.

## Cómo usarlo

1. **Preparar la API Key de OpenAI**: 
   - Abre la carpeta que contiene el programa.
   - Busca un archivo llamado `key.json`.
   - Abre `key.json` con un editor de texto y encontrarás algo como esto:
     ```json
     {
         "key": ""
     }
     ```
   - Pega tu clave API de OpenAI entre las comillas:
     ```json
     {
         "key": "tu_clave_api"
     }
     ```

2. **Ejecutar el programa**:
   - Abre el programa y selecciona el video que deseas describir cuando se te solicite.
   - El programa procesará el video y mostrará una descripción generada por la inteligencia artificial.

## Requisitos

- Una clave API de OpenAI válida.
- El archivo `key.json` correctamente configurado con tu clave API.
- Conexión a internet para acceder a la API de OpenAI.

## Ejemplo de uso

1. Ejecuta el programa.
2. Selecciona el video desde la ventana emergente.
3. Espera unos momentos mientras se procesa el video.
4. Aparecerá una ventana con la descripción del contenido del video.

¡Y eso es todo! Ahora tendrás una descripción detallada del video, proporcionada por la inteligencia artificial, que te ayudará a comprender su contenido.

## Notas adicionales

- Este programa está diseñado para ser fácil de usar, incluso para aquellos que no tienen conocimientos técnicos.
- Si tienes alguna duda o encuentras algún problema, no dudes en contactar al desarrollador.

## Cambios:

- Versión 1.0.1.30.6:
  - se limitan los videos a 30 segundos de duración para poder ser procesados por la ia, por una razón de límites. cuando intenté describir un video musical de 2 minutos, lanzó un error de exceso de tokens, por lo cual lo mejor es describir videos cortos.
  - el prompt ya no está en el código, ahora está en el json, y puede ser cambiado o modificado por cualquier persona.
  - Cambié la captura de errores `Exception` ha `OpenAIError`, siendo más precisa la captura de errores. Próximamente se irán aplicando algunas más concretas para obtener códigos de errores más precisos.
