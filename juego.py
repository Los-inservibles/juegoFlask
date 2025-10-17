import os
import random
import string
from datetime import datetime
from flask import Flask, jsonify, request, render_template

# Rutas absolutas para evitar problemas de ubicaciones Autor: Emmanuel Alvarez
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

DB_FILE = os.path.join(BASE_DIR, "db.json")

# Juegos activos en memoria (se persisten al terminar) Autor: Emmanuel Alvarez 
active_games = {}   # { game_id: {secret, attempts, score, created_at} }

# -------------------- Utilidades de archivo -------------------- Autor: Emmanuel Alvarez
def cargar_db():
    try:
        import json
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"games": {}}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
    #nuevo juego y numero
    game_id = "R" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    secret = random.randint(1,100)
    active_games[game_id] = {
        "secret": secret,
        "intentos": 0,
        "puntaje": 0,
        "creado_en": datetime.utcnow().isoformat() + "Z",
    }

    #para mostrar el numero en la consola
    print(f"[DEBUG] juego {game_id} iniciando... Numero secreto: {secret}")
    return jsonify({"ok": True, "game_id": game_id})

#Archivo decargado y creacion de rama

#Oscar Funcion de terminar el juego

@app.route("/finish", methods=["POST"])
def finish_game():
    """Finaliza el juego y lo guarda en db.json."""
    data = request.get_json(silent=True) or {}
    game_id = data.get("game_id")
    game = active_games.pop(game_id, None)

    if not game:
        return jsonify({"ok": False, "error": "ID de juego no válido o ya finalizado."}), 404

    db = cargar_db()
    db.setdefault("games", {})
    db["games"][game_id] = {
        "attempts": game["attempts"],
        "score": game["score"],
        "created_at": game["created_at"],
        "finished_at": datetime.utcnow().isoformat() + "Z",
    }
    guardar_db(db)
    print(f"[DEBUG] Juego {game_id} guardado en db.json -> {db['games'][game_id]}")
    return jsonify({
        "ok": True,
        "message": "Juego guardado correctamente.",
        "game_id": game_id,
        "attempts": game["attempts"],
        "score": game["score"],
        "finished": True
    })

#Oscar Funcion para mostrar los juegos guardados
@app.route('/games', methods=['GET'])
def get_all_devices():
    data = cargar_db()
    return jsonify(data["games"])



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)