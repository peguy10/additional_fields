from odoo import api, fields, models

class ProductSubFamily(models.Model):

    _name = 'product.sub.family'
    _description = 'Famille de produit'

    code_sub_family = fields.Char(string='Code Sous Famille', required=True)
    name = fields.Char(string="Nom de la sous famille", required=True)
    family_id = fields.Many2one('product.family', string="Famille", required=True, ondelete='restrict')