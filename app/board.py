from collections import defaultdict
from pprint import pprint

from dancing import DLX, show

from xl import find_unique_matrices, create_colored_excel, solution2matrix


class Figure:
    def __init__(self, fig):
        self.fig = fig
        self.name = fig[0]
        self.variants = self.generate_variants()

    def generate_variants(self):
        variants = []
        for x, y in self.fig[1:]:
            variants.append([(x, y), (-y, x), (-x, -y), (y, -x), (x, -y), (-y, -x), (-x, y), (y, x)])
        transformed = list(zip(*variants))
        shifted = set()
        for t in transformed:
            left = min(x for x, y in t)
            bottom = min(y for x, y in t)
            t = frozenset((x - left, y - bottom) for x, y in t)
            shifted.add(t)
        return {self.name + '_' + str(i): list(t) for i, t in enumerate(shifted)}

    def __repr__(self):
        ss = f'_______{self.name}_______\n'
        for v in self.variants:
            var = self.variants[v]
            width, height = (max(x for x, y in var) + 1,
                             max(y for x, y in var) + 1)
            s = ''
            for j in range(height):
                for i in range(width):
                    if (i, j) in var:
                        s += f'[{v}]'
                    else:
                        s += ' [ . ] '
                s += '\n\n'
            s += '\n'
            ss += s
        return ss


def occupy(mino, x, y):
    start_x, start_y = mino[0]
    occ = []
    for dx, dy in mino:
        point = dx - start_x + x, dy - start_y + y
        occ.append(point)
    return occ


class Board:
    def __init__(self, h, w):
        self.matrix = [[f'{i:0>2}_{j:0>2}' for j in range(w)] for i in range(h)]
        self.allowed = defaultdict(lambda: 0, {(i, j): 1 for j in range(w) for i in range(h)})

    def __repr__(self):
        return "\n".join([" ".join([self.matrix[i][j] if self.allowed[(i, j)] else ' ... ' for j in
                                    range(len(self.matrix[0]))]) for i in range(len(self.matrix))]) + "\n"

    def flip(self, coord1, coord2=None):
        if isinstance(coord1, tuple):
            i, j = coord1
        else:
            i, j = coord1, coord2
        if (i, j) in self.allowed:
            self.allowed[(i, j)] = 1 - self.allowed[(i, j)]

    def check(self, mino, x, y):
        occ = occupy(mino, x, y)
        return all(self.allowed[p] for p in sorted(occ))

    def place(self, solution):
        for p in solution[:-1]:
            x, y = p
            # self.flip(*p)
            self.matrix[x][y] = solution[-1]


def generate_column_names(board: Board, variants):
    return [morf(p) for p in board.allowed] + list({s.split('_')[0] for s in variants}) + ['exclude']


def morf(p):
    i, j = p
    return f'{i:0>2}_{j:0>2}'


def generate_matrix(board: Board, f_variants, names):
    lines = []
    for f in f_variants:
        variation = f_variants[f]
        for point in list(board.allowed):
            occupied = occupy(variation, *point)
            if board.check(variation, *point):
                line = [0] * len(names)
                line[names.index(f.split('_')[0])] = 1
                headers = [morf(p) for p in occupied]
                # print(headers)
                for i in [names.index(s) for s in headers]:
                    line[i] = 1
                lines.append(line)
        excluded_line = [0] * len(names)
        excluded_line[-1] = 1
        for line in board.matrix:
            for p in line:
                if not board.allowed[tuple(map(int, p.split('_')))]:
                    ind = names.index(p)
                    excluded_line[ind] = 1
        lines.append(excluded_line)
    return lines


# Пример использования:
if __name__ == "__main__":
    solution = [['04_06', '05_05', '05_06', '05_07', '06_06', 'P04'],
                ['06_05', '06_07', '07_05', '07_06', '07_07', 'P07'],
                ['02_06', '02_07', '03_06', '03_07', '04_07', 'P11'],
                ['02_03', '02_04', '02_05', '03_05', '04_05', 'P05'],
                ['00_07', '01_04', '01_05', '01_06', '01_07', 'P01'],
                ['00_02', '00_03', '00_04', '00_05', '00_06', 'P03'],
                ['00_00', '00_01', '01_01', '01_02', '01_03', 'P10'],
                ['01_00', '02_00', '02_01', '02_02', '03_00', 'P09'],
                ['06_03', '07_01', '07_02', '07_03', '07_04', 'P06'],
                ['04_02', '05_02', '05_03', '05_04', '06_04', 'P00'],
                ['05_01', '06_00', '06_01', '06_02', '07_00', 'P02'],
                ['03_01', '03_02', '04_00', '04_01', '05_00', 'P08'],
                ['03_03', '03_04', '04_03', '04_04', 'exclude']]
    b = Board(8, 8)
    b.flip(3, 3)
    b.flip(4, 3)
    b.flip(3, 4)
    b.flip(4, 4)
    print(b)
    for pent in solution[:-1]:
        b.place([tuple(map(int, p.split('_'))) for p in pent[:-1]] + [pent[-1]])
    print(b)

    # Создаем доску некоторой формы, вырезая ненужные клетки из прямоугольника
    b = Board(2, 2)
    b.flip(0, 0)
    print(b)

    # Задаем фигуры для покрытия
    figures = []
    figure1 = Figure(['L', (1, 0), (0, 1), (1, 1)])
    ...
    figures.append(figure1)
    # и для каждой фигуры получаем ее варианты и добавляем в общий словарь вариантов
    f_vars = {}
    for fig in figures:
        for variant in fig.variants:
            f_vars[variant] = fig.variants[variant]

    # Список заголовков столбцов, где часть - клетки поля, а часть - уникальные типы фигурок
    names = generate_column_names(b, f_vars)
    print(names)

    # создаем матрицу всех строк, соответствующих уникальным расположениям фигурок на поле
    matrix = generate_matrix(b, f_vars, names)
    pprint(matrix)

    dlx = DLX(matrix, names)
    solutions = dlx.solve()
    show(solutions)

    # наконец попробуем пентамино!

    # Создаем доску некоторой формы, вырезая ненужные клетки из прямоугольника
    b = Board(15, 15)
    rect = [(i + 6, j + 5) for i in range(3) for j in range(5)]
    half_face = [(4, 3), (4, 4), (4, 5), (5, 4), (9, 4), (10, 5), (11, 6)]
    face = [(11, 7)] + half_face + [(i, 14 - j) for i, j in half_face]
    # cut = rect
    cut = face
    for cell in cut:
        b.flip(cell)
    print(b)


    # Задаем фигуры для покрытия
    from polymino import generate_polyominoes

    figures = [Figure(pentamino) for pentamino in generate_polyominoes(6)]
    # и для каждой фигуры получаем ее варианты и добавляем в общий словарь вариантов
    f_vars = {}
    for fig in figures:
        for variant in fig.variants:
            f_vars[variant] = fig.variants[variant]

    # Список заголовков столбцов, где часть - клетки поля, а часть - уникальные типы фигурок
    names = generate_column_names(b, f_vars)
    # создаем матрицу всех строк, соответствующих уникальным расположениям фигурок на поле
    matrix = generate_matrix(b, f_vars, names)

    for i in range(3, 100):
        dlx = DLX(matrix, names)
        all_solutions = dlx.solve_iteratively(i)
        unique_solutions = find_unique_matrices([solution2matrix(m) for m in show(all_solutions)])
        create_colored_excel(unique_solutions, 'output'+str(i)+'.xlsx')

    # all_solutions = dlx.solve()
    # print(len(unique_solutions))
