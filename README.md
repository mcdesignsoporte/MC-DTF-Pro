# MC DTF Pro v1.0

Herramienta local de MC Creative Studio para preparar imágenes para producción DTF.

## Funciones v1.0

- Eliminación de fondo con IA usando `rembg`.
- Limpieza de semitransparencias.
- Eliminación de píxeles basura.
- Presets para caricatura, diseño normal y logo fuerte.
- Exportación PNG transparente.
- Exportación PDF opcional.
- Semitonos opcionales.
- Vista previa antes de procesar.
- Flujo más rápido: no genera PDF ni hace upscale si no se solicita.

## Instalación en Windows

Abre CMD dentro de la carpeta del proyecto y ejecuta:

```cmd
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Luego abre:

```text
http://127.0.0.1:5000
```

## Estructura

```text
MC-DTF-Pro-v1.0/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── services/
│   ├── templates/
│   └── static/
├── docs/
├── tests/
├── scripts/
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

## Recomendación de uso

Para diseños con detalles finos usa:

- Preset: Caricatura / detalle fino
- Alta resolución: Original rápido
- PDF: apagado hasta que lo necesites
- Semitonos: apagado hasta que lo necesites

## Próximas versiones

- Procesamiento por lotes.
- Historial de trabajos.
- Editor de máscara.
- Real-ESRGAN para upscale real por IA.
- Login privado.
- Docker/VPS para despliegue en `mccreativestudio.me`.
