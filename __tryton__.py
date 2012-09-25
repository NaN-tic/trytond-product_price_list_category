#This file is part product_price_list_category module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
{
    'name': 'Product Price List Category',
    'name_ca_ES': 'Tarifes de producte per categoria',
    'name_es_ES': 'Tarifas de producto por categoría',
    'version': '2.4.0',
    'author': 'Zikzakmedia',
    'email': 'zikzak@zikzakmedia.com',
    'website': 'http://www.zikzakmedia.com/',
    'description': '''Define price list rules by category.''',
    'description_ca_ES': '''Defineix regles de tarifa per categoria.''',
    'description_es_ES': 'Define reglas de tarifa por categoría.',
    'depends': [
        'ir',
        'res',
        'product_price_list',
    ],
    'xml': [
        'price_list.xml',
    ],
    'translation': [
        'locale/ca_ES.po',
        'locale/es_ES.po',
    ]
}
