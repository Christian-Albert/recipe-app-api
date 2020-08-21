from django.test import TestCase

from app.calc import add, subtract

class CalcTest(TestCase):

    def test_add_numbers(self):
        '''Test that two numbers are added together'''
        self.assertEqual(add(4, 9), 13)

    def test_subtract_numbers(self):
        '''Test that one number is subtracted from the other'''
        self.assertEqual(subtract(7, 17), 10)
