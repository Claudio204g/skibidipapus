import random
from modelo.grafos import Grafo

def generar_grafo_conexo(n_nodos, n_aristas):
    """
    Genera un grafo conexo aleatorio con pesos en las aristas.
    
    Args:
        n_nodos: Número de nodos que tendrá el grafo
        n_aristas: Número total de aristas deseadas
        
    Returns:
        Un objeto Grafo que representa una red conexa aleatoria
    """
    grafo = Grafo()
    
    # Añadir todos los nodos al grafo
    for i in range(n_nodos):
        grafo.agregar_vertice(i)
    
    # Crear un árbol de expansión mínima para garantizar que el grafo sea conexo
    # Primero mezclamos los nodos para tener conexiones aleatorias
    nodos = list(range(n_nodos))
    random.shuffle(nodos)
    
    # Conectamos cada nodo con al menos uno anterior para asegurar conexión
    for i in range(1, n_nodos):
        peso = random.randint(1, 10)  # Peso aleatorio entre 1 y 10
        grafo.agregar_arista(nodos[i-1], nodos[i], peso)
    
    # Añadir aristas adicionales hasta alcanzar n_aristas
    # El árbol ya tiene n_nodos-1 aristas, así que añadimos las restantes
    aristas_actuales = n_nodos - 1
    while aristas_actuales < n_aristas:
        u = random.randint(0, n_nodos-1)  # Nodo origen aleatorio
        v = random.randint(0, n_nodos-1)  # Nodo destino aleatorio
        if u != v and not grafo.obtener_peso_arista(u, v):  # Evitamos bucles y aristas duplicadas
            peso = random.randint(1, 10)
            grafo.agregar_arista(u, v, peso)
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
    nodos = list(grafo.vertices.keys())
    random.shuffle(nodos)  # Mezclar para asignar roles aleatoriamente
    
    # Calcular cuántos nodos de cada tipo habrá
    n_almacenes = int(len(nodos) * porcentaje_almacen)
    n_recargas = int(len(nodos) * porcentaje_recarga)
    
    # Asignar roles a los nodos
    for i, id_nodo in enumerate(nodos):
        if i < n_almacenes:
            grafo.vertices[id_nodo].rol = 'almacen'  # Primeros nodos como almacenes
        elif i < n_almacenes + n_recargas:
            grafo.vertices[id_nodo].rol = 'recarga'  # Siguientes como estaciones de recarga
        else:
            grafo.vertices[id_nodo].rol = 'cliente'  # El resto como clientes
    
    return grafo