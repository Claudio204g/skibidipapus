class Ruta:
    def __init__(self, camino, costo):
        self.camino = camino
        self.costo = costo
        self.contador_uso = 0
    
    def incrementar_uso(self):
        self.contador_uso += 1
    
    def __str__(self):
        return f"Ruta({'→'.join(self.camino)}, costo={self.costo}, usos={self.contador_uso})"