import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict
from grafos import Grafo
from vertice import Vertice
from arista import Arista
from simulacion import Simulacion
from inicializar_simulacion import generar_grafo_conexo, asignar_roles_nodos

# Configuración de la página
st.set_page_config(layout="wide", page_title="Drone Delivery Simulation")

# Título principal
st.title("🚁 Sistema de Entrega con Drones")

# Función para visualizar el grafo
def visualizar_grafo(grafo):
    """Convierte nuestro grafo a NetworkX y lo visualiza"""
    G = nx.Graph()
    
    # Añadir nodos
    for id_vertice, vertice in grafo.vertices.items():
        G.add_node(id_vertice, rol=vertice.rol)
    
    # Añadir aristas
    for arista in grafo.aristas.values():
        G.add_edge(arista.desde_vertice, arista.hasta_vertice, weight=arista.peso)
    
    # Configurar visualización
    pos = nx.spring_layout(G)
    color_map = []
    
    for node in G.nodes():
        rol = G.nodes[node]['rol']
        color_map.append('red' if rol == 'almacen' else 'green' if rol == 'recarga' else 'blue')
    
    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw(G, pos, node_color=color_map, with_labels=True, ax=ax)
    
    # Leyenda
    ax.scatter([], [], c='red', label='Almacén')
    ax.scatter([], [], c='green', label='Recarga')
    ax.scatter([], [], c='blue', label='Cliente')
    ax.legend()
    
    return fig

# Pestaña de Simulación
def pestaña_simulacion():
    st.header("🔄 Ejecutar Simulación")
    
    # Controles deslizantes
    col1, col2, col3 = st.columns(3)
    with col1:
        n_nodos = st.slider("Número de nodos", 10, 150, 15)
    with col2:
        min_aristas = max(n_nodos-1, 10)
        n_aristas = st.slider("Número de aristas", min_aristas, 300, min(min_aristas+5, 300))
    with col3:
        n_pedidos = st.slider("Número de pedidos", 10, 500, 10)
    
    # Información de distribución
    n_almacenes = int(n_nodos * 0.2)
    n_recargas = int(n_nodos * 0.2)
    n_clientes = n_nodos - n_almacenes - n_recargas
    
    st.info(f"""
    **Distribución de nodos:**
    - 📦 Almacenes: {n_almacenes} (20%)
    - 🔋 Estaciones de recarga: {n_recargas} (20%)
    - 👤 Clientes: {n_clientes} (60%)
    """)
    
    if st.button("🚀 Iniciar Simulación", type="primary"):
        with st.spinner('Generando grafo y simulando entregas...'):
            # Generar grafo
            grafo = generar_grafo_conexo(n_nodos, n_aristas)
            grafo = asignar_roles_nodos(grafo)
            
            # Inicializar simulación
            if 'simulacion' not in st.session_state:
                st.session_state.simulacion = Simulacion()
            
            st.session_state.simulacion.grafo = grafo
            st.session_state.simulacion.pedidos = st.session_state.simulacion.generar_pedidos_aleatorios(n_pedidos)
            
            # Procesar pedidos
            for origen, destino in st.session_state.simulacion.pedidos:
                st.session_state.simulacion.procesar_pedido(origen, destino)
            
            # Mostrar resultados
            st.success("¡Simulación completada con éxito!")
            st.session_state.grafo_generado = True
            
            # Visualizar grafo
            fig = visualizar_grafo(grafo)
            st.pyplot(fig)

# Pestaña de Exploración
def pestaña_exploracion():
    st.header("🌍 Explorar Red")
    
    if 'simulacion' not in st.session_state or not hasattr(st.session_state.simulacion, 'grafo'):
        st.warning("Primero ejecuta una simulación en la pestaña 'Ejecutar Simulación'")
        return
    
    grafo = st.session_state.simulacion.grafo
    
    # Visualización del grafo
    fig = visualizar_grafo(grafo)
    st.pyplot(fig)
    
    # Selectores de nodos
    nodos = list(grafo.vertices.keys())
    roles = {n: grafo.vertices[n].rol for n in nodos}
    
    col1, col2 = st.columns(2)
    with col1:
        origen = st.selectbox("Nodo origen", nodos, format_func=lambda x: f"{x} ({roles[x]})")
    with col2:
        destino = st.selectbox("Nodo destino", nodos, format_func=lambda x: f"{x} ({roles[x]})")
    
    algoritmo = st.radio("Algoritmo de búsqueda", ["BFS", "DFS"], horizontal=True)
    
    if st.button("🛩️ Calcular Ruta"):
        ruta = st.session_state.simulacion.encontrar_ruta(origen, destino, algoritmo)
        
        if ruta:
            costo = st.session_state.simulacion.calcular_costo_ruta(ruta)
            st.success(f"Ruta encontrada: {' → '.join(map(str, ruta))}")
            st.info(f"Costo total: {costo} unidades de energía")
            
            if st.button("✅ Registrar Entrega", type="primary"):
                pedido = st.session_state.simulacion.procesar_pedido(origen, destino)
                st.session_state.simulacion.pedidos.append((origen, destino))
                st.balloons()
                st.success("¡Entrega registrada exitosamente!")
        else:
            st.error("No se encontró una ruta válida que cumpla con los requisitos de energía")

# Pestaña de Estadísticas
def pestaña_estadisticas():
    st.header("📊 Estadísticas")
    
    if 'simulacion' not in st.session_state:
        st.warning("Primero ejecuta una simulación")
        return
    
    sim = st.session_state.simulacion
    
    st.subheader("Rutas más utilizadas")
    rutas_populares = sim.obtener_rutas_mas_usadas(5)
    
    if rutas_populares:
        for i, ((origen, destino), ruta) in enumerate(rutas_populares, 1):
            st.write(f"{i}. {origen} → {destino}: Usada {ruta.contador_uso} veces")
    else:
        st.write("No hay rutas registradas aún")
    
    st.subheader("Nodos más activos")
    origenes = sorted(
        [(n, stats['como_origen']) for n, stats in sim.estadisticas_nodos.items()],
        key=lambda x: x[1], reverse=True
    )
    destinos = sorted(
        [(n, stats['como_destino']) for n, stats in sim.estadisticas_nodos.items()],
        key=lambda x: x[1], reverse=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Principales orígenes**")
        for nodo, count in origenes[:5]:
            st.write(f"- Nodo {nodo}: {count} pedidos")
    with col2:
        st.write("**Principales destinos**")
        for nodo, count in destinos[:5]:
            st.write(f"- Nodo {nodo}: {count} entregas")

# Pestaña de Comparación
def pestaña_comparacion():
    st.header("⚖️ Comparación de Algoritmos")
    
    if 'simulacion' not in st.session_state:
        st.warning("Primero ejecuta una simulación")
        return
    
    grafo = st.session_state.simulacion.grafo
    nodos = list(grafo.vertices.keys())
    roles = {n: grafo.vertices[n].rol for n in nodos}
    
    col1, col2 = st.columns(2)
    with col1:
        origen = st.selectbox("Origen", nodos, key='comp_origen', format_func=lambda x: f"{x} ({roles[x]})")
    with col2:
        destino = st.selectbox("Destino", nodos, key='comp_destino', format_func=lambda x: f"{x} ({roles[x]})")
    
    if st.button("🔍 Comparar"):
        resultados = []
        algoritmos = ["BFS", "DFS"]
        
        for algo in algoritmos:
            with st.spinner(f'Probando {algo}...'):
                ruta = st.session_state.simulacion.encontrar_ruta(origen, destino, algo)
                if ruta:
                    costo = st.session_state.simulacion.calcular_costo_ruta(ruta)
                    resultados.append({
                        "Algoritmo": algo,
                        "Ruta": " → ".join(map(str, ruta)),
                        "Longitud": len(ruta),
                        "Costo": costo
                    })
        
        if resultados:
            st.table(resultados)
        else:
            st.warning("Ningún algoritmo encontró una ruta válida")

# Configuración de navegación
def main():
    st.sidebar.title("Navegación")
    paginas = {
        "Ejecutar Simulación": pestaña_simulacion,
        "Explorar Red": pestaña_exploracion,
        "Estadísticas": pestaña_estadisticas,
        "Comparar Algoritmos": pestaña_comparacion
    }
    
    seleccion = st.sidebar.radio("Ir a", list(paginas.keys()))
    paginas[seleccion]()

if __name__ == "__main__":
    main()