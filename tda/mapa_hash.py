class MapaHash:
    def __init__(self, tamaño=100):
        self.tamaño = tamaño
        self.cubetas = [[] for _ in range(tamaño)]
    
    def _hash(self, clave):
        return hash(clave) % self.tamaño
    
    def insertar(self, clave, valor):
        hash_clave = self._hash(clave)
        cubeta = self.cubetas[hash_clave]
        
        for i, (k, v) in enumerate(cubeta):
            if k == clave:
                cubeta[i] = (clave, valor)
                return
        
        cubeta.append((clave, valor))
    
    def obtener(self, clave):
        hash_clave = self._hash(clave)
        cubeta = self.cubetas[hash_clave]
        
        for k, v in cubeta:
            if k == clave:
                return v
        
        return None
    
    def contiene(self, clave):
        return self.obtener(clave) is not None