#This file is part product_price_list_category module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.tools import safe_eval, datetime_strftime
from trytond.transaction import Transaction
from trytond.pool import Pool

class PriceList(ModelSQL, ModelView):
    'Price List'
    _name = 'product.price_list'

    def compute(self, price_list, party, product, unit_price, quantity, uom,
            pattern=None):
        '''
        Compute price based on price list of party

        :param price_list: the price list id or the BrowseRecord of the
            product.price_list
        :param party: the party id or the BrowseRecord of the party.party
        :param product: the product id or the BrowseRecord of the
            product.product
        :param unit_price: a Decimal for the default unit price in the
            company's currency and default uom of the product
        :param quantity: the quantity of product
        :param uom: the UOM id or the BrowseRecord of the product.uom
        :param pattern: a dictionary with price list field as key
            and match value as value
        :return: the computed unit price
        '''
        pool = Pool()
        party_obj = pool.get('party.party')
        product_obj = pool.get('product.product')
        uom_obj = pool.get('product.uom')
        price_list_line_obj = pool.get('product.price_list.line')

        if not price_list:
            return unit_price

        if isinstance(price_list, (int, long)):
            price_list = self.browse(price_list)

        if isinstance(party, (int, long)):
            party = party_obj.browse(party)

        if isinstance(product, (int, long)):
            product = product_obj.browse(product)

        if isinstance(uom, (int, long)):
            uom = uom_obj.browse(uom)

        if pattern is None:
            pattern = {}

        pattern = pattern.copy()
        pattern['category'] = product.category and product.category.id or None
        pattern['product'] = product and product.id or None
        pattern['quantity'] = uom_obj.compute_qty(uom, quantity,
                product.default_uom, round=False)
        
        for line in price_list.lines:
            if price_list_line_obj.match(line, pattern):
                with Transaction().set_context(
                        self._get_context_price_list_line(party, product,
                            unit_price, quantity, uom)):
                    return price_list_line_obj.get_unit_price(line)
        return unit_price

PriceList()

class PriceListLine(ModelSQL, ModelView):
    _name = 'product.price_list.line'

    category = fields.Many2One('product.category', 'Category')

PriceListLine()
