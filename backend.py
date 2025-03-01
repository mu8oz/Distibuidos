from flask import Flask, request
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

STORAGE_SERVER_URL = "http://localhost:5001/save_message"

@app.route('/')
def index():
    return "Backend Flask con WebSockets funcionando!"

@socketio.on('connect')
def handle_connect():
    print("Cliente conectado")
    emit('message', {'data': 'Conexión establecida'})

@socketio.on('client_message')
def handle_message(data):
    print(f"Mensaje recibido: {data}")
    
    # Guardar el mensaje en la base de datos
    try:
        response = requests.post(STORAGE_SERVER_URL, json={"message": data})
        if response.status_code == 200:
            print("Mensaje almacenado correctamente")
        else:
            print("Error al almacenar mensaje")
    except Exception as e:
        print(f"Error conectando al servicio de almacenamiento: {e}")
    
    emit('server_response', {'data': f"Mensaje recibido: {data}"}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
