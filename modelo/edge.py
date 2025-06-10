class Edge:
    """Estructura ligera de arista para un grafo."""
    __slots__ = '_origin', '_destination', '_element'

    def __init__(self, u, v, x):
        """No llamar al constructor directamente. Usar insert_edge(u,v,x) del grafo."""
        self._origin = u
        self._destination = v
        self._element = x

    def endpoints(self):
        """Retorna una tupla (u,v) para los vértices u y v."""
        return (self._origin, self._destination)

    def opposite(self, v):
        """Retorna el vértice que está opuesto a v en esta arista."""
        return self._destination if v is self._origin else self._origin

    def element(self):
        """Retorna el elemento asociado con esta arista."""
        return self._element

    def __hash__(self):
        """Permite que la arista sea una clave de mapa/conjunto."""
        return hash((self._origin, self._destination))

    def __str__(self):
        """Representación en cadena de la arista."""
        return f"({self._origin}->{self._destination}):{self._element}"

    def __repr__(self):
        """Representación oficial en cadena."""
        return f"Edge({self._origin}, {self._destination}, {self._element})"