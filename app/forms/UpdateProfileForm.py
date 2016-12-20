from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Email

from wtforms import ValidationError
from .. models.User import User 
from flask_login import current_user

class UpdateProfileForm(FlaskForm):
    name = StringField("Name", validators=[Required()])
    email = StringField("Email", validators=[Required(), Email()])
    photo = FileField("Photo", validators=[FileAllowed(['jpg', 'png', 'gif'], 'Only Images are allowed!')])
    submit = SubmitField("Update")

    def validate_email(self, field):
        if field.data != current_user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered!')


