import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps

from services.config import MAX_PIXELS, AI_MAX_SIDE


def open_image(path):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    img.load()

    if img.width * img.height > MAX_PIXELS:
        raise ValueError("La imagen es demasiado grande. Reduce tamaño antes de subirla.")

    return img.convert("RGBA")


def resize_for_ai(img: Image.Image, max_side: int = AI_MAX_SIDE) -> Image.Image:
    img = img.copy()
    w, h = img.size

    if max(w, h) <= max_side:
        return img

    scale = max_side / max(w, h)
    new_size = (int(w * scale), int(h * scale))
    return img.resize(new_size, Image.Resampling.LANCZOS)


def remove_background(img: Image.Image) -> Image.Image:
    try:
        from rembg import remove
        return remove(img).convert("RGBA")
    except Exception as exc:
        print(f"Aviso: rembg falló o no está disponible: {exc}", flush=True)
        fallback = img.convert("RGBA")
        fallback.putalpha(Image.new("L", fallback.size, 255))
        return fallback


def clean_alpha(img: Image.Image, alpha_cut: int = 80, despeckle_area: int = 3, edge_contract: int = 0) -> Image.Image:
    arr = np.array(img.convert("RGBA"))
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    alpha = np.where(alpha >= alpha_cut, 255, 0).astype(np.uint8)

    kernel = np.ones((3, 3), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel, iterations=1)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel, iterations=1)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(alpha, 8)
    cleaned = np.zeros_like(alpha)

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= despeckle_area:
            cleaned[labels == i] = 255

    alpha = cleaned

    if edge_contract > 0:
        kernel2 = np.ones((3, 3), np.uint8)
        alpha = cv2.erode(alpha, kernel2, iterations=edge_contract)

    arr[:, :, :3] = rgb
    arr[:, :, 3] = alpha
    return Image.fromarray(arr, "RGBA")


def add_print_canvas(img: Image.Image, width_cm: float, height_cm: float, dpi: int = 300) -> Image.Image:
    if width_cm <= 0 or height_cm <= 0:
        return img

    px_w = int(width_cm / 2.54 * dpi)
    px_h = int(height_cm / 2.54 * dpi)

    if px_w <= 0 or px_h <= 0:
        return img

    working = img.copy()
    working.thumbnail((px_w, px_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (px_w, px_h), (255, 255, 255, 0))
    x = (px_w - working.width) // 2
    y = (px_h - working.height) // 2
    canvas.alpha_composite(working, (x, y))
    return canvas


def upscale_and_sharpen(img: Image.Image, scale: int = 1) -> Image.Image:
    scale = max(1, min(int(scale), 4))

    if scale > 1:
        img = img.resize((img.width * scale, img.height * scale), Image.Resampling.LANCZOS)

    return img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))


def make_halftone(img: Image.Image, dot_size: int = 8, angle: float = 15, invert: bool = False) -> Image.Image:
    rgba = img.convert("RGBA")
    alpha = np.array(rgba)[:, :, 3]

    base = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    base.alpha_composite(rgba)
    gray = ImageOps.grayscale(base)

    rotated = gray.rotate(angle, expand=True, fillcolor=255)
    w, h = rotated.size
    pixels = np.array(rotated)
    draw_arr = np.ones((h, w), dtype=np.uint8) * 255
    step = max(4, int(dot_size))

    for y in range(0, h, step):
        for x in range(0, w, step):
            block = pixels[y:min(y + step, h), x:min(x + step, w)]
            if block.size == 0:
                continue

            darkness = 255 - float(block.mean())
            radius = (darkness / 255.0) * (step / 2)
            bh, bw = block.shape
            yy, xx = np.ogrid[:bh, :bw]
            mask = (yy - bh / 2) ** 2 + (xx - bw / 2) ** 2 <= radius ** 2
            draw_arr[y:y + bh, x:x + bw][mask] = 0

    out = Image.fromarray(draw_arr, "L")
    out = out.rotate(-angle, expand=True, fillcolor=255)

    left = (out.width - img.width) // 2
    top = (out.height - img.height) // 2
    out = out.crop((left, top, left + img.width, top + img.height))

    if invert:
        out = ImageOps.invert(out)

    black = Image.new("RGBA", img.size, (0, 0, 0, 255))
    transparent = Image.new("RGBA", img.size, (0, 0, 0, 0))
    mask = ImageOps.invert(out) if not invert else out
    result = Image.composite(black, transparent, mask)
    result.putalpha(Image.fromarray(alpha).point(lambda p: 255 if p > 0 else 0))
    return result
