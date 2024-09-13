{
    'name': 'Champs Additionnel au Produit',
    'version': '1.0.0',
    'category': 'Product',
    'summary': 'Ajouter des champs supplémentaires au modèle de produit',
    'description': 'Ce module ajoute les champs suivants au modèle de produits: Sous-famille, Famille, Rayon.',
    'author': 'INOV CAMEROON',
    'website': 'https://inov.cm',
    'depends': ['base','sale','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_additional_fields_views.xml',
        'views/product_sub_family_views.xml',
        'views/product_family_views.xml',
        'views/product_rayon_views.xml',
        'views/menu.xml',
        'views/internal_reference_sequence_view.xml'
    ],
    'installable': True,
    'application': True,
}
