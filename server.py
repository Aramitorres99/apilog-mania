from flask import Flask, request, jsonify
import datetime
from conexion import get_conexion
from psycopg2 import Error

app = Flask(__name__)

with open('tokens.txt') as f:
    VALID_TOKENS = {line.strip() for line in f}
    
    
@app.route('/logs', methods=['POST'])
def receive_logs():
    token = request.headers.get('Authorization')
    if token not in VALID_TOKENS:
        return jsonify({'estado': 'error', 'message' : 'Token invalido'}), 403
    log = request.json
    log['received_at'] = datetime.datetime.now().isoformat()
    
    # Imprimir el log recibido en la terminal
    print(f'Log Recibido: {log}')
    
    conn = get_conexion()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO logs (timestamp, service, level, message, received_at) VALUES (%s, %s, %s, %s, %s)',
                               (log['timestamp'], log['service'], log['level'], log['message'], log['received_at']))
                conn.commit()
                return jsonify({'estado': 'exitoso'})
            
        except Error as e:
            print(f'Error al insertar el log en la base de datos: {e}')
            return jsonify({"status": "error", "message": str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({"status": "error", "message": "Error de conexion a la base de datos"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
