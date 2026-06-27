<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MC DTF Pro v1.1</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <div>
        <p class="tag">MC Creative Studio</p>
        <h1>MC DTF Pro</h1>
        <p class="sub">Motor v1.1: IA más rápida, limpieza conservadora, PDF opcional y tiempos de proceso.</p>
      </div>
      <div class="status ok">v{{ app_version }} Local</div>
    </section>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="alert">{{ messages[0] }}</div>
      {% endif %}
    {% endwith %}

    <form method="post" enctype="multipart/form-data" class="card" id="dtfForm">
      <div class="filebox" id="fileBox">
        <input id="imageInput" type="file" name="image" accept="image/png,image/jpeg,image/webp,image/bmp,image/tiff" required>
        <div class="filebox-content">
          <span id="fileText">Seleccionar o arrastrar imagen</span>
          <small>PNG, JPG, WEBP, BMP, TIFF</small>
        </div>
      </div>

      <div id="previewWrap" class="preview-wrap hidden">
        <p>Vista previa original</p>
        <img id="previewImg" alt="Vista previa">
      </div>

      <div class="presets">
        <button type="button" data-preset="soft">Caricatura / detalle fino</button>
        <button type="button" data-preset="normal">Diseño normal</button>
        <button type="button" data-preset="strong">Logo fuerte</button>
      </div>

      <div class="quick-options">
        <label class="check"><input type="checkbox" name="remove_bg" checked> Quitar fondo con IA</label>
        <span class="hint">Desactívalo si tu PNG ya trae fondo transparente.</span>
      </div>

      <div class="grid">
        <label>Corte de transparencia
          <input id="alphaCut" type="number" name="alpha_cut" value="80" min="1" max="254">
          <small>Menor conserva detalles. Mayor elimina halos.</small>
        </label>

        <label>Quitar basura menor a
          <input id="despeckleArea" type="number" name="despeckle_area" value="3" min="1" max="500">
          <small>Para detalles finos usa 2–5.</small>
        </label>

        <label>Contraer borde
          <input id="edgeContract" type="number" name="edge_contract" value="0" min="0" max="4">
          <small>Úsalo solo si queda halo.</small>
        </label>

        <label>Alta resolución
          <select id="upscale" name="upscale">
            <option value="1" selected>Original rápido recomendado</option>
            <option value="2">2x</option>
            <option value="3">3x</option>
            <option value="4">4x pesado</option>
          </select>
        </label>

        <label>DPI
          <input type="number" name="dpi" value="300" min="72" max="600">
        </label>

        <label>Ancho final cm opcional
          <input type="number" name="width_cm" value="0" min="0" step="0.1">
        </label>

        <label>Alto final cm opcional
          <input type="number" name="height_cm" value="0" min="0" step="0.1">
        </label>
      </div>

      <details>
        <summary>Exportación avanzada</summary>
        <div class="grid mt">
          <label class="check"><input type="checkbox" name="generate_pdf"> Generar PDF</label>
          <label class="check"><input type="checkbox" name="halftone"> Crear versión semitono</label>
          <label>Tamaño de punto <input type="number" name="dot_size" value="8" min="4" max="40"></label>
          <label>Ángulo <input type="number" name="angle" value="15" min="0" max="90"></label>
          <label class="check"><input type="checkbox" name="invert"> Invertir semitono</label>
        </div>
      </details>

      <button type="submit" id="processBtn">Procesar imagen</button>
    </form>

    {% if result %}
      <section class="card result">
        <h2>Archivo listo</h2>
        <p>Tamaño final: <strong>{{ result.size }}</strong></p>
        <p>Tiempo de proceso: <strong>{{ result.seconds }}</strong></p>
        <div class="downloads">
          <a href="{{ url_for('outputs', filename=result.png) }}">Descargar PNG transparente limpio</a>
          {% if result.pdf %}<a href="{{ url_for('outputs', filename=result.pdf) }}">Descargar PDF</a>{% endif %}
          {% if result.halftone %}<a href="{{ url_for('outputs', filename=result.halftone) }}">Descargar PNG semitono</a>{% endif %}
          {% if result.halftone_pdf %}<a href="{{ url_for('outputs', filename=result.halftone_pdf) }}">Descargar PDF semitono</a>{% endif %}
        </div>
      </section>
    {% endif %}
  </main>

  <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
