# This file is part of the product_price_list_category module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['PriceList', 'PriceListLine']


class PriceList:
    __metaclass__ = PoolMeta
    __name__ = 'product.price_list'

    def compute(self, party, product, unit_price, quantity, uom,
            pattern=None):
        if pattern is None:
            pattern = {}
        if product:
            pattern['category'] = product.category and product.category.id or None
        return super(PriceList, self).compute(party, product, unit_price,
            quantity, uom, pattern)


class PriceListLine:
    __metaclass__ = PoolMeta
    __name__ = 'product.price_list.line'
    category = fields.Many2One('product.category', 'Category')
