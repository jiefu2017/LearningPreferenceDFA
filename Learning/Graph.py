
class Graph:
    def __init__(self):
        self.vertices = []     # List of the vertices of the graph
        self.edges = []      # List of edges of the graph

        self.vertex_outEdges = dict()  # For each vertex v, self.vertex_outEdges[v] is the set of edges that
                                        # are outgoing from v

        self.connectivity_matrx = {}


        

    def addVertex(self, vertex):
        self.vertices.append(vertex)
        print(f"vertex: {vertex}")
        self.vertex_outEdges[vertex] = []

    def addEdge(self, edge):
        if edge in self.edges:
            return
        self.edges.append(edge)
        #print(f"edge: {edge}")
        src = edge[0]
        dst = edge[1]
        #print(f"src: {src}")
        if src not in self.vertex_outEdges.keys():
            self.vertex_outEdges[src] = []
        if edge not in self.vertex_outEdges[src]:
            self.vertex_outEdges[src].append(edge)

    def compute_connectivity_matrix(self):
        print("Started computing the connectivity matrix of the preference graph")
        for vertex in self.vertices:
            self.connectivity_matrx[vertex] = {}
            for vertex2 in self.vertices:
                self.connectivity_matrx[vertex][vertex2] = False
            self.connectivity_matrx[vertex][vertex] = True

        for v in self.vertices:
            visited = {}
            for v2 in self.vertices:
                visited[v2] = False
            visited[v] = True
            queue = []
            queue.append(v)
            while queue:
                v2 = queue.pop(0)
                #print(f"v2: {v2}")
                self.connectivity_matrx[v][v2] = True
                visited[v2] = True
                for e in self.vertex_outEdges[v2]:
                    if visited[e[1]]:
                        continue
                    queue.append(e[1])

    '''
    It returns for a given vertex, the set of vertices that are preferred to that vertex or
    have the same priority with that vertex.
    Vertex v2 is prefered to vertex v1 if there is a path from v2 to v1. 
    '''
    def getVerticesPreferredBy(self, vertx):
        result = set()
        result.add(vertx)
        if len(self.connectivity_matrx.keys()) == 0:
            self.compute_connectivity_matrix()
        for v in self.vertices:
            #if self.connectivity_matrx[v][vertx]:
            if self.connectivity_matrx[v][vertx]:
                if v not in result:
                    result.add(v)
        return result

    def getVerticesPreferredTo(self, vertx):
        result = set()
        result.add(vertx)
        if len(self.connectivity_matrx.keys()) == 0:
            self.compute_connectivity_matrix()
        for v in self.vertices:
            #if self.connectivity_matrx[v][vertx]:
            if self.connectivity_matrx[vertx][v]:
                if v not in result:
                    result.add(v)
        return result

    def getVerticesPreferredToSubset(self, vertx_subset):
        result = set()
        for vertex in vertx_subset:
            subset = self.getVerticesPreferredTo(vertex)
            result = result.union(subset)
        return result

    def printAll(self):
        print("-------------Graph-----------------")
        print(f"vertices: {self.vertices}")
        print(f"edges: {self.edges}")
        print("-----------------------------------")