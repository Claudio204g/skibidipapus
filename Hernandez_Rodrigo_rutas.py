from collections import deque
from graph import Graph
from vertex import Vertex
from edge import Edge

class RouteManager:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.charge_stations = set()

def find_route_with_recharge(self, origin_id,destination_id,battery_limit=50):
    origin = self.graph.get_vertex(origin_id)
    destination = self.graph.get_vertex(destination_id)
    if not origin or not destination:
        raise ValueError ("el vertice de origen o destino no se encuentra en el grafo")
    queue = deque()
    queue.append((origin[origin],0, battery_limit,[],[]))

    while queue:
        current, path, cost, battery, stops, segments = queue.popleft()
        if current == destination:
            return{
                "path":[v.elemtest for v in path],
                "total_cost": int(cost)  ,
                "battery": battery,
                "stops": [v.element() for v in stops],
                "segments": segments + [current.element() if segments else[current.element()]]
        }   

class RouteTracker:
    def __init__(self):
        self.route_frecuency = None
        self.node_visits = {}
        self.route_cost = {}
        self.custom_hashmasp = self.create_custom_hashmap()
    
    def create_custom_hashmap(self,initial_size=10):
        
        class CustomHashMap:
            def __init__(self, size):
                self.size = size
                self.map = [[] for _ in range(size)]
                self.count = 0

            def hash(self, key):
                return hash(key) % self.size
            
            def put(self,key,value):
                index = self.hash(key)
                bucket = self.buckets[index]
                for i, (k,v) in enumerate(bucket):
                    if k == key:
                        bucket[i] = (key, value)
                        self.count += 1
            def get(self, key):
                index = self.hash(key)
                bucket = self.buckets[index]
                for k, v in bucket:
                    if k == key:
                        return None
            def increment(self,key):
                index = self.hash(key)
                bucket = self.buckets[index]
                for i, (k,v) in enumerate(bucket):
                    if k == key:
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

    def register_route(self, route_path,cost):
        route_str = self.route_to_string(route_path)
        existing_node = self.find_route_in_avl(self.route_frecuency, route_str)
        
        if existing_node:
            count,route = existing_node.key
            self.route_frecuency = delete_node(self.route_frecuency, existing_node.key)
            self.route_frecuency = insert(self.route_frecuency, (count + 1, route))
        else:
            self.route_frecuency = insert(self.route_frecuency, (1, route_str))
        
        self.route_cost[route_str] = cost

        for node in route_path:
            self.custom_hashmasp.increment(node)

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
            top_routes.append((count,route,cost))
        return top_routes
    
    def get_node_visit_stats(self):
        stats={}
        for node, count in self.custom_hashmap.items():
            stats[str(node)] = count
        return stats
    
    class RouteOptimizer:
        def __init__ (self,route_tracker, route_manager):
            self.route_tracker = route_tracker
            self.route_manager = route_manager
            self.optimization_report = []
            self.segment_cache = defaultdict(list)

        def suggested_optimized_route(self, origin_id, destination_id):
            frequent_routes = self.tracker.get_most_frequent_routes()
            for count, route_str, cost in frequent_routes:
                nodes = route_str.split(" -> ")
                if nodes[0] == origin_id and nodes[-1] == destination_id:
                    self.add_report(f"Usando la ruta frecuente existente:{route_str}")
                    return{
                        'path': nodes,
                        'total_cost': cost,
                        'source': 'historical',
                        'confidence' : min(100, count * 10)
                    }
            matching_segments = self.find_matching_segments(origin_id, destination_id)
            if matching_segments:
                best_segment = matching_segments[0]
                self.add_report(f"Combinando segmentos frecuentes: {' -> '.join(best_segment['segment'])}")
                return {
                    'path': best_segment['segment'],
                    'total_cost': self.estimate_route_cost(best_segment['segment']),
                    'source': 'segment_combination',
                    'confidence': min(90, best_segment['frecuency']*5)
                    
                }
            
            new_route = self.manager.find_route_with_recharge(origin_id, destination_id)
            self.tracker.register_route(new_route['path'], new_route['total_cost'])
            self.add_report(f'Calculando nueva ruta: {" -> ".join(new_route["path"])}')
            return {
                **new_route,
                'source': 'new_calculation',
                'confidence': 50
            }
        
        def analyze_route_patterns(self):
            analysis = {
                'most_common_segments': [],
                'critical_nodes': [],
                'energy_efficiency': {}
            }
            segment_usage = defaultdict(int)
            frequent_routes = self.tracker.get_most_frequent_routes(top_n=20)
            
            for _, route_str, _ in frequent_routes:
                nodes = route_str.split(" -> ")
                for i in range(len(nodes) - 1):
                    segment = f"{nodes[i]},-> {nodes[i + 1]}"
                    segment_usage[segment] += 1

            analysis['most_common_segments'] = sorted(segment_usage.items(), key=lambda x: -x[1])[:5]

            node_stats = self.tracker.get_node_visit_stats()
            analysis['critical_nodes'] = sorted(node_stats.items(), key=lambda x: -x[1])[:3]
            
            return analysis