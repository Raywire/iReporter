import re


def validator(value):
    """method to check for only integers"""
    if not re.match(r"^[0-9]+$", value):
        raise ValueError("Pattern not matched")


def validate_coordinates(value):
    """method to check for valid coordinates"""
    if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$", value):
        raise ValueError("Pattern not matched")


def validate_comment(value):
    """method to check comment only starts with A-Z"""
    if not re.match(r"[A-Za-z1-9]", value):
        raise ValueError("Pattern not matched")


def validate_integers(value):
    """method to check for only integers"""
    if not re.match(r"^[0-9]+$", value):
        raise ValueError("Pattern not matched")


def validate_email(value):
    """method to check for a valid email"""
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
        raise ValueError("Pattern not matched")


def validate_characters(value):
    """method to check if variable contains only characters"""
    if not re.match(r"^[a-zA-Z\d\-]+$", value):
        raise ValueError("Pattern not matched")
