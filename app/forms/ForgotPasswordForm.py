from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import Required, Email
from .. models.User import User

class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[Required(), Email()])
    submit = SubmitField("Submit")

    def validate_email(self, field):
        if field.name not in self.errors:
            if not User.query.filter_by(email=field.data).first():
                raise ValidationError('Email not registered with us!')