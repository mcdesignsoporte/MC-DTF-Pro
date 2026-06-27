from pathlib import Path
from PIL import Image


def save_png(img: Image.Image, path: Path, dpi: int = 300) -> None:
    img.save(path, dpi=(dpi, dpi))


def save_pdf(img: Image.Image, path: Path, dpi: int = 300, white_background: bool = True) -> None:
    if white_background:
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.getchannel("A"))
    else:
        bg = img.convert("RGB")

    bg.save(path, "PDF", resolution=dpi)
