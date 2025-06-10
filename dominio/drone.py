class Drone:
    """
    Representa un drone de entrega en la simulación.
    
    Attributes:
        id: Identificador único del drone
        energia_maxima: Capacidad máxima de energía
        energia_actual: Nivel actual de energía
        posicion_actual: ID del nodo donde se encuentra actualmente
        estado: Estado del drone ('disponible', 'en_ruta', 'recargando', 'inactivo')
        pedido_actual: Pedido que está entregando actualmente
        ruta_actual: Lista de nodos de la ruta actual
        progreso_ruta: Índice del nodo actual en la ruta
    """
    def __init__(self, id_drone, energia_maxima=100):
        self.id = id_drone
        self.energia_maxima = energia_maxima
        self.energia_actual = energia_maxima
        self.posicion_actual = None
        self.estado = "disponible"  # disponible, en_ruta, recargando, inactivo
        self.pedido_actual = None
        self.ruta_actual = None
        self.progreso_ruta = 0  # Índice del nodo actual en la ruta
    
    def asignar_pedido(self, pedido):
        """
        Asigna un pedido al drone.
        
        Args:
            pedido: Objeto Pedido a entregar
            
        Returns:
            True si se asignó correctamente, False en caso contrario
        """
        if self.estado != "disponible":
            return False
        
        self.pedido_actual = pedido
        self.ruta_actual = pedido.ruta.nodos
        self.posicion_actual = self.ruta_actual[0]
        self.progreso_ruta = 0
        self.estado = "en_ruta"
        pedido.iniciar_entrega()
        return True
    
    def mover_siguiente_nodo(self):
        """
        Mueve el drone al siguiente nodo en su ruta actual.
        Actualiza energía y estado según el movimiento.
        
        Returns:
            True si se movió correctamente, False en caso contrario
        """
        if self.estado != "en_ruta" or not self.ruta_actual:
            return False
        
        if self.progreso_ruta < len(self.ruta_actual) - 1:
            nodo_actual = self.ruta_actual[self.progreso_ruta]
            nodo_siguiente = self.ruta_actual[self.progreso_ruta + 1]
            
            # Calcular consumo de energía para este tramo
            peso = self.grafo.obtener_peso_arista(nodo_actual, nodo_siguiente)
            consumo = peso * 1.2 if peso else 0
            
            # Verificar si hay suficiente energía
            if consumo > self.energia_actual:
                self.estado = "inactivo"  # Drone sin energía
                return False
            
            # Actualizar energía y posición
            self.energia_actual -= consumo
            self.progreso_ruta += 1
            self.posicion_actual = nodo_siguiente
            
            # Verificar si es nodo de recarga para recargar energía
            if self.grafo.vertices[nodo_siguiente].rol == 'recarga':
                self.recargar()
            
            # Verificar si hemos llegado al destino
            if self.progreso_ruta == len(self.ruta_actual) - 1:
                self.completar_entrega()
            
            return True
        return False
    
    def recargar(self, cantidad=50):
        """
        Recarga la energía del drone.
        
        Args:
            cantidad: Cantidad de energía a recargar
        """
        self.energia_actual = min(self.energia_actual + cantidad, self.energia_maxima)
        if self.estado == "recargando":
            self.estado = "en_ruta" if self.pedido_actual else "disponible"
    
    def completar_entrega(self):
        """
        Marca el pedido actual como completado y libera el drone.
        """
        if self.pedido_actual:
            self.pedido_actual.completar_entrega()
            self.pedido_actual = None
            self.ruta_actual = None
            self.progreso_ruta = 0
            self.estado = "disponible"
