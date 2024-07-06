import unittest

from pydantic import ValidationError

import app
from app.schemas.external_services_schemas.currency import Currency


class TestCurrencyModel(unittest.TestCase):

    def test_currency(self):
        currency = Currency(base_code="USD", target_code="EUR", conversion=0.85)
        self.assertEqual(currency.base_code, "USD")
        self.assertEqual(currency.target_code, "EUR")
        self.assertEqual(currency.conversion, 0.85)
