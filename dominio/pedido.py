import time

class Pedido:
    def __init__(self, id_pedido, origen, destino, ruta, prioridad=1):
        self.id = id_pedido
        self.origen = origen
        self.destino = destino
        self.ruta = ruta
        self.prioridad = prioridad  # 1: normal, 2: alta, 3: urgente
        self.estado = "pendiente"  # pendiente, en_proceso, entregado, fallido
        self.timestamp = time.time()
        self.tiempo_inicio = None
        self.tiempo_entrega = None
    
    def iniciar_entrega(self):
        self.estado = "en_proceso"
        self.tiempo_inicio = time.time()
    
    def completar_entrega(self):
        self.estado = "entregado"
        self.tiempo_entrega = time.time()
    
    def calcular_tiempo_entrega(self):
        if self.tiempo_entrega and self.tiempo_inicio:
            return self.tiempo_entrega - self.tiempo_inicio
        return None
    
    def __str__(self):
        return f"Pedido({self.id}, {self.origen} → {self.destino}, prioridad={self.prioridad})"