from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Crear la base de datos y la tabla si no existen
def init_db():
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            content TEXT NOT NULL
                          )''')
        conn.commit()

init_db()

@app.route('/save_message', methods=['POST'])
def save_message():
    data = request.json
    message = data.get("message")
    
    if not message:
        return jsonify({"error": "Mensaje vacío"}), 400
    
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (content) VALUES (?)", (message,))
        conn.commit()
    
    return jsonify({"success": True, "message": "Mensaje guardado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
