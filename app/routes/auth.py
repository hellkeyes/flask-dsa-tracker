from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required
from sqlalchemy import or_
from app.models import db, User
from app.forms import RegistrationForm, LoginForm
from app import encrypt

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_username = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_username:
            flash("Username already taken!", "danger")
        elif existing_email:
            flash("Email already registered!", "danger")
        else:
            hashed_password = encrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username = form.username.data,
                email = form.email.data,
                password = hashed_password,
            )

            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form = form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(or_(User.username == form.login.data,User.email == form.login.data)).first()
        if not user:
            flash("No account found. Please register first.", "danget")
            return redirect(url_for('auth.register'))
        elif user and encrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid email/username or password", "danger")
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))