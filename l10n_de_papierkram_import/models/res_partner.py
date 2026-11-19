# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    papierkram_number = fields.Char(
        copy=False,
        index="btree_not_null",
        help="Customer or supplier number in Papierkram (K-… or L-…).",
    )
    papierkram_is_company = fields.Boolean(
        string="Company in Papierkram",
        copy=False,
        help="Papierkram lists the contact as a company. Odoo regards it as a "
        "company also without VAT number, as long as it belongs to no other "
        "contact.",
    )

    @api.depends("papierkram_is_company", "parent_id")
    def _compute_is_company(self):
        """Odoo 20 regards a contact as a company only with a VAT number; a
        contact that Papierkram lists as a company stays one without it.
        Extension point of Odoo for a refined definition (see the docstring of
        the method in ``base``)."""
        res = super()._compute_is_company()
        for partner in self:
            if partner.papierkram_is_company and not partner.parent_id:
                partner.is_company = True
        return res
