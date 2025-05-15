from pprint import pprint
from random import randint
from time import time


def get_random_A(rows: int, cols: int, share: float = 0.5) -> [[int]]:
    '''случайная матрица для тестирования с редким набором единиц и уникальными строками'''
    matrix = set()
    while len(matrix) < rows:
        row = tuple(1 if randint(0, 1000000) < 1000000 * share else 0 for _ in range(cols))
        if row not in matrix:
            matrix.add(row)
    return [list(m) for m in matrix]


class ColumnNode:
    def __init__(self, name):
        self.L = self
        self.R = self
        self.U = self
        self.D = self
        self.C = self  # для заголовка указывает на себя
        self.S = 0  # размер столбца
        self.N = name  # имя столбца


class DataNode:
    def __init__(self, col_header):
        self.L = self
        self.R = self
        self.U = self
        self.D = self
        self.C = col_header  # ссылка на заголовок столбца


class DLX:
    def __init__(self, matrix, column_names):
        # Создаем заголовочную ноду
        self.root = ColumnNode("root")
        self.columns = {}
        self.solution = []
        self.matrix = matrix
        self.column_names = column_names

        # Инициализация заголовков столбцов
        prev = self.root
        for name in column_names:
            col = ColumnNode(name)
            col.L = prev
            col.R = self.root
            prev.R = col
            self.root.L = col
            prev = col
            self.columns[name] = col

        # Добавление строк
        for row_idx, row in enumerate(matrix):
            first_node = None
            prev_node = None
            for col_idx, val in enumerate(row):
                if val == 1:
                    col_name = column_names[col_idx]
                    col_header = self.columns[col_name]
                    node = DataNode(col_header)

                    # Вертикальные связи
                    node.U = col_header.U
                    node.D = col_header
                    col_header.U.D = node
                    col_header.U = node

                    # Горизонтальные связи
                    if prev_node:
                        node.L = prev_node
                        node.R = prev_node.R
                        prev_node.R.L = node
                        prev_node.R = node
                    else:
                        first_node = node
                    prev_node = node

                    col_header.S += 1

    def cover(self, col):
        # Удаляем столбец из списка заголовков
        col.R.L = col.L
        col.L.R = col.R

        # Удаляем все строки в этом столбце
        i = col.D
        while i != col:
            j = i.R
            while j != i:
                j.D.U = j.U
                j.U.D = j.D
                j.C.S -= 1
                j = j.R
            i = i.D

    def uncover(self, col):
        # Восстанавливаем строки в обратном порядке
        i = col.U
        while i != col:
            j = i.L
            while j != i:
                j.C.S += 1
                j.D.U = j
                j.U.D = j
                j = j.L
            i = i.U

        # Возвращаем столбец в список заголовков
        col.R.L = col
        col.L.R = col

    def search(self, k=0):
        if self.root.R == self.root:
            yield self.solution.copy()
            return

        # Выбор столбца с минимальным размером
        c = self.root.R
        min_size = float('inf')
        j = self.root.R
        while j != self.root:
            if j.S < min_size:
                c = j
                min_size = j.S
            j = j.R

        self.cover(c)

        r = c.D
        while r != c:
            self.solution.append(r)

            j = r.R
            while j != r:
                self.cover(j.C)
                j = j.R

            yield from self.search(k + 1)

            self.solution.pop()

            j = r.L
            while j != r:
                self.uncover(j.C)
                j = j.L

            r = r.D

        self.uncover(c)

    def solve(self):
        return list(self.search())

    def solve_iteratively(self, max_num=0):
        sols = []
        m = self.matrix
        columns = self.column_names
        num = 0
        while max_num == 0 or num < max_num:
            num += 1
            dlx_once = DLX(m, columns)
            try:
                solution = next(dlx_once.search())
                sols.append(solution)
                res = show([solution])[0]
                rows_to_delete = []
                for r in res:
                    row_to_delete = [1 if columns[i] in r else 0 for i in range(len(columns))]
                    if row_to_delete in m:
                        rows_to_delete.append(row_to_delete)
                for row in rows_to_delete:
                    m.remove(row)
            except StopIteration:
                break
        # return [show([sol])[0] for sol in sols]
        return sols


def show(solutions):
    sols = []
    for sol in solutions:
        rows = []
        for node in sol:
            row = [node.C.N]
            current = node.R
            while current != node:
                row.append(current.C.N)
                current = current.R
            rows.append(tuple(sorted(row)))
        sols.append(frozenset(rows))
    return [sorted([t for t in s], key=lambda x: x[-1]) for s in set(sols)]


# Пример использования:
if __name__ == "__main__":
    matrix = [
        [1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 1],
        [0, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 1],
    ]

    column_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    pprint(column_names)
    pprint(matrix)

    dlx = DLX(matrix, column_names)
    solutions = dlx.solve_iteratively(2)

    for i, solution in enumerate(show(solutions)):
        print(f"Solution {i + 1}:")
        for r in solution:
            print(r)
        print()
