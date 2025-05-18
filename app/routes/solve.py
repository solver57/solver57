from flask import Blueprint, render_template
from flask_login import login_required
import json

from ..forms.solve import CustomForm, SchoolForm
from ..algorithm.main import make_matrix, create_colored_excel, make_school


bp = Blueprint("solve", __name__, url_prefix="/solve",
               template_folder="solve")

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
        matrix_base = [[matrix_copy[j][i] if matrix_copy[j][i] in letter else "0" for i in range(
            len(matrix_copy[0]))] for j in range(len(matrix_copy))]
        return matrix_base
    else:
        return matrix


@bp.route("/school", methods=["GET", "POST"])
def solve_school():
    form = SchoolForm()
    matrix = [[""] * 10] * 5
    colormap = None
    date = form.date_res.data
    attempts = 1
    if form.validate_on_submit() and date is not None:
        if form.attempts.data and form.last_date.data == str(form.date_res.data):
            attempts = int(form.attempts.data)
        print(form.last_date.data)
        form.last_date.data = str(date)
        matrix = make_school(date)[0]
        colormap = create_colored_excel(matrix)
        colormap["0"] = "FFFFFF"

        if form.res.data:
            matrix = matrix
            attempts = 1
        elif form.hint.data:
            matrix = find_el(matrix, attempts)
            attempts += 1
    form.attempts.data = str(attempts)
    return render_template("solve/school.html", form=form, matrix=matrix, colormap=colormap)


@bp.route("/custom", methods=["GET", "POST"])
@login_required
def solve_custom():
    form = CustomForm()
    matrix = None
    colormap = None
    template_data = None
    attempts = 1
    if form.validate_on_submit() and (form.template.data or form.last_template.data):
        template_file = form.template.data
        if template_file is not None:
            template_data = json.load(template_file)
            attempts = 1
            form.last_template.data = json.dumps(template_data)
        else:
            template_data = json.loads(form.last_template.data)
            attempts = int(form.attempts.data)
        matrix = make_matrix(tuple(template_data["board_size"]), template_data["figures"],
                             list(map(tuple, template_data["excluded_cells"])))[0]
        colormap = create_colored_excel(matrix)
        colormap["0"] = "FFFFFF"

        if form.res.data:
            attempts = 1
        elif form.hint.data:
            matrix = find_el(matrix, attempts)
            attempts += 1

    form.attempts.data = str(attempts)
    return render_template(
        "solve/custom.html",
        form=form,
        matrix=matrix,
        colormap=colormap,
        template_data=template_data
    )
