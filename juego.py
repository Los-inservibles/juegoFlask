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
#funciones bryan
@app.route("/guess", methods=["POST"])
def guess_number():
    """
    Evalúa el intento actual y da pistas por distancia.
    Rango de pistas (diferencia absoluta con el secreto):
      1-9   -> Muy cerca
      10-19 -> Cerca
      20-39 -> Lejos
      40+   -> Muy lejos
    """
    data = request.get_json(silent=True) or {}
    game_id = data.get("game_id")
    number = int(data.get("number", 0))

    if number < 1 or number > 100:
        return jsonify({"ok": False, "error": "El número debe estar entre 1 y 100."}), 400

    game = active_games.get(game_id)
    if not game:
        return jsonify({"ok": False, "error": "ID de juego no encontrado."}), 404

    game["attempts"] += 1
    secret = game["secret"]
    
        # Imprime el número secreto en consola en cada intento
    print(f"[DEBUG] Juego {game_id} | Intento: {number} | Secreto actual: {secret}")
    

    if number == secret:
        game["score"] += 100
        game["secret"] = random.randint(1, 100)  # nuevo secreto para seguir jugando
        print(f"[DEBUG] ¡Adivinó! Nuevo secreto para {game_id}: {game['secret']}")
        return jsonify({
            "ok": True,
            "result": "correcto",
            "message": "¡Correcto! +100 puntos. Se generó un nuevo número secreto.",
            "game_id": game_id,
            "attempts": game["attempts"],
            "score": game["score"],
            "finished": False
        })
    else:
        diferencia = abs(number - secret)
        if diferencia <= 9:
            pista = "Muy cerca"
        elif diferencia <= 19:
            pista = "Cerca"
        elif diferencia <= 39:
            pista = "Lejos"
        else:
            pista = "Muy lejos"
        print(f"[DEBUG] Juego {game_id} | Intento: {number} | Pista: {pista} | Dif: {diferencia}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)