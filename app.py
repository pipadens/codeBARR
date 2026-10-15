from flask import Flask, render_template, request, jsonify

import sqlite3

app = Flask(__name__)


def init_db():
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS codigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


@app.route("/")
def index():
  return render_template("index.html")


# Ruta para el manifiesto PWA (permite instalar la app con su nombre e imagen)
@app.route("/manifest.json")
def manifest():
  manifest_data = {
      "name": "Codebarr",
      "short_name": "Codebarr",
      "start_url": "/",
      "display": "standalone",
      "background_color": "#0f172a",
      "theme_color": "#4f46e5",
      "icons": [{
          "src": "https://cdn-icons-png.flaticon.com/512/1048/1048953.png",
          "sizes": "512x512",
          "type": "image/png",
      }],
  }
  return jsonify(manifest_data)


@app.route("/api/guardar", methods=["POST"])
def guardar_codigo():
  data = request.json
  tipo = data.get("tipo")
  contenido = data.get("contenido")
  if not contenido:
    return jsonify({"error": "El contenido está vacío"}), 400

  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute(
      "INSERT INTO codigos (tipo, contenido) VALUES (?, ?)", (tipo, contenido)
  )
  conn.commit()
  conn.close()
  return jsonify({"mensaje": "Guardado exitosamente"})


@app.route("/api/codigos", methods=["GET"])
def obtener_codigos():
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute(
      "SELECT id, tipo, contenido, fecha FROM codigos ORDER BY id DESC"
  )
  rows = cursor.fetchall()
  conn.close()
  codigos = [{
      "id": r[0],
      "tipo": r[1],
      "contenido": r[2],
      "fecha": r[3],
  } for r in rows]
  return jsonify(codigos)


@app.route("/api/borrar/<int:id_codigo>", methods=["DELETE"])
def borrar_codigo(id_codigo):
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute("DELETE FROM codigos WHERE id = ?", (id_codigo,))
  conn.commit()
  conn.close()
  return jsonify({"mensaje": "Eliminado correctamente"})


if __name__ == "__main__":
  init_db()
  app.run(debug=True, port=5000)
