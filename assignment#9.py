# Graph G
G = [  #  A  B  C  D  E
    [0, 20, 0, 0, 0],  # A
    [0, 0, 5, 6, 0],  # B
    [0, 0, 0, 3, 7],  # C
    [0, 0, 0, 0, 8],  # D
    [0, 0, 0, 0, 0],  # E
]


# find_path function
def find_path(graph: list[list[int]], source: int, target: int):

    path: list[int] = None

    if graph is not None:
        n: int = len(graph)
        if n > 0 and (0 <= source < n) and (0 <= target < n):

            no_edge: int = graph[0][0]
            marked: list[int] = [source]
            found: bool = False

            stack: list[(int, list[int])] = [(source, [source])]

            while len(stack) > 0 and not found:
                (u, path_from_source_to_u) = stack.pop()
                found = u == target
                if found:
                    path = path_from_source_to_u
                else:
                    v: int = n - 1
                    while v >= 0:
                        if graph[u][v] != no_edge and v not in marked:
                            marked.append(v)
                            stack.append((v, path_from_source_to_u + [v]))
                        v -= 1

    return path


# FordFulkerson class
class FordFulkerson:
    def __init__(self, graph, source, target):
        import copy

        self.graph = copy.deepcopy(graph)
        self.residual = copy.deepcopy(graph)  # Initial residual graph
        self.source = source
        self.target = target
        self.n = len(graph)
        self.max_flow = 0

    # Compute bottleneck capacity of an augmenting path
    def path_capacity(self, path):
        m = float("inf")
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            m = min(m, self.residual[u][v])
        return m

    # Update residual graph with flow m along path
    def apply_flow(self, path, m):
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            self.residual[u][v] -= m
            self.residual[v][u] += m

    # Find reachable vertices from the source in the residual graph
    def reachable_from_source(self):
        marked = set([self.source])
        stack = [self.source]
        while stack:
            u = stack.pop()
            for v in range(self.n):
                if self.residual[u][v] > 0 and v not in marked:
                    marked.add(v)
                    stack.append(v)
        return marked

    # Main Ford-Fulkerson algorithm
    def run(self):
        while True:
            path = find_path(self.residual, self.source, self.target)
            if path is None:
                break

            m = self.path_capacity(path)
            self.max_flow += m
            self.apply_flow(path, m)

        # After flow is done, compute min cut
        S = self.reachable_from_source()
        T = set(range(self.n)) - S

        cut = []
        for u in S:
            for v in T:
                # edge existed in original graph and crosses cut
                if self.graph[u][v] > 0:
                    cut.append((u, v))

        return self.max_flow, cut, self.residual


# Run solver
solver = FordFulkerson(G, 0, 4)
max_flow, cut, residual = solver.run()

# Print results
print("Max Flow =", max_flow)
print("Min Cut Edges =", cut)
for row in residual:
    print(row)
