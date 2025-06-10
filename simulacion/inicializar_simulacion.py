import random
from modelo.graph import Graph
from modelo.vertex import Vertex
from modelo.edge import Edge

def generar_grafo_conexo(n_nodos, n_aristas):
    """
    Genera un grafo conexo aleatorio con pesos en las aristas.
    
    Args:
        n_nodos: Número de nodos que tendrá el grafo
        n_aristas: Número total de aristas deseadas
        
    Returns:
        Un objeto Graph que representa una red conexa aleatoria
    """
    grafo = Graph()
    
    # Añadir todos los nodos al grafo
    vertices = []
    for i in range(n_nodos):
        vertices.append(grafo.insert_vertex(i))
    
    # Crear un árbol de expansión mínima para garantizar que el grafo sea conexo
    # Primero mezclamos los nodos para tener conexiones aleatorias
    indices = list(range(n_nodos))
    random.shuffle(indices)
    
    # Conectamos cada nodo con al menos uno anterior para asegurar conexión
    for i in range(1, n_nodos):
        peso = random.randint(1, 10)  # Peso aleatorio entre 1 y 10
        grafo.insert_edge(vertices[indices[i-1]], vertices[indices[i]], peso)
    
    # Añadir aristas adicionales hasta alcanzar n_aristas
    # El árbol ya tiene n_nodos-1 aristas, así que añadimos las restantes
    aristas_actuales = n_nodos - 1
    while aristas_actuales < n_aristas:
        u_idx = random.randint(0, n_nodos-1)  # Índice origen aleatorio
        v_idx = random.randint(0, n_nodos-1)  # Índice destino aleatorio
        if u_idx != v_idx:
            u = vertices[u_idx]
            v = vertices[v_idx]
            # Verificar si ya existe una arista entre estos vértices
            if grafo.get_edge(u, v) is None:
                peso = random.randint(1, 10)
                grafo.insert_edge(u, v, peso)
                aristas_actuales += 1
    
    return grafo

def asignar_roles_nodos(grafo, porcentaje_almacen=0.2, porcentaje_recarga=0.2):
    """
    Asigna roles a los nodos del grafo (almacén, recarga o cliente).
    
    Args:
        grafo: El grafo cuyos nodos se van a etiquetar
        porcentaje_almacen: Porcentaje de nodos que serán almacenes (0.0-1.0)
        porcentaje_recarga: Porcentaje de nodos que serán estaciones de recarga (0.0-1.0)
        
    Returns:
        El mismo grafo con los roles asignados a cada nodo
    """
    vertices = list(grafo.vertices())
    random.shuffle(vertices)  # Mezclar para asignar roles aleatoriamente
    
    # Calcular cuántos nodos de cada tipo habrá
    n_almacenes = int(len(vertices) * porcentaje_almacen)
    n_recargas = int(len(vertices) * porcentaje_recarga)
    
    # Asignar roles a los nodos
    for i, vertex in enumerate(vertices):
        if i < n_almacenes:
            vertex.rol = 'almacen'  # Primeros nodos como almacenes
        elif i < n_almacenes + n_recargas:
            vertex.rol = 'recarga'  # Siguientes como estaciones de recarga
        else:
            vertex.rol = 'cliente'  # El resto como clientes
    
    return grafo