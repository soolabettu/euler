import sys

from mytimeit import *


def find(parent, x):
    """Return the representative element for x in the union-find structure."""
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]


def union(parent, rank, x, y):
    """Union the sets containing x and y while maintaining union-by-rank invariants."""
    root_x = find(parent, x)
    root_y = find(parent, y)
    if root_x != root_y:
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1


def kruskal_mst(adj_matrix):
    """Return the MST edges and total weight for the given adjacency matrix."""
    n = len(adj_matrix)
    edges = []
    # Build list of edges
    for i in range(n):
        for j in range(i + 1, n):
            w = adj_matrix[i][j]
            if w > 0:
                edges.append((w, i, j))
    # Sort by weight
    edges.sort(key=lambda x: x[0])

    parent = [i for i in range(n)]
    rank = [0] * n

    mst_edges = []
    mst_weight = 0

    for weight, u, v in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_edges.append((u, v, weight))
            mst_weight += weight
            if len(mst_edges) == n - 1:
                break

    return mst_edges, mst_weight


def parse_adjacency_matrix(lines):
    """Parse the weighted adjacency matrix from CSV-style text lines."""
    matrix = []
    for line in lines:
        values = line.strip().split(",")
        row = [0 if val.strip() == "-" else int(val.strip()) for val in values]
        matrix.append(row)
    return matrix


def total_weight_of_graph(adj_matrix):
    """Sum the weights of the undirected edges in the adjacency matrix."""
    n = len(adj_matrix)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += adj_matrix[i][j]
    return total


def solve():
    """Compute the savings achieved by replacing a network with its minimum spanning tree."""
    # Read lines (replace with your desired input method)
    lines = sys.stdin.read().strip().splitlines()

    # 1. Parse adjacency matrix
    adj_matrix = parse_adjacency_matrix(lines)

    # 2. Total weight of original graph
    original_weight = total_weight_of_graph(adj_matrix)

    # 3. Build MST using Kruskal
    mst_edges, mst_weight = kruskal_mst(adj_matrix)

    # 4. Calculate savings
    savings = original_weight - mst_weight

    # Print results
    # print("Original Graph Total Weight:", original_weight)
    # print("MST Total Weight:", mst_weight)
    print("Total Savings:", savings)

    # print("\nEdges in MST (0-based indices):")
    # for (u, v, w) in mst_edges:
    #     print(f"{u} -- {v} (weight = {w})")

    # print("\nAdjacency Matrix:")


if __name__ == "__main__":
    with MyTimer(solve) as timer:
        solve()
