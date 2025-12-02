""""
Sample tests  
"""

from django.test import SimpleTestCase

from app import calc

class CalcTests(SimpleTestCase):
    """Tests for calc.py"""

    def test_add_numbers(self):
        """Test adding numbers together"""
        res = calc.add(3, 8)

        self.assertEqual(res, 11)

