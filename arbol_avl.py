class NodoAVL:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None
    
    def insertar(self, clave, valor):
        self.raiz = self._insertar(self.raiz, clave, valor)
    
    def _insertar(self, nodo, clave, valor):
        if not nodo:
            return NodoAVL(clave, valor)
        elif clave < nodo.clave:
            nodo.izquierda = self._insertar(nodo.izquierda, clave, valor)
        else:
            nodo.derecha = self._insertar(nodo.derecha, clave, valor)
        
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), 
                            self._obtener_altura(nodo.derecha))
        
        balance = self._obtener_balance(nodo)
        
        # Casos de rotación
        if balance > 1 and clave < nodo.izquierda.clave:
            return self._rotar_derecha(nodo)
        if balance < -1 and clave > nodo.derecha.clave:
            return self._rotar_izquierda(nodo)
        if balance > 1 and clave > nodo.izquierda.clave:
            nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        if balance < -1 and clave < nodo.derecha.clave:
            nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)
        
        return nodo
    
    def _obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura
    
    def _obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)
    
    def _rotar_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        
        y.izquierda = z
        z.derecha = T2
        
        z.altura = 1 + max(self._obtener_altura(z.izquierda), 
                         self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), 
                         self._obtener_altura(y.derecha))
        
        return y
    
    def _rotar_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        
        y.derecha = z
        z.izquierda = T3
        
        z.altura = 1 + max(self._obtener_altura(z.izquierda), 
                         self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), 
                         self._obtener_altura(y.derecha))
        
        return y
    
    def contiene(self, clave):
        return self._contiene(self.raiz, clave)
    
    def obtener(self, clave):
        return self._obtener(self.raiz, clave)
    
    def recorrido_inorden(self):
        resultado = []
        self._recorrido_inorden(self.raiz, resultado)
        return resultado
    
    # Métodos auxiliares (_contiene, _obtener, _recorrido_inorden)