# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Papierkram Timesheets",
    "summary": "Import products, time entries and unbilled work from Papierkram",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "website": "https://github.com/BM1-de/odoo-papierkram-import",
    "author": "Baumgärtner Marketing GmbH",
    "maintainers": ["bm1-phillip"],
    "license": "AGPL-3",
    "development_status": "Alpha",
    "depends": ["l10n_de_papierkram_import", "sale_timesheet"],
    "data": ["views/papierkram_import_views.xml"],
    "auto_install": True,
    "images": ["static/description/banner.png"],
    "installable": True,
}
