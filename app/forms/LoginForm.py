from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Required(), Email()])
    password = PasswordField("Password", validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField("Login")

