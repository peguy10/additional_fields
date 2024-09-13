from odoo import models, fields, api, tools
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    international = fields.Boolean(string='International', default=False, store=True)
    sub_family_id = fields.Many2one('product.sub.family', string='Sous-famille', store=True)
    family_id = fields.Many2one('product.family', string='Famille', related='sub_family_id.family_id', readonly=True, store=True)
    rayon_id = fields.Many2one('product.rayon', string='Rayon', related='family_id.rayon_id', readonly=True, store=True)

    @api.model
    def create(self, vals):
        record = super(ProductTemplate, self).create(vals)
        record.generate_internal_reference()
        return record

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if any(field in vals for field in ['international', 'sub_family_id']):
            self.generate_internal_reference()
        return res

    def generate_internal_reference(self):
        for record in self:
            code_achat = '11' if record.international else '10'  # 11 pour international, 10 pour local
            code_rayon = record.rayon_id.code_rayon or '' if record.rayon_id else ''
            code_famille = record.family_id.code_family or '' if record.family_id else ''
            code_sousfamille = record.sub_family_id.code_sub_family or '' if record.sub_family_id else ''

            # Générer un nombre autoincrémenté
            sequence_number = self.env['ir.sequence'].next_by_code('product.internal.reference')

            # Formatage du code final
            if sequence_number:
                default_code = f"{code_achat}{code_rayon}{code_famille}{code_sousfamille}{sequence_number.zfill(4)}"
                record.default_code = default_code  # Mettre à jour le champ default_code
            else:
                record.default_code = f"{code_achat}{code_rayon}{code_famille}{code_sousfamille}0000"  # Valeur par défaut si la séquence échoue

class SaleReport(models.Model):
    _inherit = "sale.report"

    international = fields.Boolean(string='International', default=False, store=True)
    rayon_id = fields.Many2one('product.rayon', string='Rayon', readonly=True)
    family_id = fields.Many2one('product.family', string='Famille', readonly=True)
    sub_family_id = fields.Many2one('product.sub.family', string='Sous-famille', readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['rayon_id'] = "t.rayon_id"
        res['family_id'] = "t.family_id"
        res['sub_family_id'] = "t.sub_family_id"
        res['international'] = "t.international"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            t.rayon_id,
            t.family_id,
            t.sub_family_id,
            t.international"""
        return res

class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    international = fields.Boolean(string='International', default=False, store=True)
    rayon_id = fields.Many2one('product.rayon', string='Rayon', readonly=True)
    family_id = fields.Many2one('product.family', string='Famille', readonly=True)
    sub_family_id = fields.Many2one('product.sub.family', string='Sous-famille', readonly=True)

    def _select(self):
        rec = super()._select()
        rec += """
            , pt.rayon_id AS rayon_id,
            pt.family_id AS family_id,
            pt.sub_family_id AS sub_family_id,
            pt.international AS international
        """
        return rec

    def _group_by(self):
        rec = super()._group_by()
        rec += """,
                pt.rayon_id,
                pt.family_id,
                pt.sub_family_id,
                pt.international
        """
        return rec

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._group_by()))