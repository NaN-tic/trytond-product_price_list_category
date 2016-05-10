# This file is part of the product_price_list_category module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool

from trytond.modules.company.tests import create_company, set_company


class ProductPriceListCategoryTestCase(ModuleTestCase):
    'Test Product Price List Category module'
    module = 'product_price_list_category'

    @with_transaction()
    def test_price_list(self):
        'Test price_list'
        pool = Pool()
        Template = pool.get('product.template')
        Product = pool.get('product.product')
        Category = pool.get('product.category')
        Uom = pool.get('product.uom')
        PriceList = pool.get('product.price_list')


        company = create_company()
        with set_company(company):
            category = Category(name='Category')
            category.save()

            second_category = Category(name='Second Category')
            second_category.save()

            unit, = Uom.search([
                    ('name', '=', 'Unit'),
                    ])

            template = Template(
                name='Test Lot Sequence',
                list_price=Decimal(10),
                cost_price=Decimal(3),
                default_uom=unit,
                )
            template.save()
            product = Product(template=template)
            product.save()

            price_list, = PriceList.create([{
                        'name': 'Default Price List',
                        'lines': [('create', [{
                                        'category': category.id,
                                        'formula': '12.0',
                                        }, {
                                        'category': second_category.id,
                                        'formula': '14.0',
                                        }, {
                                        'formula': '15.0',
                                        }])],
                        }])
            self.assertEqual(
                price_list.compute(None, product, product.list_price, 1.0,
                    unit),
                Decimal(15.0))
            # Add to second category
            template.categories = [second_category]
            template.save()
            self.assertEqual(
                price_list.compute(None, product, product.list_price, 1.0,
                    unit),
                Decimal(14.0))
            # Add to both categories
            template.categories = [category, second_category]
            template.save()
            self.assertEqual(
                price_list.compute(None, product, product.list_price, 1.0,
                    unit),
                Decimal(12.0))


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPriceListCategoryTestCase))
    return suite
