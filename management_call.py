from flask import Flask, request, jsonify
import threading
import time
import random
import sys

app = Flask(__name__)

# Configuraciones iniciales
MAX_LLAMADAS = 5
llamadas_activas = 0
monitor_url = "http://localhost:5002/report-status"  # URL del monitor
lock = threading.Lock()  # Para manejar el acceso concurrente al contador
monitoreo_activo = True  # Para controlar el monitoreo constante
puerto_nodo = sys.argv[1]  # Extraer el puerto de ejecución del microservicio

# Función que simula el procesamiento de una llamada
def procesar_llamada(client_id):
    global llamadas_activas

    # Simular un tiempo de procesamiento de la llamada (5-30 segundos)
    tiempo_procesamiento = random.randint(5, 30)
    time.sleep(tiempo_procesamiento)

    # Decrementar el contador de llamadas activas
    with lock:
        llamadas_activas -= 1
        print(f"Llamada completada. Llamadas activas: {llamadas_activas}")

    # Después de procesar la llamada, verificar el estado y reportar al monitor
    if llamadas_activas < MAX_LLAMADAS:
        reportar_estado(True)

# Endpoint para recibir y procesar una llamada
@app.route('/process-call', methods=['POST'])
def recibir_llamada():
    global llamadas_activas

    # Verificar si el nodo puede procesar más llamadas
    with lock:
        if llamadas_activas >= MAX_LLAMADAS:
            return jsonify({'mensaje': 'Nodo lleno, no puede procesar más llamadas'}), 503

        # Incrementar el contador de llamadas activas
        llamadas_activas += 1
        print(f"Nueva llamada recibida. Llamadas activas: {llamadas_activas}")

    # Simular el procesamiento de la llamada en un nuevo hilo
    client_id = request.json.get('client', 'desconocido')
    hilo = threading.Thread(target=procesar_llamada, args=(client_id,))
    hilo.start()

    return jsonify({'mensaje': 'Llamada en proceso'}), 200

# Función para reportar el estado del nodo al monitor
def reportar_estado(estado_disponible):
    data = {
        "node": f"Nodo_{puerto_nodo}",  # El identificador del nodo será el puerto actual
        "status": estado_disponible  # True: disponible, False: no disponible
    }
    try:
        # response = requests.post(monitor_url, json=data)
        print(f"Estado reportado al monitor: {estado_disponible}, nodo: {puerto_nodo}")
    except Exception as e:
        print(f"Error al reportar al monitor: {e}")

# Función para monitorear constantemente el estado del microservicio
def monitoreo_constante():
    global llamadas_activas

    while monitoreo_activo:
        # Reportar el estado cada 10 segundos (puedes ajustar este valor)
        with lock:
            estado_disponible = llamadas_activas < MAX_LLAMADAS
            reportar_estado(estado_disponible)
        time.sleep(1)  # Ajusta el intervalo de monitoreo

# Iniciar un hilo separado para el monitoreo constante
def iniciar_monitoreo():
    hilo_monitoreo = threading.Thread(target=monitoreo_constante)
    hilo_monitoreo.daemon = True  # El hilo se detendrá cuando la aplicación finalice
    hilo_monitoreo.start()

if __name__ == '__main__':
    # Iniciar el monitoreo constante antes de ejecutar la aplicación
    iniciar_monitoreo()
    app.run(port=puerto_nodo, debug=False)
