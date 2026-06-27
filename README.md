# MC DTF Pro v1.1

Herramienta local de MC Creative Studio para preparar imágenes DTF: eliminar fondo, limpiar semitransparencias, quitar píxeles basura y exportar archivos listos para producción.

## Novedades v1.1

- IA más rápida con sesión `rembg` en caché.
- Modelo ligero `u2netp` para uso local.
- Opción para saltar IA cuando el archivo ya trae transparencia.
- Limpieza más conservadora para caricaturas y diseños con detalles finos.
- Tiempo total de proceso visible en la interfaz.
- Logs por etapa en terminal.
- PDF opcional para evitar esperas innecesarias.

## Instalación Windows

Desde la carpeta del proyecto:

```cmd
cd backend
python -m pip install -r requirements.txt
python app.py
```

Abrir en navegador:

```text
http://127.0.0.1:5000
```

## Uso recomendado para rapidez

- Quitar fondo con IA: activado solo si la imagen tiene fondo.
- Alta resolución: Original rápido recomendado.
- PDF: desactivado hasta el final.
- Semitono: desactivado hasta que lo necesites.
- Corte de transparencia: 80.
- Basura menor a: 3.

## Variables de entorno útiles

```cmd
set MC_DTF_AI_MAX_SIDE=1800
set MC_DTF_MAX_UPLOAD_MB=60
```

Si quieres más velocidad, usa un valor menor:

```cmd
set MC_DTF_AI_MAX_SIDE=1200
```

## Estructura

```text
backend/
  app.py
  services/
    config.py
    image_ops.py
    pipeline.py
    exporters.py
    validators.py
  templates/
  static/
docs/
scripts/
tests/
```

## Licencia

Software privado de MC Creative Studio.
