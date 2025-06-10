import json
import os
from modelo.graph import Graph
from modelo.vertex import Vertex
from modelo.edge import Edge

class GestorDatos:
    def __init__(self, directorio_datos="datos"):
        self.directorio = directorio_datos
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)
    
    def guardar_grafo(self, grafo, nombre_archivo="grafo.json"):
        ruta = os.path.join(self.directorio, nombre_archivo)
        datos = {
            "vertices": {},
            "aristas": []
        }
        
        # Mapeo de objetos Vertex a IDs para serialización
        vertex_to_id = {}
        
        # Guardar vértices
        for i, vertice in enumerate(grafo.vertices()):
            vertex_id = vertice.element()
            vertex_to_id[vertice] = vertex_id
            datos["vertices"][str(vertex_id)] = {
                "rol": vertice.rol
            }
        
        # Guardar aristas
        for arista in grafo.edges():
            origen, destino = arista.endpoints()
            origen_id = vertex_to_id[origen]
            destino_id = vertex_to_id[destino]
            peso = arista.element()
            
            datos["aristas"].append({
                "origen": origen_id,
                "destino": destino_id,
                "peso": peso
            })
        
        with open(ruta, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
    
    def cargar_grafo(self, nombre_archivo="grafo.json"):
        ruta = os.path.join(self.directorio, nombre_archivo)
        if not os.path.exists(ruta):
            return None
        
        with open(ruta, 'r') as archivo:
            datos = json.load(archivo)
        
        grafo = Graph()
        
        # Mapeo de IDs a objetos Vertex
        id_to_vertex = {}
        
        # Cargar vértices
        for id_vertice, info in datos["vertices"].items():
            vertex = grafo.insert_vertex(int(id_vertice) if id_vertice.isdigit() else id_vertice)
            vertex.rol = info["rol"]
            id_to_vertex[id_vertice] = vertex
        
        # Cargar aristas
        for info_arista in datos["aristas"]:
            origen_id = str(info_arista["origen"])
            destino_id = str(info_arista["destino"])
            
            if origen_id in id_to_vertex and destino_id in id_to_vertex:
                grafo.insert_edge(id_to_vertex[origen_id], id_to_vertex[destino_id], info_arista["peso"])
        
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
