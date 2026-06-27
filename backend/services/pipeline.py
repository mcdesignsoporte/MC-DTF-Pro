import uuid

from services.config import UPLOAD_DIR, OUTPUT_DIR
from services.exporters import save_pdf, save_png
from services.image_ops import (
    add_print_canvas,
    clean_alpha,
    make_halftone,
    open_image,
    remove_background,
    resize_for_ai,
    upscale_and_sharpen,
)


def _int(form, key, default):
    try:
        return int(form.get(key, default))
    except Exception:
        return default


def _float(form, key, default):
    try:
        return float(form.get(key, default) or default)
    except Exception:
        return default


def process_image(file, form):
    job_id = uuid.uuid4().hex[:10]
    ext = file.filename.rsplit(".", 1)[1].lower()
    input_path = UPLOAD_DIR / f"{job_id}_original.{ext}"
    file.save(input_path)

    alpha_cut = _int(form, "alpha_cut", 80)
    despeckle_area = _int(form, "despeckle_area", 3)
    edge_contract = _int(form, "edge_contract", 0)
    upscale = _int(form, "upscale", 1)
    dpi = _int(form, "dpi", 300)
    width_cm = _float(form, "width_cm", 0)
    height_cm = _float(form, "height_cm", 0)
    generate_pdf = form.get("generate_pdf") == "on"
    halftone_enabled = form.get("halftone") == "on"
    dot_size = _int(form, "dot_size", 8)
    angle = _float(form, "angle", 15)
    invert = form.get("invert") == "on"

    print("1. Abriendo imagen", flush=True)
    img = open_image(input_path)

    print("2. Redimensionando para IA", flush=True)
    ai_img = resize_for_ai(img)

    print("3. Quitando fondo con IA", flush=True)
    removed = remove_background(ai_img)

    print("4. Limpiando alpha y basura", flush=True)
    cleaned = clean_alpha(removed, alpha_cut, despeckle_area, edge_contract)

    print("5. Preparando medida de impresión", flush=True)
    final_img = add_print_canvas(cleaned, width_cm, height_cm, dpi)

    print("6. Reescalando", flush=True)
    final_img = upscale_and_sharpen(final_img, upscale)

    png_name = f"{job_id}_dtf_limpio.png"
    pdf_name = f"{job_id}_dtf_limpio.pdf" if generate_pdf else None
    png_path = OUTPUT_DIR / png_name

    print("7. Guardando PNG", flush=True)
    save_png(final_img, png_path, dpi)

    if generate_pdf:
        print("8. Guardando PDF", flush=True)
        save_pdf(final_img, OUTPUT_DIR / pdf_name, dpi)

    halftone_name = None
    halftone_pdf_name = None

    if halftone_enabled:
        print("9. Generando semitono", flush=True)
        ht = make_halftone(final_img, dot_size=dot_size, angle=angle, invert=invert)
        halftone_name = f"{job_id}_semitono.png"
        halftone_pdf_name = f"{job_id}_semitono.pdf" if generate_pdf else None
        save_png(ht, OUTPUT_DIR / halftone_name, dpi)
        if generate_pdf:
            save_pdf(ht, OUTPUT_DIR / halftone_pdf_name, dpi)

    print("10. Terminado", flush=True)

    return {
        "png": png_name,
        "pdf": pdf_name,
        "halftone": halftone_name,
        "halftone_pdf": halftone_pdf_name,
        "size": f"{final_img.width} × {final_img.height}px",
    }
