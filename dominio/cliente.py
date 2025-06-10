class Cliente:
    def __init__(self, id_nodo, ubicacion):
        self.id_nodo = id_nodo
        self.ubicacion = ubicacion
        self.pedidos = []
    
    def agregar_pedido(self, pedido):
        self.pedidos.append(pedido)
    
    def __str__(self):
        return f"Cliente(id_nodo={self.id_nodo}, ubicacion={self.ubicacion}, pedidos={len(self.pedidos)})"