import os
import random
import string
from datetime import datetime
from flask import Flask, jsonify, request, render_template

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)