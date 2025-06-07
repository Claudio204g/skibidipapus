from arbol_avl import ArbolAVL
from pedido import Pedido
from ruta import Ruta
from collections import defaultdict
import random

class Simulacion:
    def __init__(self):
        self.grafo = None
        self.seguimiento_rutas = ArbolAVL()
        self.pedidos = []
        self.estadisticas_nodos = defaultdict(lambda: {'como_origen': 0, 'como_destino': 0})
    
    def generar_pedidos_aleatorios(self, n_pedidos):
        """Genera pedidos aleatorios"""
        nodos_almacen = [v.id for v in self.grafo.vertices.values() if v.rol == 'almacen']
        nodos_cliente = [v.id for v in self.grafo.vertices.values() if v.rol == 'cliente']
        
        if not nodos_almacen or not nodos_cliente:
            return []
        
        return [(random.choice(nodos_almacen), random.choice(nodos_cliente)) for _ in range(n_pedidos)]
    
    def procesar_pedido(self, origen, destino, algoritmo='BFS'):
        """Procesa un pedido y registra la ruta"""
        ruta = self.encontrar_ruta(origen, destino, algoritmo)
        
        if ruta:
            costo = self.calcular_costo_ruta(ruta)
            objeto_ruta = Ruta(ruta, costo)
            
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
            
            # Crear y devolver pedido
            pedido = Pedido(len(self.pedidos), origen, destino, objeto_ruta)
            self.pedidos.append(pedido)
            return pedido
        return None
    
    def encontrar_ruta(self, inicio, fin, algoritmo='BFS'):
        """Encuentra ruta usando el algoritmo especificado"""
        if algoritmo == 'BFS':
            return self.ruta_bfs(inicio, fin)
        elif algoritmo == 'DFS':
            return self.ruta_dfs(inicio, fin)
        else:
            return None
    
    def ruta_bfs(self, inicio, fin):
        """Implementación de BFS para encontrar ruta"""
        # Implementación real iría aquí
        pass
    
    def calcular_costo_ruta(self, ruta):
        """Calcula el costo total de una ruta"""
        total = 0
        for i in range(len(ruta)-1):
            peso = self.grafo.obtener_peso_arista(ruta[i], ruta[i+1])
            if peso:
                total += peso
        return total
    
    def obtener_rutas_mas_usadas(self, n=5):
        """Obtiene las rutas más utilizadas"""
        todas_rutas = []
        for clave in self.seguimiento_rutas.recorrido_inorden():
            rutas = self.seguimiento_rutas.obtener(clave)
            for ruta in rutas:
                todas_rutas.append((clave, ruta))
        
        return sorted(todas_rutas, key=lambda x: x[1].contador_uso, reverse=True)[:n]