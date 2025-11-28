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

        # Basic bounds checking
        if n > 0 and (0 <= source < n) and (0 <= target < n):

            # no_edge = graph[0][0] = 0, meaning no capacity
            no_edge: int = graph[0][0]

            # Marked set = nodes we have already visited
            marked: list[int] = [source]

            found: bool = False

            # Stack for DFS:
            # Each entry is (current_node, path_to_this_node)
            stack: list[(int, list[int])] = [(source, [source])]

            # Standard DFS loop
            while len(stack) > 0 and not found:

                # Pop next item
                (u, path_from_source_to_u) = stack.pop()

                # If u == target -> we found a path
                found = u == target
                if found:
                    path = path_from_source_to_u
                else:
                    # Explore neighbors in reverse order (n-1 down to 0)
                    v: int = n - 1
                    while v >= 0:

                        # If edge exists (capacity > 0) and not visited
                        if graph[u][v] != no_edge and v not in marked:
                            marked.append(v)
                            # Push next vertex with updated path
                            stack.append((v, path_from_source_to_u + [v]))
                        v -= 1

    return path


# FordFulkerson class
class FordFulkerson:
    def __init__(self, graph, source, target):
        import copy

        # Make a deep copy of the original graph
        self.graph = copy.deepcopy(graph)

        # Residual graph starts as identical to original capacities
        self.residual = copy.deepcopy(graph)

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

            # Reduce forward capacity
            self.residual[u][v] -= m

            # Increase backward capacity (allows undo)
            self.residual[v][u] += m

    # Find reachable vertices from the source in the residual graph
    def reachable_from_source(self):
        marked = set([self.source])
        stack = [self.source]
        while stack:
            u = stack.pop()
            for v in range(self.n):

                # Residual capacity > 0 means reachable
                if self.residual[u][v] > 0 and v not in marked:
                    marked.add(v)
                    stack.append(v)

        return marked

    # Main Ford-Fulkerson algorithm
    def run(self):

        # Augment while paths exist
        while True:
            path = find_path(self.residual, self.source, self.target)

            # If no augmenting path is found, we're done
            if path is None:
                break

            # Get bottleneck capacity
            m = self.path_capacity(path)

            # Increase total max flow
            self.max_flow += m

            # Update residual graph
            self.apply_flow(path, m)

        # S = set of reachable vertices in residual graph
        S = self.reachable_from_source()
        T = set(range(self.n)) - S

        cut = []

        # For every edge (u->v) in original graph,
        # if u in S and v in T -> edge crosses the min cut
        for u in S:
            for v in T:
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
