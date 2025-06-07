class Pedido:
    def __init__(self, id_pedido, origen, destino, ruta=None):
        self.id_pedido = id_pedido
        self.origen = origen
        self.destino = destino
        self.ruta = ruta
        self.completado = False
    
    def completar_pedido(self):
        self.completado = True
    
    def __str__(self):
        return f"Pedido({self.id_pedido}, {self.origen}→{self.destino}, completado={self.completado})"