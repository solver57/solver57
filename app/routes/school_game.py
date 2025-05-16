from pprint import pprint
from flask import Blueprint, render_template


from ..forms.school_game import Gameform
from ..algorithm.some_functions import make_matrix, create_colored_excel


bp = Blueprint("school_game", __name__, url_prefix="/school_game",
               template_folder="school_game")

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


@bp.route("/", methods=["GET", "POST"])
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

        if form.res.data:
            matrix = matrix0.copy()
            num = 1
        elif form.hint.data:
            matrix = find_el(matrix0, num)
            num += 1
    return render_template("school_game/school_game.html", form=form, matrix=matrix, colormap=colormap)
