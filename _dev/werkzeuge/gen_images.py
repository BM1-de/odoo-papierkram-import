#!/usr/bin/env python3
# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Banner and icon of the three modules (static/description).

In English, as the Odoo Apps Store requires, and in the style of l10n_de_euer.
Runs inside the Odoo container, which has Pillow and the DejaVu fonts::

    docker compose run --rm --no-deps -T --entrypoint python3 odoo - \
        < _dev/werkzeuge/gen_images.py
"""

# pylint: disable=print-used

from PIL import Image, ImageDraw, ImageFont

ROOT = "/mnt/extra-addons/"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DARK, LIGHT, ACCENT, WHITE = (
    (31, 58, 96),
    (233, 239, 247),
    (52, 120, 184),
    (255, 255, 255),
)

#: module, label of the icon, rows of the banner (title, two lines, footer)
MODULES = (
    (
        "l10n_de_papierkram_import",
        "Import",
        (
            "Papierkram → Odoo",
            "Contacts, invoices, vouchers, payments, fixed assets",
            "the complete history or only the open items",
            "Odoo 19 · from the Papierkram exports · SKR03 and SKR04",
        ),
    ),
    (
        "l10n_de_papierkram_import_euer",
        "EÜR",
        (
            "Papierkram → EÜR",
            "Fixed assets with their book value at the takeover date",
            "straight into the asset register of the Anlage AVEÜR",
            "Odoo 19 · with Papierkram Import and Germany EÜR",
        ),
    ),
    (
        "l10n_de_papierkram_import_timesheet",
        "Time",
        (
            "Papierkram → Timesheets",
            "Products, time entries and unbilled work",
            "one sales order per customer, invoiced in Odoo",
            "Odoo 19 · with Papierkram Import and Timesheets",
        ),
    ),
)


def fitted(draw, text, path, size, width):
    """Font of at most ``size`` points whose ``text`` fits into ``width``."""
    while size > 10:
        font = ImageFont.truetype(path, size)
        if draw.textlength(text, font=font) <= width:
            return font
        size -= 1
    return ImageFont.truetype(path, size)


def icon(out, label):
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=40, fill=DARK)
    # a sheet with lines and an arrow pointing out of it
    draw.rounded_rectangle((40, 36, 176, 220), radius=10, fill=WHITE)
    for y in (64, 86, 108, 130):
        draw.rectangle((58, y, 158, y + 8), fill=LIGHT)
    draw.polygon(
        (
            (150, 78),
            (186, 78),
            (186, 52),
            (232, 97),
            (186, 142),
            (186, 116),
            (150, 116),
        ),
        fill=ACCENT,
    )
    font = fitted(draw, label, BOLD, 40, 124)
    width = draw.textlength(label, font=font)
    draw.text((40 + (136 - width) / 2, 164), label, font=font, fill=DARK)
    img.resize((128, 128), Image.LANCZOS).save(out + "icon.png", optimize=True)


def banner(out, rows):
    width, height = 1120, 560
    margin = 80
    img = Image.new("RGB", (width, height), DARK)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, height - 120, width, height), fill=ACCENT)
    title, first, second, footer = rows
    for text, path, size, color, top in (
        (title, BOLD, 84, WHITE, 100),
        (first, REGULAR, 38, LIGHT, 240),
        (second, REGULAR, 38, LIGHT, 300),
        (footer, REGULAR, 30, WHITE, height - 82),
    ):
        font = fitted(draw, text, path, size, width - 2 * margin)
        draw.text((margin, top), text, font=font, fill=color)
    img.save(out + "banner.png", optimize=True)


for module, label, rows in MODULES:
    out = ROOT + module + "/static/description/"
    icon(out, label)
    banner(out, rows)
print("ok")
