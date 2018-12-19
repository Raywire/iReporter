"""Tests for validators run with pytest"""
import unittest
from app.validators import (validate_characters, validate_comment, validate_coordinates,
                            validate_email, validate_integers, validate_password)


class ValidatorTestCase(unittest.TestCase):

    def test_for_integers(self):
        with self.assertRaises(ValueError):
            validate_integers("123f")

    def test_for_characters(self):
        with self.assertRaises(ValueError):
            validate_characters("Ray'")

    def test_for_email(self):
        with self.assertRaises(ValueError):
            validate_email("ryanwiregmail.com")

    def test_for_coordinates(self):
        with self.assertRaises(ValueError):
            validate_coordinates("-123, 1234")

    def test_for_password(self):
        with self.assertRaises(ValueError):
            validate_password("123")

    def test_for_comment(self):
        with self.assertRaises(ValueError):
            validate_comment("@##$$Hello")
          