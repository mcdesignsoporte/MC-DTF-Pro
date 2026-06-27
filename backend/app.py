from pathlib import Path
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for

from services.config import BASE_DIR, OUTPUT_DIR, UPLOAD_DIR, APP_SECRET, MAX_UPLOAD_MB
from services.pipeline import process_image
from services.validators import allowed_file

app = Flask(__name__)
app.secret_key = APP_SECRET
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files.get("image")

        if not file or file.filename == "":
            flash("Sube una imagen antes de procesar.")
            return redirect(url_for("index"))

        if not allowed_file(file.filename):
            flash("Formato no permitido. Usa PNG, JPG, JPEG, WEBP, BMP o TIFF.")
            return redirect(url_for("index"))

        try:
            result = process_image(file=file, form=request.form)
        except Exception as exc:
            flash(f"Error al procesar: {exc}")
            return redirect(url_for("index"))

    return render_template("index.html", result=result)


@app.route("/outputs/<filename>")
def outputs(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


@app.route("/health")
def health():
    return {"status": "ok", "app": "MC DTF Pro", "version": "1.0.0"}


if __name__ == "__main__":
    print("MC DTF Pro v1.0 iniciado", flush=True)
    print("Abrir: http://127.0.0.1:5000", flush=True)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
