from modelo.vertex import Vertex
from modelo.edge import Edge

class Graph:
    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing
        self._directed = directed

    def is_directed(self):
        """Retorna True si el grafo es dirigido, False en caso contrario."""
        return self._directed

    def insert_vertex(self, element):
        """Inserta y retorna un nuevo vértice con el elemento dado."""
        v = Vertex(element)
        self._outgoing[v] = {}
        if self._directed:
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, element):
        """Inserta y retorna una nueva arista desde u a v con elemento auxiliar."""
        e = Edge(u, v, element)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e

    def remove_edge(self, u, v):
        """Elimina la arista de u a v, si existe."""
        if u in self._outgoing and v in self._outgoing[u]:
            del self._outgoing[u][v]
            del self._incoming[v][u]

    def remove_vertex(self, v):
        """Elimina el vértice v y todas sus aristas incidentes."""
        for u in list(self._outgoing.get(v, {})):
            self.remove_edge(v, u)
        for u in list(self._incoming.get(v, {})):
            self.remove_edge(u, v)
        self._outgoing.pop(v, None)
        if self._directed:
            self._incoming.pop(v, None)

    def get_edge(self, u, v):
        """Retorna la arista de u a v, o None si no existe."""
        return self._outgoing.get(u, {}).get(v)

    def vertices(self):
        """Retorna un iterador de todos los vértices del grafo."""
        return self._outgoing.keys()

    def edges(self):
        """Retorna un conjunto de todas las aristas del grafo."""
        seen = set()
        for map in self._outgoing.values():
            seen.update(map.values())
        return seen

    def neighbors(self, v):
        """Retorna un iterador de todos los vértices adyacentes a v."""
        return self._outgoing[v].keys()

    def degree(self, v, outgoing=True):
        """Retorna el número de aristas salientes (o entrantes) de v."""
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """Retorna un iterador de todas las aristas incidentes a v."""
        adj = self._outgoing if outgoing else self._incoming
        return adj[v].values()
