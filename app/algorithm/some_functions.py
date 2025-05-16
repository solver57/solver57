from datetime import date
import json
import colorsys
from typing import Any
from .dancing import DLX, show
from .board import Figure, generate_column_names, Board, generate_matrix

N_H_W = '''пн,0,8
вт,0,9
ср,1,9
чт,2,9
пт,3,9
сб,4,9
вс,4,8
янв,0,0
фев,0,1
мар,0,2
апр,0,3
май,1,0 
июн,1,1 
июл,3,0
авг,3,1
сен,4,0
окт,4,1
ноя,4,2
дек,4,3
1,0,4
2,0,5
3,0,6
4,0,7
5,1,2
6,1,3
7,1,4
8,1,5
9,1,6
10,1,7
11,1,8
12,2,0
13,2,1
14,2,2
15,2,3
16,2,4
17,2,5
18,2,6
19,2,7
20,2,8
21,3,2
22,3,3
23,3,4
24,3,5
25,3,6
26,3,7
27,3,8
28,4,4
29,4,5
30,4,6
31,4,7'''


def create_dict_from_str(cal: str):
    data_dict: dict[str, tuple[int, int]] = {}
    for line in cal.split():
        row = line.split(',')
        if len(row) == 3:
            key = row[0]
            try:
                value = (int(row[1]), int(row[2]))
                data_dict[key] = value
            except ValueError:
                print(
                    f"Warning: Could not convert values to integers in row: {row}")
        else:
            print(
                f"Warning: Skipping row with incorrect number of elements: {row}")
    return data_dict


def read_dict_json(filename: str):
    with open(filename + ('.json' if filename[-5:] != '.json' else ''), encoding='UTF8') as f:
        cal = {a: tuple(b) for a, b in json.loads(f.read()).items()}
    return cal


def save_dict_json(filename: str, calendar_cells: dict[Any, Any]):
    with open(filename + ('.json' if filename[-5:] != '.json' else ''), 'w', encoding='UTF8') as f:
        f.write(json.dumps(calendar_cells, ensure_ascii=False, indent=4))


def format_date_ru(date_obj: date):
    """
    Formats a date string into a tuple of (weekday, day, month) in Russian.

    Args:
        date_str (str): A date string in the format 'YYYY-MM-DD'.

    Returns:
        tuple: A tuple containing the weekday (short format in Russian),
               day (string), and month (short format in Russian).
               Returns None if the input date is invalid.
    """

    try:
        # 0 is Sunday, 1 is Monday, ..., 6 is Saturday
        weekday = date_obj.strftime('%w')
        weekday_names = ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб']
        weekday_ru = weekday_names[int(weekday)]
        day = str(date_obj.day)
        month = date_obj.strftime('%m')
        month_names = ['янв', 'фев', 'мар', 'апр', 'май',
                       'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        month_ru = month_names[int(month) - 1]
        return (weekday_ru, day, month_ru)
    except ValueError as e:
        e.add_note("Invalid date format. Please use YYYY-MM-DD.")
        raise e


# Задаем фигуры для покрытия
def make_matrix(date_obj: date, board_size: tuple[int, int]):
    n_h_w_dict = create_dict_from_str(N_H_W)

    f1 = Figure('L', [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1)])
    f2 = Figure('P', [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1)])
    f3 = Figure('F', [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 2)])
    f4 = Figure('T', [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1)])
    f5 = Figure('H', [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1), (2, 2)])
    f6 = Figure('S', [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1), (3, 1)])
    f7 = Figure('W', [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)])
    f8 = Figure('D', [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)])
    figures = [f1, f2, f3, f4, f5, f6, f7, f8]
    # и для каждой фигуры получаем ее варианты и добавляем в общий словарь вариантов
    f_vars: dict[str, list[tuple[int, int]]] = {}
    for fig in figures:
        for variant in fig.variants:
            f_vars[variant] = fig.variants[variant]

    # Создаем доску некоторой формы, вырезая ненужные клетки из прямоугольника
    b = Board(board_size[0], board_size[1])
    formatted_date = format_date_ru(date_obj)
    for cell in formatted_date:
        b.flip(*n_h_w_dict[cell])

    # Список заголовков столбцов, где часть - клетки поля, а часть - уникальные типы фигурок
    column_names = generate_column_names(b, f_vars)
    # print(column_names)

    # создаем матрицу всех строк, соответствующих уникальным расположениям фигурок на поле
    matrix = generate_matrix(b, f_vars, column_names)

    dlx = DLX(matrix, column_names)
    all_solutions = dlx.solve()
    unique_solutions = find_unique_matrices(
        [solution2matrix(m) for m in show(all_solutions)])
    return unique_solutions


def create_colored_excel(matrices: list[list[str]]):
    # Получаем все уникальные буквы (исключая '0')
    unique_letters = sorted(
        {cell for matrix in matrices for row in matrix for cell in row if cell != '0'})

    # Создаем палитру цветов
    palette: list[str] = []
    num_colors = len(unique_letters)
    for i in range(num_colors):
        hue = i / num_colors  # Равномерное распределение оттенков
        saturation = [0.5, 0.9, 0.9, 0.5][i % 4]  # Разная насыщенность
        lightness = [0.4, 0.9][i % 2]  # Разная яркость
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        hex_color = f"{int(rgb[0] * 255):02X}{int(rgb[1] * 255):02X}{int(rgb[2] * 255):02X}"
        palette.append(hex_color)

    # Сопоставляем буквы и цвета
    color_map = {letter: color
                 for letter, color in zip(unique_letters, palette)}
    return color_map

def rotate_matrix(matrix: list[list[str]]):
    """Поворачивает матрицу на 90 градусов по часовой стрелке."""
    return [list(row) for row in zip(*matrix[::-1])]

def reflect_matrix(matrix: list[list[str]]):
    """Отражает матрицу по горизонтали."""
    return [row[::-1] for row in matrix]

def generate_all_variants(matrix: list[list[str]]):
    """Генерирует все 8 вариантов матрицы (повороты и отражения)."""
    variants: list[list[list[str]]] = []
    current = matrix
    for _ in range(4):  # 4 поворота
        variants.append(current)
        variants.append(reflect_matrix(current))  # Отражение
        current = rotate_matrix(current)  # Поворот на 90 градусов
    return variants


def find_unique_matrices(matrices: list[list[list[str]]]):
    """Возвращает список уникальных матриц с точностью до поворотов и отражений."""
    unique_matrices: list[list[list[str]]] = []
    for matrix in matrices:
        # Генерируем все варианты текущей матрицы
        variants = generate_all_variants(matrix)
        # Проверяем, есть ли хотя бы один вариант в списке уникальных
        is_unique = True
        for variant in variants:
            if variant in unique_matrices:
                is_unique = False
                break
        # Если матрица уникальна, добавляем её в список
        if is_unique:
            unique_matrices.append(matrix)
    return unique_matrices


def solution2matrix(s: list[tuple[str, ...]]):
    t: dict[tuple[int, ...], str] = {}
    for r in s:
        ind = r[-1][:1]
        color = ind if r[-1] != 'exclude' else '0'
        for w in r[:-1]:
            t[tuple(map(int, w.split('_')))] = color
    h, w = map(lambda x: max(x) + 1, zip(*list(t)))
    m = [[t[(i, j)] for j in range(w)] for i in range(h)]
    return m
