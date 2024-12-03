

class UGraph:
    def __init__(self, vertices, edges):
        new_vertices = []
        for v in vertices:
            new_vertices.append(tuple(v))

        new_edges = []
        for e in edges:
            new_edges.append((tuple(e[0]), tuple(e[1])))

        self.vertices = new_vertices     # List of the vertices of the graph
        self.edges = new_edges      # List of edges of the graph

        self.vertices_edges = dict()

        for v in self.vertices:
            self.vertices_edges[v] = []

        for e in self.edges:
            v1 = e[0]
            v2 = e[1]
            if v2 not in self.vertices_edges[v1]:
                self.vertices_edges[v1].append(v2)
            if v1 not in self.vertices_edges[v2]:
                self.vertices_edges[v2].append(v1)

        self.SCCs = []

    def compute_SCCs(self):
        self.indices = dict()
        self.lowlink = dict()
        self.onstack = dict()
        for v in self.vertices:
            self.indices[v] = -1
            self.lowlink[v] = -1
            self.onstack[v] = False
        self.index = 0
        self.stack = []
        for v in self.vertices:
            if self.indices[v] == -1:
                self.strongconnect(v)

    def strongconnect(self, v):
        self.indices[v] = self.index
        self.lowlink[v] = self.index
        self.index = self.index+1
        self.stack.append(v)
        self.onstack[v] = True

        for w in self.vertices_edges[v]:
            if self.indices[w] == -1:
                self.strongconnect(w)
                self.lowlink[v] = min(self.lowlink[v], self.lowlink[w])
            elif self.onstack[w]:
                self.lowlink[v] = min(self.lowlink[v], self.indices[w])


        if self.lowlink[v] == self.indices[v]:
            scc = []
            while self.stack[-1] != v:
                w = self.stack.pop()
                self.onstack[w] = False
                scc.append(w)
            scc.append(v)
            self.SCCs.append(scc)

