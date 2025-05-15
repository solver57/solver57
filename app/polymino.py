def generate_polyominoes(n):
    def generate_recursive(current, remaining, visited):
        if remaining == 0:
            return [current]
        result = []
        for (x, y) in current:
            for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_cell = (x + dx, y + dy)
                if new_cell not in visited:
                    visited.add(new_cell)
                    result.extend(generate_recursive(current + [new_cell], remaining - 1, visited))
                    visited.remove(new_cell)
        return result

    def normalize(polyomino):
        min_x = min(x for x, y in polyomino)
        min_y = min(y for x, y in polyomino)
        return tuple(sorted((x - min_x, y - min_y) for x, y in polyomino))

    def generate_transformations(polyomino):
        transformations = set()
        for _ in range(4):
            polyomino = [(y, -x) for x, y in polyomino]
            transformations.add(normalize(polyomino))
            transformations.add(normalize([(-x, y) for x, y in polyomino]))
        return transformations

    unique_polyominoes = set()
    initial_cell = [(0, 0)]
    visited = set(initial_cell)
    all_polyominoes = generate_recursive(initial_cell, n - 1, visited)

    for polyomino in all_polyominoes:
        transformations = generate_transformations(polyomino)
        unique_polyominoes.add(min(transformations))

    return [[chr(ord('А') + i)] + list(p) for i, p in enumerate(unique_polyominoes)]

# Пример использования:
if __name__ == "__main__":
    n = 6  # Размер полимино
    polyominoes = generate_polyominoes(n)
    for poly in polyominoes:
        print(poly)
