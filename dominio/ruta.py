class Ruta:
    """
    Representa una ruta entre dos nodos del grafo.
    Almacena información sobre los nodos que componen la ruta, 
    su costo, prioridad y uso.
    
    Attributes:
        nodos: Lista de IDs de nodos que forman la ruta
        costo: Costo total de la ruta
        contador_uso: Contador de cuántas veces se ha usado la ruta
        prioridad: Nivel de prioridad de la ruta
        energia_requerida: Energía necesaria para completar la ruta
    """
    def __init__(self, nodos, costo, prioridad=1):
        self.nodos = nodos
        self.costo = costo
        self.contador_uso = 1  # Inicialmente se usa una vez
        self.prioridad = prioridad
        self.energia_requerida = costo * 1.2  # Estimación simple de consumo energético
    
    def incrementar_uso(self):
        """Incrementa el contador de uso de la ruta"""
        self.contador_uso += 1
    
    def obtener_longitud(self):
        """Retorna el número de nodos en la ruta"""
        return len(self.nodos) if self.nodos else 0
    
    def obtener_segmento(self, inicio, fin):
        """
        Obtiene un segmento de la ruta entre dos índices.
        
        Args:
            inicio: Índice inicial del segmento
            fin: Índice final del segmento
            
        Returns:
            Lista con los nodos del segmento o None si los índices son inválidos
        """
        if not self.nodos or inicio < 0 or fin >= len(self.nodos) or inicio > fin:
            return None
        return self.nodos[inicio:fin+1]
    
    def __str__(self):
        """Representación en string de la ruta"""
        return f"Ruta({' → '.join(map(str, self.nodos))}, costo={self.costo})"