from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField

from datetime import datetime


class DeskEditForm(FlaskForm):
    deskName = StringField("Title", validators=[DataRequired()])

class CardEditForm(FlaskForm):
    word = StringField("Word", validators=[DataRequired()])
    translation = StringField("Translation", validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class SigninForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    mail = StringField("Mail", validators=[DataRequired()])
    firstName = StringField("Firstname")
    lastName = StringField("Lastname")

#class StudyForm(FlaskForm):
    