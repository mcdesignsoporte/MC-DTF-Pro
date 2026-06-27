# Changelog

## v1.1.0 - Performance Release

### Added
- Caché de sesión `rembg` para evitar cargar el modelo en cada imagen.
- Modelo ligero `u2netp` para procesamiento local más rápido.
- Opción para saltar IA si el PNG ya tiene fondo transparente.
- Tiempo total de procesamiento en la interfaz.
- Logs por etapa con duración.
- Servidor Flask con `threaded=True`.

### Changed
- `AI_MAX_SIDE` bajó de 1800 a 1400 px para acelerar IA local.
- Limpieza alpha más conservadora para no destruir detalles finos.
- PDF sigue siendo opcional para evitar procesamiento pesado innecesario.
- Versión actualizada a 1.1.0.

### Notes
- La primera imagen puede tardar más porque carga el modelo IA.
- La segunda imagen en adelante debe ser más rápida gracias al caché.
