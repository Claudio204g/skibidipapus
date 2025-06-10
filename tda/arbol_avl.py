class NodoAVL:
    """
    Representa un nodo en un árbol AVL.
    
    Attributes:
        clave: Clave para ordenar y buscar el nodo
        valor: Información almacenada en el nodo
        izquierda: Referencia al hijo izquierdo
        derecha: Referencia al hijo derecho
        altura: Altura del nodo en el árbol (para balanceo)
    """
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1  # Altura inicial es 1 (hoja)

class ArbolAVL:
    """
    Implementación de un árbol AVL (árbol binario de búsqueda balanceado).
    El árbol mantiene un equilibrio que garantiza operaciones en O(log n).
    """
    def __init__(self):
        self.raiz = None
    
    def insertar(self, clave, valor):
        """
        Inserta un nuevo par clave-valor en el árbol AVL.
        
        Args:
            clave: Clave para ordenar y buscar el valor
            valor: Información a almacenar
        """
        self.raiz = self._insertar(self.raiz, clave, valor)
    
    def _insertar(self, nodo, clave, valor):
        """
        Método recursivo auxiliar para insertar un nodo y balancear el árbol.
        
        Args:
            nodo: Nodo actual en la recursión
            clave: Clave a insertar
            valor: Valor a insertar
            
        Returns:
            El nodo (posiblemente nuevo) que ocupa esta posición después del balanceo
        """
        # Caso base: llegamos a una hoja
        if not nodo:
            return NodoAVL(clave, valor)
        # Navegación recursiva según BST
        elif clave < nodo.clave:
            nodo.izquierda = self._insertar(nodo.izquierda, clave, valor)
        else:
            nodo.derecha = self._insertar(nodo.derecha, clave, valor)
        
        # Actualizar altura del nodo actual
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), 
                            self._obtener_altura(nodo.derecha))
        
        # Calcular factor de balance
        balance = self._obtener_balance(nodo)
        
        # Casos de rotación para mantener el balance
        # Caso Izquierda-Izquierda: rotación simple a la derecha
        if balance > 1 and clave < nodo.izquierda.clave:
            return self._rotar_derecha(nodo)
        # Caso Derecha-Derecha: rotación simple a la izquierda
        if balance < -1 and clave > nodo.derecha.clave:
            return self._rotar_izquierda(nodo)
        # Caso Izquierda-Derecha: rotación doble (izquierda, luego derecha)
        if balance > 1 and clave > nodo.izquierda.clave:
            nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        # Caso Derecha-Izquierda: rotación doble (derecha, luego izquierda)
        if balance < -1 and clave < nodo.derecha.clave:
            nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)
        
        return nodo
    
    def _obtener_altura(self, nodo):
        """
        Obtiene la altura de un nodo (0 si el nodo es None).
        """
        if not nodo:
            return 0
        return nodo.altura
    
    def _obtener_balance(self, nodo):
        """
        Calcula el factor de balance de un nodo.
        Factor = altura(izquierda) - altura(derecha)
        """
        if not nodo:
            return 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)
    
    def _rotar_izquierda(self, z):
        """
        Realiza una rotación a la izquierda en el nodo z.
        
        Args:
            z: Nodo sobre el que realizar la rotación
            
        Returns:
            El nuevo nodo raíz después de la rotación
        """
        y = z.derecha  # y se convierte en la nueva raíz
        T2 = y.izquierda  # Subárbol que cambiará de padre
        
        # Realizar rotación
        y.izquierda = z
        z.derecha = T2
        
        # Actualizar alturas
        z.altura = 1 + max(self._obtener_altura(z.izquierda), 
                         self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), 
                         self._obtener_altura(y.derecha))
        
        return y  # Retornar nueva raíz
    
    def _rotar_derecha(self, z):
        """
        Realiza una rotación a la derecha en el nodo z.
        
        Args:
            z: Nodo sobre el que realizar la rotación
            
        Returns:
            El nuevo nodo raíz después de la rotación
        """
        y = z.izquierda  # y se convierte en la nueva raíz
        T3 = y.derecha  # Subárbol que cambiará de padre
        
        # Realizar rotación
        y.derecha = z
        z.izquierda = T3
        
        # Actualizar alturas
        z.altura = 1 + max(self._obtener_altura(z.izquierda), 
                         self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), 
                         self._obtener_altura(y.derecha))
        
        return y  # Retornar nueva raíz
    
    def contiene(self, clave):
        """
        Verifica si la clave existe en el árbol.
        
        Args:
            clave: Clave a buscar
            
        Returns:
            True si la clave existe, False en caso contrario
        """
        return self._contiene(self.raiz, clave)
    
    def obtener(self, clave):
        """
        Obtiene el valor asociado a una clave.
        
        Args:
            clave: Clave a buscar
            
        Returns:
            El valor asociado a la clave o None si no existe
        """
        return self._obtener(self.raiz, clave)
    
    def recorrido_inorden(self):
        """
        Realiza un recorrido inorden del árbol (izquierda-raíz-derecha).
        
        Returns:
            Lista con las claves en orden ascendente
        """
        resultado = []
        self._recorrido_inorden(self.raiz, resultado)
        return resultado
    
    # Métodos auxiliares para operaciones comunes
    def _contiene(self, nodo, clave):
        """
        Verifica recursivamente si la clave existe en el subárbol.
        """
        if not nodo:
            return False
        if clave == nodo.clave:
            return True
        elif clave < nodo.clave:
            return self._contiene(nodo.izquierda, clave)
        else:
            return self._contiene(nodo.derecha, clave)
    
    def _obtener(self, nodo, clave):
        """
        Busca recursivamente el valor asociado a una clave en el subárbol.
        """
        if not nodo:
            return None
        if clave == nodo.clave:
            return nodo.valor
        elif clave < nodo.clave:
            return self._obtener(nodo.izquierda, clave)
        else:
            return self._obtener(nodo.derecha, clave)
    
    def _recorrido_inorden(self, nodo, resultado):
        """
        Método auxiliar para realizar recorrido inorden recursivo.
        """
        if nodo:
            self._recorrido_inorden(nodo.izquierda, resultado)
            resultado.append(nodo.clave)
            self._recorrido_inorden(nodo.derecha, resultado)