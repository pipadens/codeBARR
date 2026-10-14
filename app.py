from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

# API para guardar un código o URL
@app.route('/api/guardar', methods=['POST'])
def guardar_codigo():
    data = request.json
    tipo = data.get('tipo')
    contenido = data.get('contenido')

    if not contenido:
        return jsonify({'error': 'El contenido está vacío'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO codigos (tipo, contenido) VALUES (?, ?)', (tipo, contenido))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Guardado exitosamente en la base de datos'})

# API para listar todos los registros guardados
@app.route('/api/codigos', methods=['GET'])
def obtener_codigos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, tipo, contenido, fecha FROM codigos ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()

    codigos = [{'id': r[0], 'tipo': r[1], 'contenido': r[2], 'fecha': r[3]} for r in rows]
    return jsonify(codigos)

# API para borrar un registro por su ID
@app.route('/api/borrar/<int:id_codigo>', methods=['DELETE'])
def borrar_codigo(id_codigo):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM codigos WHERE id = ?', (id_codigo,))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Registro eliminado correctamente'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
