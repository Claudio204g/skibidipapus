from vertice import Vertice
from arista import Arista

class Grafo:
    def __init__(self):
        self.vertices = {}
        self.aristas = {}
    
    def agregar_vertice(self, id_vertice, rol=None):
        if id_vertice not in self.vertices:
            self.vertices[id_vertice] = Vertice(id_vertice, rol)
    
    def agregar_arista(self, desde_vertice, hasta_vertice, peso):
        if desde_vertice in self.vertices and hasta_vertice in self.vertices:
            id_arista = f"{desde_vertice}-{hasta_vertice}"
            self.aristas[id_arista] = Arista(desde_vertice, hasta_vertice, peso)
    
    def obtener_vecinos(self, id_vertice):
        vecinos = []
        for id_arista, arista in self.aristas.items():
            if arista.desde_vertice == id_vertice:
                vecinos.append(arista.hasta_vertice)
            elif arista.hasta_vertice == id_vertice:
                vecinos.append(arista.desde_vertice)
        return vecinos
    
    def obtener_peso_arista(self, desde_vertice, hasta_vertice):
        id_arista1 = f"{desde_vertice}-{hasta_vertice}"
        id_arista2 = f"{hasta_vertice}-{desde_vertice}"
        
        if id_arista1 in self.aristas:
            return self.aristas[id_arista1].peso
        elif id_arista2 in self.aristas:
            return self.aristas[id_arista2].peso
        return None