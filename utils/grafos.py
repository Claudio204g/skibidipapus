from utils.vertice import Vertice
from utils.arista import Arista

class Grafo:
    """
    Implementación de un grafo no dirigido con pesos en las aristas.
    Usado para representar la red de entrega con drones.
    """
    def __init__(self):
        self.vertices = {}  # Diccionario de vértices: {id_vertice: objeto_vertice}
        self.aristas = {}   # Diccionario de aristas: {id_arista: objeto_arista}
    
    def agregar_vertice(self, id_vertice, rol=None):
        """
        Agrega un nuevo vértice al grafo si no existe.
        
        Args:
            id_vertice: Identificador único para el vértice
            rol: Función del nodo ('almacen', 'recarga', 'cliente')
        """
        if id_vertice not in self.vertices:
            self.vertices[id_vertice] = Vertice(id_vertice, rol)
    
    def agregar_arista(self, desde_vertice, hasta_vertice, peso):
        """
        Agrega una arista entre dos vértices con un peso determinado.
        
        Args:
            desde_vertice: ID del vértice de origen
            hasta_vertice: ID del vértice de destino
            peso: Peso de la arista (distancia, costo, etc.)
        """
        if desde_vertice in self.vertices and hasta_vertice in self.vertices:
            id_arista = f"{desde_vertice}-{hasta_vertice}"
            self.aristas[id_arista] = Arista(desde_vertice, hasta_vertice, peso)
    
    def obtener_vecinos(self, id_vertice):
        """
        Obtiene la lista de vértices adyacentes a un vértice dado.
        
        Args:
            id_vertice: ID del vértice del que se quieren obtener los vecinos
            
        Returns:
            Lista de IDs de vértices vecinos
        """
        vecinos = []
        for id_arista, arista in self.aristas.items():
            if arista.desde_vertice == id_vertice:
                vecinos.append(arista.hasta_vertice)
            elif arista.hasta_vertice == id_vertice:
                vecinos.append(arista.desde_vertice)
        return vecinos
    
    def obtener_peso_arista(self, desde_vertice, hasta_vertice):
        """
        Obtiene el peso de la arista entre dos vértices.
        
        Args:
            desde_vertice: ID del vértice de origen
            hasta_vertice: ID del vértice de destino
            
        Returns:
            Peso de la arista o None si no existe
        """
        # Verificar en ambas direcciones (grafo no dirigido)
        id_arista1 = f"{desde_vertice}-{hasta_vertice}"
        id_arista2 = f"{hasta_vertice}-{desde_vertice}"
        
        if id_arista1 in self.aristas:
            return self.aristas[id_arista1].peso
        elif id_arista2 in self.aristas:
            return self.aristas[id_arista2].peso
        return None  # No existe arista entre estos vértices