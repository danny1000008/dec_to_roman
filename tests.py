import unittest
from number import Number

class decimalTestCase(unittest.TestCase):

    def test_1_is_roman_numeral_I(self):
        test_num = Number(1)
        self.assertTrue(test_num.convert_to_roman() == 'I')

    def test_2000_is_roman_numeral_MM(self):
        test_num = Number(2000)
        self.assertTrue(test_num.convert_to_roman() == 'MM')

    def test_minus_1_is_not_valid_input(self):
        test_num = Number(-1)
        self.assertFalse(test_num.convert_to_roman())

    def test_I_is_decimal_1(self):
        test_num = Number('I', 'roman')
        self.assertTrue(test_num.convert_to_decimal() == 1)

    def test_MM_is_decimal_2000(self):
        test_num = Number('MM', 'roman')
        self.assertTrue(test_num.convert_to_decimal() == 2000)


if __name__ == '__main__':
    unittest.main()
