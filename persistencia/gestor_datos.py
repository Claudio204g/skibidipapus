import json
import os

class GestorDatos:
    def __init__(self, directorio_datos="datos"):
        self.directorio = directorio_datos
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)
    
    def guardar_grafo(self, grafo, nombre_archivo="grafo.json"):
        ruta = os.path.join(self.directorio, nombre_archivo)
        datos = {
            "vertices": {},
            "aristas": {}
        }
        
        # Guardar vértices
        for id_vertice, vertice in grafo.vertices.items():
            datos["vertices"][id_vertice] = {
                "rol": vertice.rol
            }
        
        # Guardar aristas
        for id_arista, arista in grafo.aristas.items():
            datos["aristas"][id_arista] = {
                "desde": arista.desde_vertice,
                "hasta": arista.hasta_vertice,
                "peso": arista.peso
            }
        
        with open(ruta, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
    
    def cargar_grafo(self, nombre_archivo="grafo.json"):
        from modelo.grafos import Grafo
        
        ruta = os.path.join(self.directorio, nombre_archivo)
        if not os.path.exists(ruta):
            return None
        
        with open(ruta, 'r') as archivo:
            datos = json.load(archivo)
        
        grafo = Grafo()
        
        # Cargar vértices
        for id_vertice, info in datos["vertices"].items():
            grafo.agregar_vertice(id_vertice, info["rol"])
        
        # Cargar aristas
        for id_arista, info in datos["aristas"].items():
            grafo.agregar_arista(info["desde"], info["hasta"], info["peso"])
        
        return grafo
    
    def guardar_simulacion(self, simulacion, nombre_archivo="simulacion.json"):
        ruta = os.path.join(self.directorio, nombre_archivo)
        datos = {
            "pedidos": [],
            "estadisticas": {}
        }
        
        # Guardar pedidos simplificados
        for pedido in simulacion.pedidos:
            if isinstance(pedido, tuple):  # Si es solo una tupla (origen, destino)
                datos["pedidos"].append({
                    "origen": pedido[0],
                    "destino": pedido[1]
                })
            else:  # Si es un objeto Pedido completo
                datos["pedidos"].append({
                    "id": pedido.id,
                    "origen": pedido.origen,
                    "destino": pedido.destino,
                    "estado": pedido.estado,
                    "prioridad": pedido.prioridad
                })
        
        # Guardar estadísticas
        datos["estadisticas"] = dict(simulacion.estadisticas_nodos)
        
        with open(ruta, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
        
        # Guardar el grafo asociado
        if simulacion.grafo:
            self.guardar_grafo(simulacion.grafo)
