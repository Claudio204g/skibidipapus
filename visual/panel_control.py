import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict
from modelo.graph import Graph
from modelo.vertex import Vertex
from modelo.edge import Edge
from simulacion.simulacion import Simulacion
from simulacion.inicializar_simulacion import generar_grafo_conexo, asignar_roles_nodos

# Configuración de la página de Streamlit
st.set_page_config(layout="wide", page_title="Simulación de Entrega con Drones")

# Título principal de la aplicación
st.title("🚁 Sistema de Entrega con Drones")

# Función para visualizar el grafo
def visualizar_grafo(grafo):
    """
    Convierte nuestro grafo a NetworkX y lo visualiza con matplotlib.
    
    Args:
        grafo: Objeto Graph a visualizar
        
    Returns:
        Figura de matplotlib con el grafo visualizado
    """
    G = nx.Graph()
    
    # Añadir nodos al grafo de NetworkX
    for vertice in grafo.vertices():
        G.add_node(vertice.element(), rol=vertice.rol)
    
    # Añadir aristas con sus pesos
    for edge in grafo.edges():
        origen, destino = edge.endpoints()
        G.add_edge(origen.element(), destino.element(), weight=edge.element())
    
    # Configurar visualización
    pos = nx.spring_layout(G)  # Algoritmo de posicionamiento de nodos
    color_map = []
    
    # Asignar colores según el rol de cada nodo
    for node in G.nodes():
        rol = G.nodes[node]['rol']
        color_map.append('red' if rol == 'almacen' else 'green' if rol == 'recarga' else 'blue')
    
    # Crear figura y dibujar el grafo
    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw(G, pos, node_color=color_map, with_labels=True, ax=ax)
    
    # Añadir leyenda para tipos de nodos
    ax.scatter([], [], c='red', label='Almacén')
    ax.scatter([], [], c='green', label='Recarga')
    ax.scatter([], [], c='blue', label='Cliente')
    ax.legend()
    
    return fig

# Pestaña de Simulación
def pestaña_simulacion():
    """
    Pestaña para configurar y ejecutar la simulación.
    Permite generar un grafo aleatorio y simular pedidos.
    """
    st.header("🔄 Ejecutar Simulación")
    
    # Controles deslizantes para configurar la simulación
    col1, col2, col3 = st.columns(3)
    with col1:
        n_nodos = st.slider("Número de nodos", 10, 150, 15)
    with col2:
        min_aristas = max(n_nodos-1, 10)  # Mínimo para garantizar conexión
        n_aristas = st.slider("Número de aristas", min_aristas, 300, min(min_aristas+5, 300))
    with col3:
        n_pedidos = st.slider("Número de pedidos", 10, 500, 10)
    
    # Mostrar información sobre la distribución de nodos
    n_almacenes = int(n_nodos * 0.2)
    n_recargas = int(n_nodos * 0.2)
    n_clientes = n_nodos - n_almacenes - n_recargas
    
    st.info(f"""
    **Distribución de nodos:**
    - 📦 Almacenes: {n_almacenes} (20%)
    - 🔋 Estaciones de recarga: {n_recargas} (20%)
    - 👤 Clientes: {n_clientes} (60%)
    """)
    
    # Botón para iniciar la simulación
    if st.button("🚀 Iniciar Simulación", type="primary"):
        with st.spinner('Generando grafo y simulando entregas...'):
            # Generar grafo aleatorio
            grafo = generar_grafo_conexo(n_nodos, n_aristas)
            grafo = asignar_roles_nodos(grafo)
            
            # Inicializar o reiniciar la simulación
            if 'simulacion' not in st.session_state:
                st.session_state.simulacion = Simulacion()
            
            st.session_state.simulacion.grafo = grafo
            
            # Generar pedidos aleatorios como tuplas (origen, destino)
            pedidos_tuples = st.session_state.simulacion.generar_pedidos_aleatorios(n_pedidos)
            
            # Procesar cada pedido y guardar los objetos Pedido resultantes
            st.session_state.simulacion.pedidos = []  # Reiniciar la lista de pedidos
            for origen, destino in pedidos_tuples:
                pedido = st.session_state.simulacion.procesar_pedido(origen, destino)
                if pedido:  # Solo añadir si se creó exitosamente
                    st.session_state.simulacion.pedidos.append(pedido)
            
            # Mostrar resultados
            st.success("¡Simulación completada con éxito!")
            st.session_state.grafo_generado = True
            
            # Visualizar el grafo generado
            fig = visualizar_grafo(grafo)
            st.pyplot(fig)

# Pestaña de Exploración
def pestaña_exploracion():
    """
    Pestaña para explorar el grafo y probar rutas entre nodos.
    Permite calcular y visualizar rutas usando diferentes algoritmos.
    """
    st.header("🌍 Explorar Red")
    
    # Verificar que exista una simulación
    if 'simulacion' not in st.session_state or not hasattr(st.session_state.simulacion, 'grafo'):
        st.warning("Primero ejecuta una simulación en la pestaña 'Ejecutar Simulación'")
        return
    
    grafo = st.session_state.simulacion.grafo
    
    # Visualizar el grafo actual
    fig = visualizar_grafo(grafo)
    st.pyplot(fig)
    
    # Recopilar información de los nodos para los selectores
    nodos_ids = [v.element() for v in grafo.vertices()]
    nodos_por_rol = {
        'almacen': [v.element() for v in grafo.vertices() if v.rol == 'almacen'],
        'cliente': [v.element() for v in grafo.vertices() if v.rol == 'cliente'],
        'recarga': [v.element() for v in grafo.vertices() if v.rol == 'recarga']
    }
    
    # Selectores para elegir nodos origen y destino
    col1, col2 = st.columns(2)
    with col1:
        origen = st.selectbox(
            "Nodo origen", 
            nodos_ids, 
            format_func=lambda x: f"{x} ({'almacen' if x in nodos_por_rol['almacen'] else 'recarga' if x in nodos_por_rol['recarga'] else 'cliente'})"
        )
    with col2:
        destino = st.selectbox(
            "Nodo destino", 
            nodos_ids, 
            format_func=lambda x: f"{x} ({'almacen' if x in nodos_por_rol['almacen'] else 'recarga' if x in nodos_por_rol['recarga'] else 'cliente'})"
        )
    
    # Selector de algoritmo de ruta
    algoritmo = st.radio("Algoritmo de búsqueda", ["BFS", "DFS", "Dijkstra"], horizontal=True)
    
    # Botón para calcular ruta
    if st.button("🛩️ Calcular Ruta"):
        ruta = st.session_state.simulacion.encontrar_ruta(origen, destino, algoritmo)
        
        if ruta:
            # Mostrar información de la ruta encontrada
            costo = st.session_state.simulacion.calcular_costo_ruta(ruta)
            st.success(f"Ruta encontrada: {' → '.join(map(str, ruta))}")
            st.info(f"Costo total: {costo} unidades de energía")
            
            # Opción para registrar la entrega
            if st.button("✅ Registrar Entrega", type="primary"):
                pedido = st.session_state.simulacion.procesar_pedido(origen, destino)
                if pedido:
                    st.session_state.simulacion.pedidos.append(pedido)
                    st.balloons()
                    st.success("¡Entrega registrada exitosamente!")
                else:
                    st.error("No se pudo registrar la entrega")
        else:
            st.error("No se encontró una ruta válida que cumpla con los requisitos de energía")

# Pestaña de Estadísticas
def pestaña_estadisticas():
    """
    Pestaña para mostrar estadísticas de la simulación.
    Muestra rutas más utilizadas y nodos más activos.
    """
    st.header("📊 Estadísticas")
    
    # Verificar que exista una simulación
    if 'simulacion' not in st.session_state:
        st.warning("Primero ejecuta una simulación")
        return
    
    sim = st.session_state.simulacion
    
    # Mostrar rutas más utilizadas
    st.subheader("Rutas más utilizadas")
    rutas_populares = sim.obtener_rutas_mas_usadas(5)
    
    if rutas_populares:
        for i, ((origen, destino), ruta) in enumerate(rutas_populares, 1):
            st.write(f"{i}. {origen} → {destino}: Usada {ruta.contador_uso} veces")
    else:
        st.write("No hay rutas registradas aún")
    
    # Mostrar nodos más activos
    st.subheader("Nodos más activos")
    origenes = sorted(
        [(n, stats['como_origen']) for n, stats in sim.estadisticas_nodos.items()],
        key=lambda x: x[1], reverse=True
    )
    destinos = sorted(
        [(n, stats['como_destino']) for n, stats in sim.estadisticas_nodos.items()],
        key=lambda x: x[1], reverse=True
    )
    
    # Mostrar en dos columnas
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
    """
    Pestaña para comparar diferentes algoritmos de ruta.
    Permite ver las diferencias entre BFS, DFS y Dijkstra.
    """
    st.header("⚖️ Comparación de Algoritmos")
    
    # Verificar que exista una simulación
    if 'simulacion' not in st.session_state:
        st.warning("Primero ejecuta una simulación")
        return
    
    grafo = st.session_state.simulacion.grafo
    
    # Recopilar información de los nodos para los selectores
    nodos_ids = [v.element() for v in grafo.vertices()]
    nodos_por_rol = {
        'almacen': [v.element() for v in grafo.vertices() if v.rol == 'almacen'],
        'cliente': [v.element() for v in grafo.vertices() if v.rol == 'cliente'],
        'recarga': [v.element() for v in grafo.vertices() if v.rol == 'recarga']
    }
    
    # Selectores de nodos origen y destino
    col1, col2 = st.columns(2)
    with col1:
        origen = st.selectbox(
            "Origen", 
            nodos_ids, 
            key='comp_origen',
            format_func=lambda x: f"{x} ({'almacen' if x in nodos_por_rol['almacen'] else 'recarga' if x in nodos_por_rol['recarga'] else 'cliente'})"
        )
    with col2:
        destino = st.selectbox(
            "Destino", 
            nodos_ids, 
            key='comp_destino',
            format_func=lambda x: f"{x} ({'almacen' if x in nodos_por_rol['almacen'] else 'recarga' if x in nodos_por_rol['recarga'] else 'cliente'})"
        )
    
    # Botón para comparar algoritmos
    if st.button("🔍 Comparar"):
        resultados = []
        algoritmos = ["BFS", "DFS", "Dijkstra"]
        
        # Probar cada algoritmo
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
        
        # Mostrar resultados en una tabla
        if resultados:
            st.table(resultados)
        else:
            st.warning("Ningún algoritmo encontró una ruta válida")

# Pestaña de Configuración
def pestaña_configuracion():
    """
    Pestaña para configurar parámetros del sistema y gestionar
    la persistencia de datos.
    """
    st.header("⚙️ Configuración del Sistema")
    
    # Opciones de energía
    st.subheader("Configuración de Energía")
    energia_inicial = st.slider("Energía inicial de los drones", 50, 200, 100)
    recarga_estacion = st.slider("Energía obtenida en estaciones de recarga", 10, 100, 50)
    
    # Funcionalidad de guardar/cargar simulación
    st.subheader("Persistencia de Datos")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre_archivo = st.text_input("Nombre del archivo", "simulacion_1")
        if st.button("💾 Guardar Simulación"):
            if 'simulacion' in st.session_state:
                from persistencia.gestor_datos import GestorDatos
                gestor = GestorDatos()
                gestor.guardar_simulacion(st.session_state.simulacion, f"{nombre_archivo}.json")
                st.success("Simulación guardada correctamente")
            else:
                st.warning("No hay simulación para guardar")
    
    with col2:
        # En una implementación real, se listarían los archivos existentes
        archivos_disponibles = ["simulacion_1.json", "simulacion_2.json"]
        archivo_seleccionado = st.selectbox("Seleccionar archivo", archivos_disponibles)
        if st.button("📂 Cargar Simulación"):
            from persistencia.gestor_datos import GestorDatos
            gestor = GestorDatos()
            grafo = gestor.cargar_grafo()
            if grafo:
                # Aquí cargaríamos la simulación completa
                st.success("Simulación cargada correctamente")
                st.session_state.grafo_generado = True
                
                # En una implementación real, cargaríamos todos los datos de la simulación
            else:
                st.error("No se pudo cargar la simulación")

# Configuración de navegación de la interfaz
def main():
    """
    Función principal que configura la navegación entre pestañas
    y ejecuta la interfaz de usuario.
    """
    st.sidebar.title("Navegación")
    paginas = {
        "Ejecutar Simulación": pestaña_simulacion,
        "Explorar Red": pestaña_exploracion,
        "Estadísticas": pestaña_estadisticas,
        "Comparar Algoritmos": pestaña_comparacion,
        "Configuración": pestaña_configuracion
    }
    
    # Radio button para seleccionar la pestaña
    seleccion = st.sidebar.radio("Ir a", list(paginas.keys()))
    paginas[seleccion]()  # Ejecutar la función de la pestaña seleccionada

if __name__ == "__main__":
    main()