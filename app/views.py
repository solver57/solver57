from pprint import pprint
from flask import Blueprint, render_template, redirect


from .models import User, db
from .forms import Gameform, LoginForm
from .algorithm.some_functions import make_matrix, create_colored_excel


bp = Blueprint("main", __name__)

LETTERS = ["L", 'P', 'F', 'T', 'H', 'S', 'W', 'D']


def generate_colormap_list(matrix: list[list[str]], colormap: dict[str, str]):
    w, h = len(matrix[0]), len(matrix)
    colormap_list = [[""] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            colormap_list[j][i] = f"#{colormap[matrix[j][i]]}"
    return colormap_list


def find_el(matrix: list[list[str]], num: int):
    if num < len(LETTERS):
        matrix_base = [[""] * 10 for _ in range(5)]
        matrix_copy = matrix.copy()
        letter = LETTERS[:num]
        print(letter)
        matrix_base = [[matrix_copy[j][i] if matrix_copy[j][i] in letter else "0" for i in range(
            len(matrix_copy[0]))] for j in range(len(matrix_copy))]
        pprint(matrix_copy)
        return matrix_base
    else:
        return matrix


@bp.route("/school_game", methods=["GET", "POST"])
def generate_matrix1(num: int = 1):
    num = 1
    form = Gameform()
    matrix = [[""] * 10] * 5
    colormap = None
    date = None
    if form.validate_on_submit():
        date = form.date_res.data
        if date is None:
            return  # TODO
        matrix0 = make_matrix(date, (5, 10))[0]
        colormap = create_colored_excel(matrix0)
        colormap["0"] = "FFFFFF"
        # colormap_list = generate_colormap_list(matrix0, colormap)

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


@bp.route("/form", methods=["GET", "POST"])
def login():  # TODO
    form = LoginForm()
    r_user = None
    if form.validate_on_submit():
        res = db.session.query(User).filter(
            User.email == form.email.data.lower())
        el = res.first()
        if el is None:
            user = User(
                email=form.email.data,
                name=form.username.data,
                surname=form.surname.data,
                hashed_password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
        else:
            if el.hashed_password != form.password.data:
                render_template("form.html", form=form, right_user=r_user)
        return redirect("/school_game")

    return render_template("form.html", form=form, right_user=r_user)
