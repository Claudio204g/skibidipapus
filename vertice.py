class Vertice:
    def __init__(self, id_vertice, rol=None):
        self.id = id_vertice
        self.rol = rol  # 'almacen', 'recarga', 'cliente'
    
    def __str__(self):
        return f"Vertice({self.id}, rol={self.rol})"