from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, SubmitField


class Gameform(FlaskForm):
    date_res = DateField("Введите дату")
    res = SubmitField("Решение")
    hint = SubmitField("Подсказка")
    attempts = HiddenField()
    last_date = HiddenField()
