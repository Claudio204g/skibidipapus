import random
from collections import deque, defaultdict
from graph import Graph
from vertex import Vertex
from edge import Edge
from datetime import datetime
from typing import List, Dict
from AVL import insert, delete_node

class RouteManager:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.charging_stations = set()

    def add_charging_station(self, vertex: Vertex):
        self.charging_stations.add(vertex)

    def _find_vertex_by_id(self, vertex_id):
        for v in self.graph.vertices():
            if v.element() == vertex_id:
                return v
        return None

    def find_route_with_recharge(self, origin_id, destination_id, battery_limit=50):
        origin = self._find_vertex_by_id(origin_id)
        destination = self._find_vertex_by_id(destination_id)
        if not origin or not destination:
            raise ValueError("Vértice de origen o destino no encontrado")
        
        queue = deque()
        queue.append((origin, [origin], 0, battery_limit, [], []))
        
        while queue:
            current, path, cost, battery, stops, segments = queue.popleft()
            
            print(f"[DEBUG] Nodo actual: {current.element()}, batería restante: {battery}, ruta: {[v.element() for v in path]}, recargas: {[v.element() for v in stops]}")
            
            if current == destination:
                print(f"[DEBUG] ¡Destino alcanzado! Ruta final: {[v.element() for v in path]}, recargas: {[v.element() for v in stops]}")
                return {
                    "path": [v.element() for v in path],
                    "total_cost": cost,
                    "battery": battery,
                    "recharge_stops": [v.element() for v in stops],
                    "segments": segments + [current.element()] if segments else [current.element()]
                }
            
            for neighbor in self.graph.neighbors(current):
                edge = self.graph.get_edge(current, neighbor)
                if not edge:
                    continue
                
                edge_cost = edge.element()
                
                # Caso 1: Batería suficiente
                if edge_cost <= battery:
                    print(f"[DEBUG] Avanzando a {neighbor.element()} (costo {edge_cost}), batería suficiente ({battery} >= {edge_cost})")
                    queue.append((
                        neighbor,
                        path + [neighbor],
                        cost + edge_cost,
                        battery - edge_cost,
                        stops,
                        segments
                    ))
                # Caso 2: Necesita recarga
                else:
                    for station in self.charging_stations:
                        if station != current and station not in path:
                            edge_to_station = self.graph.get_edge(current, station)
                            if edge_to_station and edge_to_station.element() <= battery:
                                print(f"[DEBUG] Recargando en estación {station.element()} desde {current.element()} (costo {edge_to_station.element()})")
                                queue.append((
                                    station,
                                    path + [station],
                                    cost + edge_to_station.element(),
                                    battery_limit,
                                    stops + [station],
                                    segments + [current.element()]
                                ))
        print("[DEBUG] No se encontró ruta posible.")
        return None

class RouteTracker:
    def __init__(self):
        self.route_frecuency = None
        self.node_visits = {}
        self.route_cost = {}
        self.custom_hashmap = self.create_custom_hashmap()
    
    def create_custom_hashmap(self, initial_size=10):
        class CustomHashMap:
            def __init__(self, size):
                self.size = size
                self.buckets = [[] for _ in range(size)]
                self.count = 0

            def hash(self, key):
                return hash(key) % self.size
            
            def put(self, key, value):
                index = self.hash(key)
                bucket = self.buckets[index]
                for i, (k, v) in enumerate(bucket):
                    if k == key:
                        bucket[i] = (key, value)
                        return
                bucket.append((key, value))
                self.count += 1

            def get(self, key):
                index = self.hash(key)
                bucket = self.buckets[index]
                for k, v in bucket:
                    if k == key:
                        return v
                return None

            def increment(self, key):
                index = self.hash(key)
                bucket = self.buckets[index]
                for i, (k, v) in enumerate(bucket):
                    if k == key:
                        bucket[i] = (k, v + 1)
                        return
                bucket.append((key, 1))
                self.count += 1

            def items(self):
                for bucket in self.buckets:
                    for item in bucket:
                        yield item
        return CustomHashMap(initial_size)

    def route_to_string(self, path):
        return " -> ".join(str(node) for node in path)

    def find_route_in_avl(self, node, route_str):
        if node is None:
            return None
        if node.key[1] == route_str:
            return node
        if route_str < node.key[1]:
            return self.find_route_in_avl(node.left, route_str)
        return self.find_route_in_avl(node.right, route_str)
    
    def in_order_traversal(self, node, result):
        if node is not None:
            self.in_order_traversal(node.left, result)
            result.append(node.key)
            self.in_order_traversal(node.right, result)

    def register_route(self, route_path, cost):
        route_str = self.route_to_string(route_path)
        existing_node = self.find_route_in_avl(self.route_frecuency, route_str)
        
        if existing_node:
            count, route = existing_node.key
            self.route_frecuency = delete_node(self.route_frecuency, existing_node.key)
            self.route_frecuency = insert(self.route_frecuency, (count + 1, route))
        else:
            self.route_frecuency = insert(self.route_frecuency, (1, route_str))
        
        self.route_cost[route_str] = cost

        for node in route_path:
            self.custom_hashmap.increment(node)

        for node in route_path:
            node_str = str(node)
            self.node_visits[node_str] = self.node_visits.get(node_str, 0) + 1

    def get_most_frequent_routes(self, top_n=5):
        routes = []
        self.in_order_traversal(self.route_frecuency, routes)
        routes.sort(reverse=True, key=lambda x: x[0])
        top_routes = []
        for count, route in routes[:top_n]:
            cost = self.route_cost.get(route, 0)
            top_routes.append((count, route, cost))
        return top_routes
    
    def get_node_visit_stats(self):
        stats = {}
        for node, count in self.custom_hashmap.items():
            stats[str(node)] = count
        return stats

class RouteOptimizer:
    def __init__(self, route_tracker, route_manager):
        self.tracker = route_tracker
        self.manager = route_manager
        self.optimization_report = []
        self.segment_cache = defaultdict(list)

    def add_report(self, decision):
        self.optimization_report.append({'decision': decision})

    def suggested_optimized_route(self, origin_id, destination_id, battery_limit=50):
        frequent_routes = self.tracker.get_most_frequent_routes()
        # 1. Buscar ruta histórica completa
        for count, route_str, cost in frequent_routes:
            nodes = route_str.split(" -> ")
            if nodes[0] == str(origin_id) and nodes[-1] == str(destination_id):
                self.add_report(f"Usando ruta frecuente existente: {route_str}")
                # Intentar obtener paradas de recarga reales para la ruta histórica
                recharge_info = self.manager.find_route_with_recharge(origin_id, destination_id, battery_limit)
                return {
                    'path': nodes,
                    'total_cost': cost,
                    'recharge_stops': recharge_info['recharge_stops'] if recharge_info else [],
                    'source': 'historical',
                    'confidence': min(100, count * 10)
                }
        # 2. Intentar combinar segmentos históricos
        for count1, route1, cost1 in frequent_routes:
            nodes1 = route1.split(" -> ")
            if nodes1[0] == str(origin_id):
                for count2, route2, cost2 in frequent_routes:
                    nodes2 = route2.split(" -> ")
                    if nodes1[-1] == nodes2[0] and nodes2[-1] == str(destination_id):
                        # Combinar rutas
                        combined_path = nodes1 + nodes2[1:]
                        combined_cost = cost1 + cost2
                        self.add_report(f"Combinando segmentos: {route1} + {route2}")
                        # Intentar obtener paradas de recarga para la ruta combinada
                        recharge_info = self.manager.find_route_with_recharge(origin_id, destination_id, battery_limit)
                        return {
                            'path': combined_path,
                            'total_cost': combined_cost,
                            'recharge_stops': recharge_info['recharge_stops'] if recharge_info else [],
                            'source': 'segment_combination',
                            'confidence': 70
                        }
        # 3. Calcular nueva ruta
        new_route = self.manager.find_route_with_recharge(origin_id, destination_id, battery_limit)
        if new_route:
            self.tracker.register_route(new_route['path'], new_route['total_cost'])
            self.add_report(f'Calculando nueva ruta: {" -> ".join(new_route["path"])}')
            return {
                **new_route,
                'source': 'new_calculation',
                'confidence': 50
            }
        else:
            self.add_report('No se encontró ruta posible')
            return {
                'path': [],
                'total_cost': 0,
                'recharge_stops': [],
                'source': 'no_route',
                'confidence': 0
            }
    
    def get_optimization_report(self):
        return self.optimization_report

class OrderSimulator:
    def __init__(self, graph: Graph, warehouse: List[Vertex], clients: List[Vertex]):
        self.graph = graph
        self.warehouse = warehouse
        self.clients = clients
        self.order_counter = 0
        self.route_manager = RouteManager(graph)
        self.route_tracker = RouteTracker()
        self.route_optimizer = RouteOptimizer(self.route_tracker, self.route_manager)
        self.setup_charging_stations()

    def setup_charging_stations(self):
        all_vertices = list(self.graph.vertices())
        num_stations = max(1, len(all_vertices) // 5)
        self.charging_stations = random.sample(all_vertices, num_stations)
        for station in self.charging_stations:
            self.route_manager.add_charging_station(station)
    
    def generate_random_order(self):
        origin = random.choice(self.warehouse)
        destination = random.choice(self.clients)
        battery_limit = random.randint(30, 100)
        return {
            'origin': origin,
            'destination': destination,
            'battery_limit': battery_limit,
            'timestamp': datetime.now()
        }

    def process_single_order(self, order_data: dict):
        origin_id = order_data['origin'].element()
        dest_id = order_data['destination'].element()
        battery_limit = order_data['battery_limit']
        optimized_route = self.route_optimizer.suggested_optimized_route(
            origin_id,
            dest_id,
            battery_limit
        )
        self.route_tracker.register_route(
            optimized_route['path'],
            optimized_route['total_cost']
        )
        recharge_stops = optimized_route.get('recharge_stops', [])
        return {
            'order_number': self.order_counter,
            'origin': origin_id,
            'destination': dest_id,
            'path': ' -> '.join(optimized_route['path']),
            'cost': optimized_route['total_cost'],
            'recharge_stops': recharge_stops,
            'source': optimized_route['source'],
            'battery_used': self.calculate_battery_usage(optimized_route, battery_limit),
        }

    def calculate_battery_usage(self, route_data: Dict, battery_limit: int) -> float:
        if 'recharge_stops' not in route_data or not route_data['recharge_stops']:
            if battery_limit == 0:
                return 0
            return min(100, route_data['total_cost'] / battery_limit * 100)
        max_usage = 0
        current_segment_cost = 0
        for i in range(len(route_data['path']) - 1):
            from_node = route_data['path'][i]
            to_node = route_data['path'][i + 1]
            vertex_from = self.route_manager._find_vertex_by_id(from_node)
            vertex_to = self.route_manager._find_vertex_by_id(to_node)
            edge = self.graph.get_edge(vertex_from, vertex_to)
            if edge:
                current_segment_cost += edge.element()
                if to_node in route_data.get('recharge_stops', []) or i == len(route_data['path']) - 2:
                    segment_usage = (current_segment_cost / battery_limit) * 100
                    max_usage = max(max_usage, segment_usage)
                    current_segment_cost = 0
        return min(100, max_usage)

    def process_orders(self, num_orders: int = 10):
        print("\n" + "=" * 50)
        print(f"Iniciando simulación de {num_orders} órdenes")
        print("=" * 50 + "\n")
        for _ in range(num_orders):
            self.order_counter += 1
            order_data = self.generate_random_order()
            result = self.process_single_order(order_data)
            print(f"Orden #{result['order_number']}: {result['origin']} → {result['destination']}")
            print(f"Ruta: {result['path']}")
            print(f"Costo: {result['cost']:.1f} | Batería usada: {result['battery_used']:.1f}%")
            print(f"Paradas de recarga: {len(result['recharge_stops'])} recargas ({result['recharge_stops']})")
            print(f"Tipo: {self.translate_source(result['source'])}")
            print("-" * 50)
        self.show_statistical_summary()

    def translate_source(self, source: str) -> str:
        translations = {
            'historical': "Ruta histórica óptima",
            'segment_combination': "Combinación de segmentos",
            'new_calculation': "Nueva ruta calculada",
            'no_route': "No se encontró ruta"
        }
        return translations.get(source, source)

    def show_statistical_summary(self):
        print("\n" + "=" * 50)
        print("Resumen Estadístico")
        print("=" * 50)
        total_orders = self.order_counter
        frequent_routes = self.route_tracker.get_most_frequent_routes(3)
        node_stats = self.route_tracker.get_node_visit_stats()
        print(f"\nTotal de órdenes procesadas: {total_orders}")
        print("\nRutas más frecuentes:")
        for i, (count, route, cost) in enumerate(frequent_routes, 1):
            print(f"{i}. {route} (usada {count} veces, costo promedio: {cost:.1f})")
        print("\nNodos más visitados:")
        sorted_nodes = sorted(node_stats.items(), key=lambda x: -x[1])[:5]
        for node, visits in sorted_nodes:
            print(f"- {node}: {visits} visitas")
        optimization_stats = self._calculate_optimization_stats()
        print("\nEfectividad de optimización:")
        print(f"- Rutas históricas usadas: {optimization_stats['historical']} ({optimization_stats['historical_pct']:.1f}%)")
        print(f"- Segmentos combinados: {optimization_stats['segment_combination']} ({optimization_stats['segment_pct']:.1f}%)")
        print(f"- Nuevas rutas calculadas: {optimization_stats['new_calculation']} ({optimization_stats['new_pct']:.1f}%)")

    def _calculate_optimization_stats(self) -> Dict:
        report = self.route_optimizer.get_optimization_report()
        total = len(report) if len(report) > 0 else 1
        counts = {
            'historical': 0,
            'segment_combination': 0,
            'new_calculation': 0
        }
        for entry in report:
            if 'Usando ruta frecuente' in entry['decision']:
                counts['historical'] += 1
            elif 'Combinando segmentos' in entry['decision']:
                counts['segment_combination'] += 1
            elif 'Calculando nueva ruta' in entry['decision']:
                counts['new_calculation'] += 1
        return {
            'historical': counts['historical'],
            'historical_pct': (counts['historical'] / total) * 100,
            'segment_combination': counts['segment_combination'],
            'segment_pct': (counts['segment_combination'] / total) * 100,
            'new_calculation': counts['new_calculation'],
            'new_pct': (counts['new_calculation'] / total) * 100
        }

# --- SIMULACIÓN DE PRUEBA ---
if __name__ == "__main__":
    # Crear un grafo de ejemplo
    g = Graph()
    # Crear nodos
    vA = g.insert_vertex("A")
    vB = g.insert_vertex("B")
    vC = g.insert_vertex("C")
    vD = g.insert_vertex("D")
    vE = g.insert_vertex("E")
    # Crear aristas con costos (distancias)
    g.insert_edge(vA, vB, 20)
    g.insert_edge(vB, vC, 15)
    g.insert_edge(vC, vD, 10)
    g.insert_edge(vD, vE, 25)
    g.insert_edge(vA, vC, 30)
    g.insert_edge(vB, vD, 35)
    g.insert_edge(vC, vE, 20)
    g.insert_edge(vA, vE, 60)
    # Definir almacén y clientes
    warehouse = [vA]
    clients = [vB, vC, vD, vE]
    # Simular
    sim = OrderSimulator(g, warehouse, clients)
    # Forzar estaciones de recarga útiles ANTES de las simulaciones
    sim.route_manager.add_charging_station(vC)
    sim.route_manager.add_charging_station(vD)

    # Primeras órdenes para poblar rutas históricas
    print("\nSimulación inicial para poblar rutas históricas:")
    sim.process_orders(7)  # Cambiado a 7 simulaciones

    # Forzar una combinación de segmentos
    print("\nSimulación con combinación de segmentos:")
    sim.route_tracker.register_route(['A', 'B', 'C'], 35)  # A->B->C
    sim.route_tracker.register_route(['C', 'D', 'E'], 35)  # C->D->E
    order_data = {
        'origin': vA,
        'destination': vE,
        'battery_limit': 100,
        'timestamp': datetime.now()
    }
    result = sim.process_single_order(order_data)
    print(f"\nOrden combinada: {result['origin']} → {result['destination']}")
    print(f"Ruta: {result['path']}")
    print(f"Costo: {result['cost']:.1f} | Batería usada: {result['battery_used']:.1f}%")
    print(f"Paradas de recarga: {len(result['recharge_stops'])} recargas ({result['recharge_stops']})")
    print(f"Tipo: {sim.translate_source(result['source'])}")
    print("-" * 50)
    sim.show_statistical_summary()

    # --- SIMULACIÓN EXTRA: Recarga obligatoria ---
    print("\nSimulación donde es obligatoria la recarga de energía:")
    order_data_recarga = {
        'origin': vA,
        'destination': vE,
        'battery_limit': 25,  # Menor que cualquier tramo largo
        'timestamp': datetime.now()
    }
    result_recarga = sim.process_single_order(order_data_recarga)
    print(f"\nOrden con recarga obligatoria: {result_recarga['origin']} → {result_recarga['destination']}")
    print(f"Ruta: {result_recarga['path']}")
    print(f"Costo: {result_recarga['cost']:.1f} | Batería usada: {result_recarga['battery_used']:.1f}%")
    print(f"Paradas de recarga: {len(result_recarga['recharge_stops'])} recargas ({result_recarga['recharge_stops']})")
    print(f"Tipo: {sim.translate_source(result_recarga['source'])}")
    print("-" * 50)

    # --- SIMULACIÓN EXTRA: Segmentos combinados obligatorios ---
    print("\nSimulación donde es obligatoria la combinación de segmentos:")
    sim.route_tracker = RouteTracker()
    sim.route_optimizer = RouteOptimizer(sim.route_tracker, sim.route_manager)
    sim.route_manager.add_charging_station(vC)
    sim.route_manager.add_charging_station(vD)
    sim.route_tracker.register_route(['A', 'B', 'C'], 35)  # A->B->C
    sim.route_tracker.register_route(['C', 'D', 'E'], 35)  # C->D->E

    order_data_segmentos = {
        'origin': vA,
        'destination': vE,
        'battery_limit': 100,
        'timestamp': datetime.now()
    }
    result_segmentos = sim.process_single_order(order_data_segmentos)
    print(f"\nOrden con combinación obligatoria de segmentos: {result_segmentos['origin']} → {result_segmentos['destination']}")
    print(f"Ruta: {result_segmentos['path']}")
    print(f"Costo: {result_segmentos['cost']:.1f} | Batería usada: {result_segmentos['battery_used']:.1f}%")
    print(f"Paradas de recarga: {len(result_segmentos['recharge_stops'])} recargas ({result_segmentos['recharge_stops']})")
    print(f"Tipo: {sim.translate_source(result_segmentos['source'])}")
    print("-" * 50)