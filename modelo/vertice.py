class Vertice:
    """
    Representa un vértice (nodo) en el grafo.
    
    Attributes:
        id: Identificador único del vértice
        rol: Función del nodo en la red ('almacen', 'recarga', 'cliente')
    """
    def __init__(self, id_vertice, rol=None):
        self.id = id_vertice
        self.rol = rol  # 'almacen', 'recarga', 'cliente'
    
    def __str__(self):
        """Representación en string del vértice"""
        return f"Vertice({self.id}, rol={self.rol})"