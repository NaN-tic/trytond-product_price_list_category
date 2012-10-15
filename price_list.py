#This file is part product_price_list_category module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.tools import safe_eval, datetime_strftime
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta

__all__ = ['PriceList', 'PriceListLine']
__metaclass__ = PoolMeta

class PriceList:
    'Price List'
    __name__ = 'product.price_list'

    def compute(self, party, product, unit_price, quantity, uom,
            pattern=None):
        '''
        Compute price based on price list of party

        :param unit_price: a Decimal for the default unit price in the
            company's currency and default uom of the product
        :param quantity: the quantity of product
        :param uom: a instance of the product.uom
        :param pattern: a dictionary with price list field as key
            and match value as value
        :return: the computed unit price
        '''

        Uom = Pool().get('product.uom')

        if pattern is None:
            pattern = {}

        pattern = pattern.copy()
        pattern['product'] = product and product.id or None
        pattern['category'] = product.category and product.category.id or None
        pattern['quantity'] = Uom.compute_qty(uom, quantity,
                product.default_uom, round=False)

        for line in self.lines:
            if line.match(pattern):
                with Transaction().set_context(
                        self._get_context_price_list_line(party, product,
                            unit_price, quantity, uom)):
                    return line.get_unit_price()
        return unit_price

class PriceListLine:
    __name__ = 'product.price_list.line'

    category = fields.Many2One('product.category', 'Category')
