import os
import random
import string
from datetime import datetime
from flask import Flask, jsonify, request, render_template

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)