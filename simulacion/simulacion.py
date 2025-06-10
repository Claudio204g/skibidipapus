from tda.arbol_avl import ArbolAVL
from dominio.pedido import Pedido
from dominio.ruta import Ruta
from collections import defaultdict
import random

class Simulacion:
    """
    Clase principal que controla la simulación de entregas con drones.
    Maneja el grafo de la red, pedidos, rutas y estadísticas.
    """
    def __init__(self):
        self.grafo = None  # Grafo que representa la red de nodos
        self.seguimiento_rutas = ArbolAVL()  # Árbol AVL para guardar y recuperar rutas eficientemente
        self.pedidos = []  # Lista de pedidos procesados
        self.estadisticas_nodos = defaultdict(lambda: {'como_origen': 0, 'como_destino': 0})  # Estadísticas de uso de nodos
    
    def generar_pedidos_aleatorios(self, n_pedidos):
        """
        Genera pedidos aleatorios entre almacenes y clientes.
        
        Args:
            n_pedidos: Número de pedidos a generar
            
        Returns:
            Lista de tuplas (origen, destino) para los pedidos
        """
        # Obtener nodos según su rol
        nodos_almacen = [v.id for v in self.grafo.vertices.values() if v.rol == 'almacen']
        nodos_cliente = [v.id for v in self.grafo.vertices.values() if v.rol == 'cliente']
        
        # Verificar que haya nodos de ambos tipos
        if not nodos_almacen or not nodos_cliente:
            return []
        
        # Generar pares origen-destino aleatorios
        return [(random.choice(nodos_almacen), random.choice(nodos_cliente)) for _ in range(n_pedidos)]
    
    def procesar_pedido(self, origen, destino, algoritmo='BFS'):
        """
        Procesa un pedido calculando la mejor ruta y registrando estadísticas.
        
        Args:
            origen: ID del nodo de origen
            destino: ID del nodo de destino
            algoritmo: Algoritmo de búsqueda a utilizar ('BFS', 'DFS', 'Dijkstra')
            
        Returns:
            Objeto Pedido creado o None si no se pudo encontrar ruta
        """
        # Encontrar la mejor ruta según el algoritmo especificado
        ruta = self.encontrar_ruta(origen, destino, algoritmo)
        
        if ruta:
            # Calcular costo y crear objeto Ruta
            costo = self.calcular_costo_ruta(ruta)
            objeto_ruta = Ruta(ruta, costo)
            
            # Registrar en el árbol AVL para seguimiento
            clave = (origen, destino)
            if self.seguimiento_rutas.contiene(clave):
                existente = self.seguimiento_rutas.obtener(clave)
                existente.append(objeto_ruta)
            else:
                self.seguimiento_rutas.insertar(clave, [objeto_ruta])
            
            # Actualizar estadísticas de uso de nodos
            self.estadisticas_nodos[origen]['como_origen'] += 1
            self.estadisticas_nodos[destino]['como_destino'] += 1
            
            # Crear y registrar el pedido
            pedido = Pedido(len(self.pedidos), origen, destino, objeto_ruta)
            self.pedidos.append(pedido)
            return pedido
        return None  # No se encontró ruta válida
    
    def encontrar_ruta(self, inicio, fin, algoritmo='BFS'):
        """
        Encuentra la mejor ruta entre dos nodos usando el algoritmo especificado.
        
        Args:
            inicio: ID del nodo inicial
            fin: ID del nodo final
            algoritmo: Algoritmo a utilizar ('BFS', 'DFS', 'Dijkstra')
            
        Returns:
            Lista de nodos que forman la ruta o None si no hay ruta
        """
        if algoritmo == 'BFS':
            return self.ruta_bfs(inicio, fin)
        elif algoritmo == 'DFS':
            return self.ruta_dfs(inicio, fin)
        elif algoritmo == 'Dijkstra':
            return self.ruta_dijkstra(inicio, fin)
        else:
            return None
    
    def ruta_bfs(self, inicio, fin, energia_inicial=100):
        """
        Implementa Breadth-First Search para encontrar la ruta más corta
        considerando limitaciones de energía.
        
        Args:
            inicio: ID del nodo inicial
            fin: ID del nodo final
            energia_inicial: Energía con la que parte el drone
            
        Returns:
            Lista de nodos que forman la ruta o None si no hay ruta factible
        """
        # Caso base: origen y destino son el mismo
        if inicio == fin:
            return [inicio]
        
        # Inicialización de BFS
        visitados = set([inicio])
        cola = [[inicio]]  # Cola de rutas parciales
        nodos_recarga = [v.id for v in self.grafo.vertices.values() if v.rol == 'recarga']
        
        while cola:
            ruta = cola.pop(0)  # Obtener primera ruta de la cola
            nodo = ruta[-1]  # Último nodo de la ruta actual
            energia_restante = self._calcular_energia_restante(ruta, energia_inicial, nodos_recarga)
            
            # Explorar vecinos
            for vecino in self.grafo.obtener_vecinos(nodo):
                if vecino not in visitados:
                    peso = self.grafo.obtener_peso_arista(nodo, vecino)
                    energia_requerida = peso * 1.2 if peso else 0  # Consumo de energía para esta arista
                    
                    # Verificar si hay suficiente energía para moverse
                    if energia_requerida <= energia_restante:
                        nueva_ruta = list(ruta)
                        nueva_ruta.append(vecino)
                        
                        # Si encontramos el destino, devolvemos la ruta
                        if vecino == fin:
                            return nueva_ruta
                        
                        visitados.add(vecino)
                        cola.append(nueva_ruta)
        
        return None  # No se encontró ruta factible
    
    def _calcular_energia_restante(self, ruta, energia_inicial, nodos_recarga):
        """
        Calcula la energía restante después de seguir una ruta determinada.
        Tiene en cuenta estaciones de recarga en el camino.
        
        Args:
            ruta: Lista de nodos que forman la ruta
            energia_inicial: Energía máxima del drone
            nodos_recarga: Lista de IDs de nodos de recarga
            
        Returns:
            Energía restante al final de la ruta
        """
        energia_restante = energia_inicial
        
        # Recorrer la ruta calculando el consumo
        for i in range(len(ruta) - 1):
            peso = self.grafo.obtener_peso_arista(ruta[i], ruta[i+1])
            if peso:
                energia_restante -= peso * 1.2  # Consumo proporcional al peso
            
            # Recargar si estamos en un nodo de recarga
            if ruta[i+1] in nodos_recarga:
                energia_restante = min(energia_restante + 50, energia_inicial)  # Recarga parcial
                
        return energia_restante
    
    def ruta_dfs(self, inicio, fin, max_profundidad=100):
        """
        Implementa Depth-First Search para encontrar una ruta.
        
        Args:
            inicio: ID del nodo inicial
            fin: ID del nodo final
            max_profundidad: Profundidad máxima de búsqueda para evitar ciclos infinitos
            
        Returns:
            Lista de nodos que forman la ruta o None si no hay ruta
        """
        visitados = set()
        ruta = []
        encontrado = [False]  # Uso de lista para poder modificarlo en la función anidada
        
        def dfs_recursivo(nodo, profundidad):
            # Caso base: profundidad máxima alcanzada
            if profundidad > max_profundidad:
                return
            
            visitados.add(nodo)
            ruta.append(nodo)
            
            # Si encontramos el destino, terminamos
            if nodo == fin:
                encontrado[0] = True
                return
            
            # Explorar vecinos no visitados
            for vecino in self.grafo.obtener_vecinos(nodo):
                if vecino not in visitados and not encontrado[0]:
                    dfs_recursivo(vecino, profundidad + 1)
            
            # Si no encontramos el destino por este camino, retroceder (backtracking)
            if not encontrado[0]:
                ruta.pop()
        
        # Iniciar búsqueda DFS
        dfs_recursivo(inicio, 0)
        return ruta if encontrado[0] else None
    
    def ruta_dijkstra(self, inicio, fin, energia_inicial=100):
        """
        Implementa el algoritmo de Dijkstra para encontrar la ruta de menor costo
        considerando limitaciones de energía.
        
        Args:
            inicio: ID del nodo inicial
            fin: ID del nodo final
            energia_inicial: Energía con la que parte el drone
            
        Returns:
            Lista de nodos que forman la ruta óptima o None si no hay ruta factible
        """
        # Caso base: origen y destino son el mismo
        if inicio == fin:
            return [inicio]
        
        # Inicializar distancias como infinito
        distancias = {vertice: float('infinity') for vertice in self.grafo.vertices}
        distancias[inicio] = 0
        
        # Predecesores para reconstruir la ruta
        predecesores = {vertice: None for vertice in self.grafo.vertices}
        
        # Energía restante al llegar a cada nodo
        energia_restante = {vertice: 0 for vertice in self.grafo.vertices}
        energia_restante[inicio] = energia_inicial
        
        # Nodos no visitados y nodos de recarga
        no_visitados = list(self.grafo.vertices.keys())
        nodos_recarga = [v.id for v in self.grafo.vertices.values() if v.rol == 'recarga']
        
        while no_visitados:
            # Encontrar el nodo con menor distancia entre los no visitados
            actual = min(no_visitados, key=lambda x: distancias[x])
            
            # Si llegamos al destino o no hay ruta posible
            if actual == fin or distancias[actual] == float('infinity'):
                break
                
            no_visitados.remove(actual)
            
            # Explorar vecinos no visitados
            for vecino in self.grafo.obtener_vecinos(actual):
                if vecino not in no_visitados:
                    continue
                    
                peso = self.grafo.obtener_peso_arista(actual, vecino)
                if not peso:
                    continue
                
                # Calcular consumo de energía para esta arista
                energia_requerida = peso * 1.2
                
                # Verificar si hay suficiente energía
                energia_actual = energia_restante[actual]
                if energia_requerida > energia_actual:
                    continue  # No hay suficiente energía
                
                # Calcular nueva energía después de moverse
                nueva_energia = energia_actual - energia_requerida
                
                # Recargar si es un nodo de recarga
                if vecino in nodos_recarga:
                    nueva_energia = min(nueva_energia + 50, energia_inicial)
                
                # Calcular nueva distancia acumulada
                nueva_distancia = distancias[actual] + peso
                
                # Si encontramos un camino mejor (menor distancia)
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = actual
                    energia_restante[vecino] = nueva_energia
        
        # Reconstruir la ruta si existe
        if fin not in predecesores or predecesores[fin] is None:
            return None  # No hay ruta factible
            
        ruta = [fin]
        while ruta[0] != inicio:
            ruta.insert(0, predecesores[ruta[0]])
            
        return ruta
    
    def calcular_costo_ruta(self, ruta):
        """
        Calcula el costo total de una ruta sumando los pesos de sus aristas.
        
        Args:
            ruta: Lista de nodos que forman la ruta
            
        Returns:
            Costo total de la ruta
        """
        total = 0
        for i in range(len(ruta)-1):
            peso = self.grafo.obtener_peso_arista(ruta[i], ruta[i+1])
            if peso:
                total += peso
        return total
    
    def calcular_energia_necesaria(self, ruta):
        """
        Calcula la energía necesaria para completar una ruta.
        
        Args:
            ruta: Lista de nodos que forman la ruta
            
        Returns:
            Energía total requerida
        """
        if not ruta or len(ruta) < 2:
            return 0
            
        energia_total = 0
        for i in range(len(ruta) - 1):
            peso = self.grafo.obtener_peso_arista(ruta[i], ruta[i+1])
            if peso:
                energia_total += peso * 1.2  # Factor de consumo de energía
        
        return energia_total
    
    def es_ruta_factible(self, ruta, energia_inicial=100):
        """
        Verifica si una ruta es factible con la energía disponible.
        
        Args:
            ruta: Lista de nodos que forman la ruta
            energia_inicial: Energía con la que parte el drone
            
        Returns:
            True si la ruta es factible, False en caso contrario
        """
        if not ruta or len(ruta) < 2:
            return True
            
        energia_restante = energia_inicial
        nodos_recarga = [v.id for v in self.grafo.vertices.values() if v.rol == 'recarga']
        
        for i in range(len(ruta) - 1):
            peso = self.grafo.obtener_peso_arista(ruta[i], ruta[i+1])
            if not peso:
                return False  # No hay conexión directa
                
            energia_necesaria = peso * 1.2
            if energia_necesaria > energia_restante:
                return False  # No hay suficiente energía
                
            energia_restante -= energia_necesaria
            
            # Recargar si llegamos a un nodo de recarga
            if ruta[i+1] in nodos_recarga:
                energia_restante = min(energia_restante + 50, energia_inicial)  # Recarga parcial

        return True
    
    def obtener_rutas_mas_usadas(self, n=5):
        """
        Obtiene las rutas más utilizadas en la simulación.
        
        Args:
            n: Número de rutas top a retornar
            
        Returns:
            Lista de tuplas ((origen, destino), ruta) ordenadas por uso
        """
        todas_rutas = []
        for clave in self.seguimiento_rutas.recorrido_inorden():
            rutas = self.seguimiento_rutas.obtener(clave)
            for ruta in rutas:
                todas_rutas.append((clave, ruta))
        
        # Ordenar por contador de uso y tomar las n primeras
        return sorted(todas_rutas, key=lambda x: x[1].contador_uso, reverse=True)[:n]
    
    def procesar_pedido_con_prioridad(self, origen, destino, prioridad=1, algoritmo='BFS'):
        """
        Procesa un pedido con nivel de prioridad.
        
        Args:
            origen: ID del nodo de origen
            destino: ID del nodo de destino
            prioridad: Nivel de prioridad (1: normal, 2: alta, 3: urgente)
            algoritmo: Algoritmo de búsqueda a utilizar
            
        Returns:
            Objeto Pedido creado o None si no se pudo encontrar ruta
        """
        # Similar a procesar_pedido pero con prioridad
        ruta = self.encontrar_ruta(origen, destino, algoritmo)
        
        if ruta:
            costo = self.calcular_costo_ruta(ruta)
            objeto_ruta = Ruta(ruta, costo, prioridad)
            
            # Registrar en el AVL
            clave = (origen, destino)
            if self.seguimiento_rutas.contiene(clave):
                existente = self.seguimiento_rutas.obtener(clave)
                existente.append(objeto_ruta)
            else:
                self.seguimiento_rutas.insertar(clave, [objeto_ruta])
            
            # Actualizar estadísticas
            self.estadisticas_nodos[origen]['como_origen'] += 1
            self.estadisticas_nodos[destino]['como_destino'] += 1
            
            # Crear pedido con prioridad especificada
            pedido = Pedido(len(self.pedidos), origen, destino, objeto_ruta, prioridad)
            self.pedidos.append(pedido)
            return pedido
        return None