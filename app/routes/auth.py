from flask import Blueprint, redirect, render_template
from flask_login import login_required, login_user, logout_user

from app.models import User

from ..forms.auth import LoginForm, RegisterForm
from .. import db


bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="auth")


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@bp.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        if db.session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/auth/login')
    return render_template('auth/register.html', title='Регистрация', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('auth/login.html', message="Неправильный логин или пароль", form=form)
    return render_template('auth/login.html', title='Авторизация', form=form)
