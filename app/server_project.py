from flask import Flask, render_template, redirect
from loginform import Gameform, LoginForm
from pprint import pprint
from some_functions import make_matrix, create_colored_excel
from database import DataBase
# import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


LETTERS = ["L", 'P', 'F', 'T', 'H', 'S', 'W', 'D']
num = 1

def generate_colormap_list(matrix, colormap):
    w, h = len(matrix[0]), len(matrix)
    colormap_list = [[0] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            colormap_list[j][i] = f"#{colormap[matrix[j][i]]}"
    return colormap_list


def find_el(matrix, num):
    if num < len(LETTERS):
        matrix_base = [[""] * 10 for _ in range(5)]
        matrix_copy = matrix.copy()
        letter = LETTERS[:num]
        print(letter)
        matrix_base = [[matrix_copy[j][i] if matrix_copy[j][i] in letter else "0" for i in range(len(matrix_copy[0]))] for j in range(len(matrix_copy))]
        pprint(matrix_copy)
        return matrix_base
    else:
        return matrix


@app.route("/school_game", methods=["GET", "POST"])
def generate_matrix1(num=1):
    num = 1
    form = Gameform()
    matrix = [[""] * 10] * 5
    colormap = None
    date = None
    if form.validate_on_submit():
        if (date is None) or (date is not None and date != form.date_res.data):
            date = form.date_res.data
            matrix0 = make_matrix(date, (5, 10))[0]
            colormap = create_colored_excel(matrix0)
            colormap["0"] = "FFFFFF"
            colormap_list = generate_colormap_list(matrix0, colormap)

        if form.res.data:
            matrix = matrix0.copy()
            num = 1
            # pprint(matrix)
            # pprint(colormap_list)
        elif form.hint.data:
            print(num)
            matrix = find_el(matrix0, num)
            num += 1
            # pprint(matrix)
    return render_template("school.html", form=form, matrix=matrix, colormap=colormap)


@app.route("/form", methods=["GET", "POST"])
def login():
    form = LoginForm()
    r_user = None
    if form.validate_on_submit():
        datab = DataBase()
        params = {}
        name = form.username.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        params["name"], params["surname"], params["email"], params["password"] = name, surname, email, password
        r_user = datab.get_inf(params)
        print(name, surname, email, password)
        if r_user:
            return redirect("/school_game")

    return render_template("form.html", form=form, right_user=r_user)

if __name__ == "__main__":
    app.run(port=5050, debug=True)