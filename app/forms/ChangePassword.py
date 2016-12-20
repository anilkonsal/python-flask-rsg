import sys
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import PasswordField, SubmitField
from wtforms.validators import Required, EqualTo
from wtforms import ValidationError
from .. models.User import User

class ChangePassword(FlaskForm):
    existing_password = PasswordField("Existing Password", validators=[Required()])
    password = PasswordField("Password", validators=[Required(), 
                    EqualTo('confirm_password', 'Both passwords must match!')])
    confirm_password = PasswordField("Confirm Password", validators=[Required()])
    submit = SubmitField("Change Password")


    def validate_existing_password(self, field):
        user = User.query.filter_by(id=current_user.id).first()
        if not user.verify_password(field.data):
            raise ValidationError('Existing password is incorrect!')
