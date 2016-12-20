import os
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from .. forms.LoginForm import LoginForm
from .. forms.RegisterForm import RegisterForm
from .. forms.ChangePassword import ChangePassword
from .. forms.UpdateProfileForm import UpdateProfileForm
from .. forms.ForgotPasswordForm import ForgotPasswordForm
from . import site
from .. import db
from .. models.User import User
from ..emails import send_email

# from ..models import User

@site.route('/', methods=['GET', 'POST'])
def index():
    return render_template('site/index.html')

@site.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('site.index'))
        flash('Invalid username or password', 'danger')

    return render_template('site/login.html', form=form)


@site.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('site.index'))


@site.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, 
                        password=form.password.data)
        db.session.add(user)
        flash('Successfully registered! You can now login.', 'success')
        return redirect(url_for('site.login'))
    return render_template('site/register.html', form=form)


@site.route('/change-password', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePassword()
    if form.validate_on_submit():
        user = current_user
        if user is not None:
            user.password = form.password.data
            db.session.add(user)
            flash('Successfully changed the password', 'success')
            return redirect(url_for('site.index'))

    return render_template('site/change-password.html', form=form)


@site.route('/update-profile', methods=['GET', 'POST'])
@login_required
def updateProfile():
    user = current_user
    form = UpdateProfileForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data

        photo = request.files['photo']
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(upload_folder, filename))

        db.session.add(user)
        flash('Updated Profile!', 'success')
        return redirect(url_for('site.updateProfile'))
    return render_template('site/update-profile.html', form=form)


@site.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.generate_password_reset_token()
        # send_email(user.email, 'Confirm your account', 'site/emails/password-reset', user=user, token=token)
        flash('An email has been sent to you for further instructions.', 'success')
        return redirect(url_for('site.forgotPassword'))
    return render_template('site/forgot-password.html', form=form)

@site.route('/reset-password/<token>')
def resetPassword(token):
    user = User.load_user_by_token(token)
    return render_template('site/reset-password.html', user=user)
    