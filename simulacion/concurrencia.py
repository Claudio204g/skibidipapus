import threading
import time
from collections import deque

class GestorConcurrencia:
    def __init__(self, simulacion):
        self.simulacion = simulacion
        self.drones = []
        self.cola_pedidos = deque()
        self.lock = threading.Lock()
        self.ejecutando = False
        self.thread_principal = None
    
    def agregar_drone(self, drone):
        with self.lock:
            self.drones.append(drone)
    
    def encolar_pedido(self, pedido):
        with self.lock:
            # Insertar el pedido según su prioridad (mayor prioridad al frente)
            for i, p in enumerate(self.cola_pedidos):
                if pedido.prioridad > p.prioridad:
                    self.cola_pedidos.insert(i, pedido)
                    return
            self.cola_pedidos.append(pedido)
    
    def asignar_pedidos(self):
        with self.lock:
            drones_disponibles = [d for d in self.drones if d.estado == "disponible"]
            
            while drones_disponibles and self.cola_pedidos:
                # Obtener el siguiente pedido
                pedido = self.cola_pedidos.popleft()
                
                # Encontrar el drone más cercano al origen del pedido
                mejor_drone = None
                menor_distancia = float('inf')
                
                for drone in drones_disponibles:
                    if drone.posicion_actual:
                        # Calcular distancia (simplificado)
                        ruta = self.simulacion.encontrar_ruta(drone.posicion_actual, pedido.origen)
                        if ruta:
                            distancia = len(ruta)
                            if distancia < menor_distancia:
                                menor_distancia = distancia
                                mejor_drone = drone
                
                if mejor_drone:
                    mejor_drone.asignar_pedido(pedido)
                    drones_disponibles.remove(mejor_drone)
                else:
                    # Si no hay drone adecuado, volver a encolar
                    self.cola_pedidos.appendleft(pedido)
                    break
    
    def iniciar_simulacion_concurrente(self):
        self.ejecutando = True
        self.thread_principal = threading.Thread(target=self._ciclo_simulacion)
        self.thread_principal.daemon = True
        self.thread_principal.start()
    
    def detener_simulacion(self):
        self.ejecutando = False
        if self.thread_principal:
            self.thread_principal.join(timeout=2)
    
    def _ciclo_simulacion(self):
        while self.ejecutando:
            self.asignar_pedidos()
            
            # Mover drones
            with self.lock:
                for drone in self.drones:
                    if drone.estado == "en_ruta":
                        drone.mover_siguiente_nodo()
            
            time.sleep(1)  # Esperar un segundo entre ciclos
