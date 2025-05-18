from datetime import datetime
from flask import Blueprint, jsonify, request

from ..algorithm.main import make_matrix, make_school


bp = Blueprint("solve_api", __name__, url_prefix="/api/solve")


def _bad_request(message: str, code: int = 400):
    return jsonify({"error": message}), code


@bp.route('/custom', methods=['POST'])
def api_solve_custom():
    if not request.is_json:
        return _bad_request("Request body must be JSON")
    data = request.get_json()
    bs = data.get("board_size")
    if not isinstance(bs, (list, tuple)) or len(bs) != 2:
        return _bad_request("Invalid or missing 'board_size'")
    try:
        board_size = (int(bs[0]), int(bs[1]))
    except (TypeError, ValueError):
        return _bad_request("'board_size' elements must be integers")
    figures = data.get("figures")
    if not isinstance(figures, dict):
        return _bad_request("Invalid or missing 'figures'")
    exc = data.get("excluded_cells", [])
    if not isinstance(exc, list):
        return _bad_request("'excluded_cells' must be a list")
    try:
        excluded = [(int(c[0]), int(c[1])) for c in exc]
    except (TypeError, ValueError, IndexError):
        return _bad_request("Each 'excluded_cells' item must be a [row, col] list")
    try:
        solutions = make_matrix(board_size, figures, excluded)
    except Exception as e:
        return _bad_request(str(e), 500)
    return jsonify({"solutions": solutions})


@bp.route('/school', methods=['POST'])
def api_solve_school():
    if not request.is_json:
        return _bad_request("Request body must be JSON")
    data = request.get_json()
    date_str = data.get("date")
    if not isinstance(date_str, str):
        return _bad_request("Missing or invalid 'date'")
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return _bad_request("Invalid date format; use YYYY-MM-DD")
    try:
        solutions = make_school(date_obj)
    except Exception as e:
        return _bad_request(str(e), 500)
    return jsonify({"solutions": solutions})


@bp.errorhandler(400)
def handle_bad_request(error):
    return jsonify({'error': str(error)}), 400


@bp.errorhandler(500)
def handle_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500
