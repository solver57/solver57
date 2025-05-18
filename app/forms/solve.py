from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import DateField, HiddenField, SubmitField


class SchoolForm(FlaskForm):
    date_res = DateField("Введите дату")
    res = SubmitField("Решение")
    hint = SubmitField("Подсказка")
    attempts = HiddenField()
    last_date = HiddenField()


class CustomForm(FlaskForm):
    template = FileField("Шаблон")
    res = SubmitField("Решение")
    hint = SubmitField("Подсказка")
    attempts = HiddenField()
    last_template = HiddenField()
