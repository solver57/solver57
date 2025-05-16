from collections import defaultdict


class Figure:
    def __init__(self, name: str, fig: list[tuple[int, int]]):
        self.fig = fig
        self.name = name
        self.variants = self.generate_variants()

    def generate_variants(self) -> dict[str, list[tuple[int, int]]]:
        variants: list[list[tuple[int, int]]] = []
        for x, y in self.fig:
            variants.append([(x, y), (-y, x), (-x, -y), (y, -x),
                            (x, -y), (-y, -x), (-x, y), (y, x)])
        transformed = list(zip(*variants))
        shifted: set[frozenset[tuple[int, int]]] = set()
        for t in transformed:
            left = min(x for x, _ in t)
            bottom = min(y for _, y in t)
            t = frozenset((x - left, y - bottom) for x, y in t)
            shifted.add(t)
        return {self.name + '_' + str(i): list(t) for i, t in enumerate(shifted)}

    def __repr__(self):
        ss = f'_______{self.name}_______\n'
        for v in self.variants:
            var = self.variants[v]
            width, height = (max(x for x, _ in var) + 1,
                             max(y for _, y in var) + 1)
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


def occupy(mino: list[tuple[int, int]], x: int, y: int):
    start_x, start_y = mino[0]
    occ: list[tuple[int, int]] = []
    for dx, dy in mino:
        point = dx - start_x + x, dy - start_y + y
        occ.append(point)
    return occ


class Board:
    def __init__(self, h: int, w: int):
        self.matrix = [
            [f'{i:0>2}_{j:0>2}' for j in range(w)] for i in range(h)]
        self.allowed = defaultdict(
            lambda: 0, {(i, j): 1 for j in range(w) for i in range(h)})

    def __repr__(self):
        return "\n".join([" ".join([self.matrix[i][j] if self.allowed[(i, j)] else ' ... ' for j in
                                    range(len(self.matrix[0]))])
                          for i in range(len(self.matrix))]) + "\n"

    def flip(self, coord1: int, coord2: int):
        if (coord1, coord2) in self.allowed:
            self.allowed[(coord1, coord2)] = 1 - self.allowed[(coord1, coord2)]

    def check(self, mino: list[tuple[int, int]], x: int, y: int):
        occ = occupy(mino, x, y)
        return all(self.allowed[p] for p in sorted(occ))

    def place(self, solution: list[tuple[int, int]], figure: str):
        for p in solution[:-1]:
            x, y = p
            # self.flip(*p)
            self.matrix[x][y] = figure


def generate_column_names(board: Board, variants: dict[str, list[tuple[int, int]]]):
    return [morf(p) for p in board.allowed] + \
        list({s.split('_')[0] for s in variants}) + ['exclude']


def morf(p: tuple[int, int]):
    i, j = p
    return f'{i:0>2}_{j:0>2}'


def generate_matrix(board: Board, f_variants: dict[str, list[tuple[int, int]]], names: list[str]):
    lines: list[list[int]] = []
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
                a = tuple(map(int, p.split('_')))
                if not board.allowed[a[0], a[1]]:
                    ind = names.index(p)
                    excluded_line[ind] = 1
        lines.append(excluded_line)
    return lines
