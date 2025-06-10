# Manual de Usuario - Sistema de Entrega con Drones

## Introducción
Este sistema simula una red de entrega utilizando drones, permitiendo planificar y optimizar rutas considerando limitaciones de energía y ubicaciones estratégicas. Está diseñado para estudiar algoritmos de grafos y optimización de rutas en un entorno práctico.

## Funcionalidades

### Simulación de Red
- **Generar Red**: Cree una red aleatoria especificando el número de nodos y aristas. El sistema asigna automáticamente roles (almacén, estación de recarga, cliente) a los nodos.
- **Visualizar Grafo**: Observe la red generada con colores que distinguen los diferentes tipos de nodos (rojo para almacenes, verde para estaciones de recarga, azul para clientes).

### Cálculo de Rutas
- **Buscar Rutas**: Seleccione nodos de origen y destino para calcular la mejor ruta considerando la energía disponible.
- **Comparar Algoritmos**: Compare diferentes algoritmos (BFS, DFS, Dijkstra) para encontrar rutas entre dos nodos y analice sus diferencias.
- **Gestión de Energía**: El sistema considera la energía de los drones y las paradas de recarga necesarias durante una ruta.

### Análisis de Datos
- **Estadísticas**: Visualice las rutas más utilizadas y los nodos con mayor actividad en la red.
- **Comparativa de Algoritmos**: Compare el rendimiento de distintos algoritmos de búsqueda de rutas.

## Uso del Panel de Control

1. **Ejecutar Simulación**:
   - Ajuste los parámetros (nodos, aristas, pedidos) usando los deslizadores
   - Haga clic en "Iniciar Simulación" para generar la red y pedidos aleatorios
   - Visualice el grafo generado con sus componentes

2. **Explorar Red**:
   - Seleccione nodos de origen y destino
   - Elija el algoritmo de búsqueda
   - Calcule la ruta y visualice el costo energético
   - Opcionalmente, registre la entrega

3. **Visualizar Estadísticas**:
   - Consulte las rutas más frecuentes
   - Identifique los nodos más activos como origen y destino

4. **Comparar Algoritmos**:
   - Seleccione origen y destino
   - Compare los resultados de BFS, DFS y Dijkstra en una tabla

## Preguntas Frecuentes

- **¿Cómo afecta la energía a las rutas?**
  - El sistema calcula el consumo energético basado en el peso de las aristas. Los drones necesitan suficiente energía para completar cada tramo, y pueden recargar en estaciones designadas.

- **¿Qué significan los colores de los nodos?**
  - Rojo: Almacenes (puntos de origen de entregas)
  - Verde: Estaciones de recarga (donde los drones pueden recuperar energía)
  - Azul: Clientes (destinos de entrega)

- **¿Cómo se calcula la ruta óptima?**
  - Por defecto, se utiliza el algoritmo de Dijkstra para encontrar la ruta de menor costo considerando las restricciones de energía. BFS encuentra la ruta con menos nodos, mientras que DFS puede explorar rutas alternativas.

- **¿Puedo guardar mis simulaciones?**
  - Sí, en la pestaña de Configuración puede guardar el estado actual de la simulación y cargarlo posteriormente.

- **¿Qué ocurre si un drone se queda sin energía?**
  - El sistema marcará la ruta como no factible. Para rutas válidas, se asegura que siempre haya suficiente energía o estaciones de recarga accesibles.
