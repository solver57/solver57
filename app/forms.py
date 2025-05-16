from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired


class Gameform(FlaskForm):
    date_res = DateField("Введите дату")
    res = SubmitField("Решение")
    hint = SubmitField("Подсказка")


class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
