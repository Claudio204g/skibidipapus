class Arista:
    def __init__(self, desde_vertice, hasta_vertice, peso):
        self.desde_vertice = desde_vertice
        self.hasta_vertice = hasta_vertice
        self.peso = peso
    
    def __str__(self):
        return f"Arista({self.desde_vertice}→{self.hasta_vertice}, peso={self.peso})"