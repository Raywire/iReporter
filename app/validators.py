import re

ALLOWED_EXTENSIONS_IMAGE = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS_VIDEO = set(['mp4', 'webm', 'ogg'])


def validator(value):
    """method to validate title"""
    if not re.match(r"[A-Za-z0-9\']", value) or len(value) > 100:
        raise ValueError("Please enter a valid title")


def validate_coordinates(value):
    """method to check for valid coordinates"""
    if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$", value) or len(value) > 50:
        raise ValueError("Use valid coordinates")


def validate_comment(value):
    """method to check comment only starts with A-Z"""
    if not re.match(r"[A-Za-z0-9\']", value) or len(value) > 5000:
        raise ValueError("Comment cannot start with special characters")


def validate_phonenumber(value):
    """method to check for only integers"""
    if not re.match(r"^07[0-9]{8}$", value):
        raise ValueError("Only integers allowed")


def validate_email(value):
    """method to check for a valid email"""
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value) or len(value) > 100:
        raise ValueError("Enter a valid email")


def validate_characters(value):
    """method to check if variable contains only characters"""
    if not re.match(r"^[a-zA-Z\d\-\']{1,20}$", value):
        raise ValueError("Use a valid name")


def validate_username(value):
    """method to check if variable contains only alphanumeric characters"""
    if not re.match(r"^[a-zA-Z\d]{1,20}$", value):
        raise ValueError("Username can only contain characters and integers")


def validate_password(value):
    """method to check if password contains more than 6 characters"""
    if not re.match(r"^[A-Za-z0-9!@#$%^&+*-_?.,\']{6,120}$", value):
        raise ValueError("Enter a valid password")


def allowed_file(filename, filetype):
    if filetype == 'videos':
        allowed_file_type = ALLOWED_EXTENSIONS_VIDEO

    if filetype == 'images':
        allowed_file_type = ALLOWED_EXTENSIONS_IMAGE

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_file_type
