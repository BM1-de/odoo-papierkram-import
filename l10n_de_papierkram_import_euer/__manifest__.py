# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Papierkram EÜR Assets",
    "summary": "Take over the fixed assets of Papierkram into the EÜR asset register",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "website": "https://github.com/BM1-de/odoo-papierkram-import",
    "author": "Baumgärtner Marketing GmbH",
    "maintainers": ["bm1-phillip"],
    "license": "AGPL-3",
    "development_status": "Alpha",
    "depends": ["l10n_de_papierkram_import", "l10n_de_euer"],
    "data": ["views/papierkram_import_views.xml"],
    "auto_install": True,
    "images": ["static/description/banner.png"],
    "installable": True,
}
