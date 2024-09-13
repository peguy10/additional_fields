from odoo import api, fields, models

class ProductRayon(models.Model):

    _name = 'product.rayon'
    _description = 'Rayon de produit'

    code_rayon = fields.Char(string='Code rayon', required=True)
    name = fields.Char(string="Nom du rayon", required=True)