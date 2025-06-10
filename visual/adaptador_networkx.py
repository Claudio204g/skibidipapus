import networkx as nx
import matplotlib.pyplot as plt

def convertir_a_networkx(grafo):
    """Convierte nuestro grafo a un objeto networkx para visualización"""
    grafo_nx = nx.Graph()
    
    for id_vertice, vertice in grafo.vertices.items():
        grafo_nx.add_node(id_vertice, rol=vertice.rol)
    
    for arista in grafo.aristas.values():
        grafo_nx.add_edge(arista.desde_vertice, arista.hasta_vertice, peso=arista.peso)
    
    return grafo_nx

def visualizar_grafo(grafo):
    """Visualiza el grafo usando matplotlib"""
    grafo_nx = convertir_a_networkx(grafo)
    posicion = nx.spring_layout(grafo_nx)
    
    mapa_colores = []
    for nodo in grafo_nx.nodes():
        rol = grafo_nx.nodes[nodo]['rol']
        if rol == 'almacen':
            mapa_colores.append('red')
        elif rol == 'recarga':
            mapa_colores.append('green')
        else:
            mapa_colores.append('blue')
    
    plt.figure(figsize=(10, 8))
    nx.draw(grafo_nx, posicion, node_color=mapa_colores, with_labels=True)
    
    # Añadir leyenda
    plt.scatter([], [], c='red', label='Almacén')
    plt.scatter([], [], c='green', label='Recarga')
    plt.scatter([], [], c='blue', label='Cliente')
    plt.legend()
    
    return plt.gcf()