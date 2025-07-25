import heapq
import mytimeit


def dijkstra_min_path(grid, cell):
    rows, cols = len(grid), len(grid[0])
    dist = [[float("inf")] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]

    heap = [(grid[0][cell], 0, cell)]
    dist[0][cell] = grid[0][cell]
    directions = [(1, 0), (0, -1), (0, 1)]  # Down, Left, Right

    while heap:
        cost, r, c = heapq.heappop(heap)

        if r == rows - 1:
            path = []
            while (r, c) != (0, 0):
                path.append((r, c))
                r, c = parent[r][c] if parent[r][c] else (0, 0)
            return dist[path[0][0]][path[0][1]], path[::-1]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + grid[nr][nc]
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    parent[nr][nc] = (r, c)
                    heapq.heappush(heap, (new_cost, nr, nc))

    return None, []


def print_grid_with_path(grid, path):
    path_set = set(path)
    print("\n📊 Grid with Shortest Path:")
    for r in range(len(grid)):
        row = ""
        for c in range(len(grid[0])):
            val = f"{grid[r][c]:3}"
            if (r, c) in path_set:
                row += f"[{val}]"
            else:
                row += f" {val} "
        print(row)


# Input grid (parsed)
# grid = [
#     [805, 537, 630, 201, 131],
#     [732, 699, 803,  96, 673],
#     [524, 497, 746, 342, 234],
#     [ 37, 121, 422, 965, 103],
#     [331, 956, 111, 150,  18]
# ]


def read_matrix_from_file(filepath):
    matrix = []
    with open(filepath, "r") as file:
        for line in file:
            row = list(map(int, line.strip().split(",")))
            matrix.append(row)
    return matrix


def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]


with mytimeit.MyTimer() as t:
    # Run it
    filepath = "./0082_matrix.txt"
    matrix = read_matrix_from_file(filepath)
    transposed = transpose_matrix(matrix)

    min_cost = float("inf")
    for i in range(len(transposed)):
        cost, path = dijkstra_min_path(transposed, i)
        min_cost = min(min_cost, cost)


print("Minimum cost to last row:", min_cost)
# print("Path:", path)
# print_grid_with_path(grid, path)
