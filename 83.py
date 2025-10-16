#!/usr/bin/env python3
import sys
import heapq
import mytimeit


def load_grid(path: str):
    """
    Reads a matrix of integers from `path`.
    Accepts rows with space or comma separators.
    """
    grid = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # allow commas or spaces
            if "," in line:
                row = [int(x) for x in line.split(",") if x.strip()]
            else:
                row = [int(x) for x in line.split() if x.strip()]
            grid.append(row)
    if not grid or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("Malformed grid: empty or non-rectangular.")
    return grid


def to_index(r, c, cols):
    """Convert row/column coordinates to a linear node index."""
    return r * cols + c


def from_index(idx, cols):
    """Convert a linear node index back to row and column."""
    return divmod(idx, cols)


def build_adjacency(grid):
    """
    Build an adjacency list for 4-neighbor moves (up/down/left/right).
    Node id = r*cols + c. Edge weight = value of the destination cell.
    (Cost model: entering a cell costs that cell's value.)
    """
    R, C = len(grid), len(grid[0])
    adj = {to_index(r, c, C): [] for r in range(R) for c in range(C)}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(R):
        for c in range(C):
            u = to_index(r, c, C)
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    v = to_index(nr, nc, C)
                    w = grid[nr][nc]  # cost to move into neighbor
                    adj[u].append((v, w))
    return adj


def dijkstra_min_path_sum(grid, adj):
    """
    Dijkstra from (0,0) to (R-1,C-1).
    Distance initialized with cost of the start cell.
    """
    R, C = len(grid), len(grid[0])
    start = 0
    goal = to_index(R - 1, C - 1, C)

    dist = {u: float("inf") for u in adj}
    prev = {u: None for u in adj}

    dist[start] = grid[0][0]  # include start cell cost
    pq = [(dist[start], start)]
    seen = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == goal:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    # reconstruct path
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    return dist[goal], path  # total cost, list of node indices


def pretty_path(path, grid):
    """Translate a path of node indices into grid coordinates and values."""
    R, C = len(grid), len(grid[0])
    coords = [from_index(idx, C) for idx in path]
    values = [grid[r][c] for r, c in coords]
    return coords, values


with mytimeit.MyTimer() as t:
    if len(sys.argv) != 2:
        print("Usage: python dijkstra_grid.py <path_to_matrix_file>")
        sys.exit(1)

    grid = load_grid(sys.argv[1])
    adj = build_adjacency(grid)
    total_cost, path = dijkstra_min_path_sum(grid, adj)
    coords, vals = pretty_path(path, grid)

    # print("Grid size:", len(grid), "x", len(grid[0]))
    print("Minimum-sum path cost:", total_cost)
    # print("Path (r,c):", coords)
    # print("Path values:", vals)
