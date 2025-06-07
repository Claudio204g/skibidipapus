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