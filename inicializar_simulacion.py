import random
from grafos import Grafo

def generar_grafo_conexo(n_nodos, n_aristas):
    """Genera un grafo conexo aleatorio"""
    grafo = Grafo()
    
    # Añadir todos los nodos
    for i in range(n_nodos):
        grafo.agregar_vertice(i)
    
    # Crear un árbol de expansión mínima para garantizar conexión
    nodos = list(range(n_nodos))
    random.shuffle(nodos)
    
    for i in range(1, n_nodos):
        peso = random.randint(1, 10)
        grafo.agregar_arista(nodos[i-1], nodos[i], peso)
    
    # Añadir aristas adicionales hasta alcanzar n_aristas
    aristas_actuales = n_nodos - 1
    while aristas_actuales < n_aristas:
        u = random.randint(0, n_nodos-1)
        v = random.randint(0, n_nodos-1)
        if u != v and not grafo.obtener_peso_arista(u, v):
            peso = random.randint(1, 10)
            grafo.agregar_arista(u, v, peso)
            aristas_actuales += 1
    
    return grafo

def asignar_roles_nodos(grafo, porcentaje_almacen=0.2, porcentaje_recarga=0.2):
    """Asigna roles a los nodos del grafo"""
    nodos = list(grafo.vertices.keys())
    random.shuffle(nodos)
    
    n_almacenes = int(len(nodos) * porcentaje_almacen)
    n_recargas = int(len(nodos) * porcentaje_recarga)
    
    for i, id_nodo in enumerate(nodos):
        if i < n_almacenes:
            grafo.vertices[id_nodo].rol = 'almacen'
        elif i < n_almacenes + n_recargas:
            grafo.vertices[id_nodo].rol = 'recarga'
        else:
            grafo.vertices[id_nodo].rol = 'cliente'
    
    return grafo