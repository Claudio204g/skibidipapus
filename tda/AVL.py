class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 0  # nodo singular tiene altura 0

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, N):
        return -1 if N is None else N.height

    def get_balance(self, N):
        return 0 if N is None else self.height(N.left) - self.height(N.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Rotación
        x.right = y
        y.left = T2

        # Actualizar alturas
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1

        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Rotación
        y.left = x
        x.right = T2

        # Actualizar alturas
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1

        return y

    def _insert(self, node, key, value=None):
        if node is None:
            return Node(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # Si la clave ya existe, actualizar el valor
            node.value = value
            return node

        node.height = max(self.height(node.left), self.height(node.right)) + 1
        balance = self.get_balance(node)

        # Casos de desbalanceo
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert(self, key, value=None):
        """Inserta una clave con su valor opcional en el árbol."""
        self.root = self._insert(self.root, key, value)
    
    def insertar(self, key, value=None):
        """Alias de insert para compatibilidad con la simulación."""
        self.insert(key, value)

    def _find(self, node, key):
        """Busca un nodo por su clave."""
        if node is None:
            return None
        if key < node.key:
            return self._find(node.left, key)
        elif key > node.key:
            return self._find(node.right, key)
        else:
            return node

    def contiene(self, key):
        """Verifica si una clave existe en el árbol."""
        return self._find(self.root, key) is not None

    def obtener(self, key):
        """Obtiene el valor asociado a una clave."""
        node = self._find(self.root, key)
        return node.value if node else None
    
    def _inorden(self, node, keys):
        """Recorrido inorden auxiliar."""
        if node:
            self._inorden(node.left, keys)
            keys.append(node.key)
            self._inorden(node.right, keys)
    
    def recorrido_inorden(self):
        """Retorna todas las claves del árbol en orden."""
        keys = []
        self._inorden(self.root, keys)
        return keys

    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _delete_node(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            if root.left is None or root.right is None:
                root = root.left or root.right
            else:
                temp = self.min_value_node(root.right)
                root.key = temp.key
                root.right = self._delete_node(root.right, temp.key)

        if root is None:
            return root

        root.height = max(self.height(root.left), self.height(root.right)) + 1
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete_node(self, key):
        self.root = self._delete_node(self.root, key)

    def pre_order(self):
        self._pre_order(self.root)
        
    def _pre_order(self, root):
        if root:
            print(f"{root.key} ", end="")
            self._pre_order(root.left)
            self._pre_order(root.right)

# Prueba
if __name__ == "__main__":
    avl_tree = AVLTree()
    for key in [9, 5, 10, 0, 6, 11, -1, 1, 2]:
        avl_tree.insert(key)

    print("Preorden del AVL construido:")
    avl_tree.pre_order()

    avl_tree.delete_node(10)
    print("\nPreorden luego de eliminar 10:")
    avl_tree.pre_order()
