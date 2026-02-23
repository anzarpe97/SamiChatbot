import unittest
from bot.utils.helpers import format_currency

class TestCurrencyHelpers(unittest.TestCase):
    def test_format_currency_usd(self):
        self.assertEqual(format_currency(100, "USD"), "$100.00")

    def test_format_currency_eur(self):
        self.assertEqual(format_currency(50, "EUR"), "€50.00")

    def test_format_currency_unknown(self):
        self.assertEqual(format_currency(10, "XYZ"), "XYZ10.00")

if __name__ == '__main__':
    unittest.main()
