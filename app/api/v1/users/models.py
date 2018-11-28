from werkzeug import generate_password_hash, check_password_hash

import datetime

class UserModel():

  def __init__(self, public_id, firstname, lastname, othernames, email, phoneNumber, username, password, registered, isAdmin):
    self.public_id = public_id
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.othernames = othernames.title()
    self.email = email.lower()
    self.username = username
    self.phoneNumber = phoneNumber
    self.set_password(password)
    self.isAdmin = isAdmin
    self.registered = registered

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)


