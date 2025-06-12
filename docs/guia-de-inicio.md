# Guía de Inicio

## Introducción
Esta guía proporciona los pasos necesarios para comenzar a trabajar con el proyecto de planificación inteligente de rutas para drones, incluyendo la simulación, visualización y análisis de rutas con restricciones energéticas.

## Configuración del Entorno

1. **Clona el repositorio**
   ```bash
   git clone <URL-del-repositorio>
   cd skibidipapus
   ```
2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configura las variables de entorno en caso de ser necesario**
   Asegúrate de tener las siguientes variables de entorno configuradas:
   - `DRONE_API_KEY`: Tu clave API para acceder a la funcionalidad del dron. 
   - `ROUTE_OPTIMIZATION_SERVICE`: URL del servicio de optimización de rutas.

## Primeros Pasos
Ejecuta la aplicación principal
streamlit run main.py
