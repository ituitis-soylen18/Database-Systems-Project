from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, nickName, passwordHash, mail, firstName, lastName, userID):
        self.nickName = nickName
        self.passwordHash = passwordHash
        self.mail = mail
        self.firstName = firstName
        self.lastName = lastName
        self.userID = userID
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.nickName

    @property
    def is_active(self):
        return self.active

