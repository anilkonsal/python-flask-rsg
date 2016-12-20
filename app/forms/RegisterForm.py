from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Email, EqualTo
from wtforms import ValidationError
from .. models.User import User 

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[Required()])
    email = StringField("Email", validators=[Required(), Email()])
    password = PasswordField("Password", validators=[Required(), 
                                EqualTo('confirm_password', 'Passwords must match!')])
    confirm_password = PasswordField("Confirm Password", validators=[Required()])
    submit = SubmitField("Login")


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered!')


