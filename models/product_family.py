from odoo import api, fields, models

class ProductFamily(models.Model):

    _name = 'product.family'
    _description = 'Famille de produit'

    code_family = fields.Char(string='Code Famille', required=True)
    name = fields.Char(string="Nom de la famille", required=True)
    rayon_id = fields.Many2one('product.rayon', string="Rayon", required=True, ondelete='restrict')