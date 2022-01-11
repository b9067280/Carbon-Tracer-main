import re
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo, ValidationError


def character_check(form, field):
    excluded_chars = "*?"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


class LoginForm(FlaskForm):
    username = StringField(validators=[Required()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    firstname = StringField(validators=[Required(), character_check])
    lastname = StringField(validators=[Required(), character_check])
    username = StringField(validators=[Required()])
    email = StringField(validators=[Required(), Email()])

    # Function to validate the password.
    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d])')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit, 1 lowercase, 1 uppercase and 1 special "
                                  "character.")

    password = PasswordField(validators=[Required(), Length(min=8, max=15, message='Password must be between 8 and 15 '
                                                                                   'characters in length.')])
    confirm_password = PasswordField(
        validators=[Required(), EqualTo('password', message='Both password fields must be equal!')])

    submit = SubmitField()
