import re


def validator(value):
    """method to validate title"""
    if not re.match(r"[A-Za-z0-9\']", value) or len(value) > 100:
        raise ValueError("Pattern not matched")


def validate_coordinates(value):
    """method to check for valid coordinates"""
    if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$", value) or len(value) > 50:
        raise ValueError("Pattern not matched")


def validate_comment(value):
    """method to check comment only starts with A-Z"""
    if not re.match(r"[A-Za-z0-9\']", value) or len(value) > 5000:
        raise ValueError("Pattern not matched")


def validate_integers(value):
    """method to check for only integers"""
    if not re.match(r"^[0-9]{5,20}$", value):
        raise ValueError("Pattern not matched")


def validate_email(value):
    """method to check for a valid email"""
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value) or len(value) > 100:
        raise ValueError("Pattern not matched")


def validate_characters(value):
    """method to check if variable contains only characters"""
    if not re.match(r"^[a-zA-Z\d\-\']{1,20}$", value):
        raise ValueError("Pattern not matched")

def validate_username(value):
    """method to check if variable contains only alphanumeric characters"""
    if not re.match(r"^[a-zA-Z\d]{1,20}$", value):
        raise ValueError("Pattern not matched")

def validate_password(value):
    """method to check if password contains more than 6 characters"""
    if not re.match(r"^[A-Za-z0-9!@#$%^&+*=]{6,120}$", value):
        raise ValueError("Pattern not matched")
