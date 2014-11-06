#!/usr/bin/env python
# This file is part product_price_list_category module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends


class ProductPriceListCategoryTestCase(unittest.TestCase):
    'Test Product PriceList Category module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('product_price_list_category')

    def test0005views(self):
        'Test views'
        test_view('product_price_list_category')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPriceListCategoryTestCase))
    return suite
