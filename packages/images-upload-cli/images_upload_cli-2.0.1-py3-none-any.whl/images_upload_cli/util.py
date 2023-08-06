#!/usr/bin/env python
"""Utils."""

from io import BytesIO
from os import getenv
from pathlib import Path
from shutil import which
from subprocess import Popen

import click
from PIL import Image, ImageDraw, ImageFont


class GetEnvError(Exception):
    """Exception raised for getenv errors."""


def get_config_path() -> Path:
    """Get app config path."""
    return Path(f"{click.get_app_dir('images-upload-cli')}/.env")


def get_env(key: str) -> str:
    """Get environment variable or raise an error."""
    if value := getenv(key):
        return value

    msg = f"Please setup {key} in environment variables or in '{get_config_path()}'."
    raise GetEnvError(msg)


def human_size(num: float, suffix: str = "B") -> str:
    """Convert bytes to human readable units."""
    round_num = 1024.0
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < round_num:
            return f"{num:3.1f} {unit}{suffix}"
        num /= round_num
    return f"{num:.1f} Yi{suffix}"


def get_img_ext(img: bytes) -> str:
    """Get image extension from bytes."""
    return Image.open(BytesIO(img)).format.lower()


def get_font(size: int = 14) -> ImageFont.FreeTypeFont:
    """Get caption font."""
    return (
        ImageFont.truetype(font_name, size=size)
        if (font_name := getenv("CAPTION_FONT"))
        else get_default_font()
    )


def get_default_font(size: int = 14) -> ImageFont.FreeTypeFont:
    """Attempt to retrieve a reasonably-looking TTF font from the system."""
    font_names = [
        "Helvetica",
        "NotoSerif-Regular",
        "Menlo",
        "DejaVuSerif",
        "arial",
    ]

    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size=size)
        except OSError:  # noqa: PERF203
            continue

    msg = (
        f"None of the default fonts were found: {font_names}.\n"
        f"Please setup CAPTION_FONT in environment variables or in '{get_config_path()}'.",
    )  # pragma: no cover
    raise GetEnvError(msg)  # pragma: no cover


def make_thumbnail(
    img: bytes,
    font: ImageFont.FreeTypeFont,
    size: tuple[int, int] = (300, 300),
) -> bytes:
    """Make this image into a captioned thumbnail."""
    # get a pw
    im = Image.open(BytesIO(img))
    pw = im.copy().convert("RGB")
    pw.thumbnail(size=size, resample=Image.Resampling.LANCZOS)

    # make a blank image for the text
    pw_with_line = Image.new(
        mode="RGB",
        size=(pw.width, pw.height + 16),
        color=(255, 255, 255),
    )
    pw_with_line.paste(pw, box=(0, 0))

    # get a file size info
    fsize = human_size(len(img))

    # draw text
    d = ImageDraw.Draw(pw_with_line)
    d.text(
        xy=(pw.width / 5, pw.height),
        text=f"{im.width}x{im.height} ({im.format}) [{fsize}]",
        font=font,
        fill=(0, 0, 0),
    )

    # save to buffer
    buffer = BytesIO()
    pw_with_line.save(
        buffer,
        format="JPEG",
        quality=95,
        optimize=True,
        progressive=True,
    )

    return buffer.getvalue()


def notify_send(text_to_print: str) -> None:
    """Send desktop notifications via libnotify."""
    if notify_send := which("notify-send"):
        Popen([notify_send, "-a", "images-upload-cli", text_to_print])  # pragma: no cover
