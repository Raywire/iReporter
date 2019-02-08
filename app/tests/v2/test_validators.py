"""Tests for validators run with pytest"""
import unittest
from app.validators import (validate_characters, validate_comment,
                            validate_coordinates, validate_phonenumber,
                            validate_email, validator, validate_password,
                            validate_username, allowed_file)


class ValidatorTestCase(unittest.TestCase):

    def test_for_integers(self):
        with self.assertRaises(ValueError):
            validate_phonenumber("123f")

    def test_for_characters(self):
        with self.assertRaises(ValueError):
            validate_characters("Ray' ")

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

    def test_validator(self):
        with self.assertRaises(ValueError):
            validator("@##$$Hello")

    def test_for_username(self):
        with self.assertRaises(ValueError):
            validate_username("ryan'")

    def test_allowed_file(self):
        self.assertTrue(allowed_file('test.MP4', 'videos'))
        self.assertTrue(allowed_file('test.jpg', 'images'))
      
          