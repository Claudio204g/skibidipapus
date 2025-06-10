class Vertex:
    """Estructura ligera de vértice para un grafo."""
    __slots__ = '_element', 'rol'

    def __init__(self, element):
        """No llamar al constructor directamente. Usar insert_vertex(element) del grafo."""
        self._element = element
        self.rol = None  # Puede ser 'almacen', 'recarga' o 'cliente'

    def element(self):
        """Retorna el elemento asociado con este vértice."""
        return self._element

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return str(self._element)

    def __repr__(self):
        return f"Vertex({self._element})"
