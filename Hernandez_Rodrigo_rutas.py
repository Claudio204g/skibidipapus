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