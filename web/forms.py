__author__ = 'alesha'
from wtforms import Form, PasswordField, validators, StringField
import re


class LoginForm(Form):
    email = StringField('Email Address', [validators.regexp(re.compile(
        '^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    ))])
    password = PasswordField('New Password', [
        validators.DataRequired(),
    ])
    # first_name = StringField('First name')
    # last_name = StringField('Last name')


class RegistrationForm(LoginForm):
    confirm = PasswordField('Repeat Password', [validators.DataRequired(),
                                                validators.EqualTo('password',
                                                                   'подтверждение должно совпадать с паролем')])

