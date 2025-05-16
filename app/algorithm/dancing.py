from pprint import pprint
from random import randint
from typing import Generator


def get_random_a(rows: int, cols: int, share: float = 0.5) -> list[list[int]]:
    '''случайная матрица для тестирования с редким набором единиц и уникальными строками'''
    matrix: set[tuple[int, ...]] = set()
    while len(matrix) < rows:
        row = tuple(1 if randint(0, 1000000) < 1000000 *
                    share else 0 for _ in range(cols))
        if row not in matrix:
            matrix.add(row)
    return [list(m) for m in matrix]


class ColumnNode:
    def __init__(self, name: str):
        self.left = self
        self.right = self
        self.up: ColumnNode | DataNode = self
        self.down: ColumnNode | DataNode = self
        self.column_header = self  # для заголовка указывает на себя
        self.size: int = 0  # размер столбца
        self.name = name  # имя столбца


class DataNode:
    def __init__(self, column_header: ColumnNode):
        self.left = self
        self.right = self
        self.up: ColumnNode | DataNode = self
        self.down: ColumnNode | DataNode = self
        self.column_header = column_header  # ссылка на заголовок столбца


class DLX:
    def __init__(self, matrix: list[list[int]], column_names: list[str]):
        # Создаем заголовочную ноду
        self.root = ColumnNode("root")
        self.columns: dict[str, ColumnNode] = {}
        self.solution: list[DataNode] = []
        self.matrix = matrix
        self.column_names = column_names

        # Инициализация заголовков столбцов
        prev = self.root
        for name in column_names:
            col = ColumnNode(name)
            col.left = prev
            col.right = self.root
            prev.right = col
            self.root.left = col
            prev = col
            self.columns[name] = col

        # Добавление строк
        for row in matrix:
            prev_node = None
            for col_idx, val in enumerate(row):
                if val == 1:
                    col_name = column_names[col_idx]
                    col_header = self.columns[col_name]
                    node = DataNode(col_header)

                    # Вертикальные связи
                    node.up = col_header.up
                    node.down = col_header
                    col_header.up.down = node
                    col_header.up = node

                    # Горизонтальные связи
                    if prev_node:
                        node.left = prev_node
                        node.right = prev_node.right
                        prev_node.right.left = node
                        prev_node.right = node
                    prev_node = node

                    col_header.size += 1

    def cover(self, col: ColumnNode):
        # Удаляем столбец из списка заголовков
        col.right.left = col.left
        col.left.right = col.right

        # Удаляем все строки в этом столбце
        i = col.down
        while i != col:
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.column_header.size -= 1
                j = j.right
            i = i.down

    def uncover(self, col: ColumnNode):
        # Восстанавливаем строки в обратном порядке
        i = col.up
        while i != col:
            j = i.left
            while j != i:
                j.column_header.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up

        # Возвращаем столбец в список заголовков
        col.right.left = col
        col.left.right = col

    def search(self, k: int = 0) -> Generator[list[DataNode]]:
        if self.root.right == self.root:
            yield self.solution.copy()
            return

        # Выбор столбца с минимальным размером
        c = self.root.right
        min_size = float('inf')
        j = self.root.right
        while j != self.root:
            if j.size < min_size:
                c = j
                min_size = j.size
            j = j.right

        self.cover(c)

        r = c.down
        while isinstance(r, DataNode):
            self.solution.append(r)

            j = r.right
            while j != r:
                self.cover(j.column_header)
                j = j.right

            yield from self.search(k + 1)

            self.solution.pop()

            j = r.left
            while j != r:
                self.uncover(j.column_header)
                j = j.left

            r = r.down

        self.uncover(c)

    def solve(self):
        return list(self.search())

    def solve_iteratively(self, max_num: int = 0):
        sols: list[list[DataNode]] = []
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
                rows_to_delete: list[list[int]] = []
                for r in res:
                    row_to_delete = [1 if columns[i]
                                     in r else 0 for i in range(len(columns))]
                    if row_to_delete in m:
                        rows_to_delete.append(row_to_delete)
                for row in rows_to_delete:
                    m.remove(row)
            except StopIteration:
                break
        # return [show([sol])[0] for sol in sols]
        return sols


def show(solutions: list[list[DataNode]]):
    sols: list[frozenset[tuple[str, ...]]] = []
    for sol in solutions:
        rows: list[tuple[str, ...]] = []
        for node in sol:
            row = [node.column_header.name]
            current = node.right
            while current != node:
                row.append(current.column_header.name)
                current = current.right
            rows.append(tuple(sorted(row)))
        sols.append(frozenset(rows))
    return [sorted([t for t in s], key=lambda x: x[-1]) for s in set(sols)]


# Пример использования:
def example():
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


if __name__ == "__main__":
    example()
