
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/weather")
def weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "Digite uma cidade."}), 400

    if not API_KEY:
        return jsonify({"error": "Chave da API não configurada."}), 500

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("message", "Erro na consulta.")}), response.status_code

        return jsonify({
            "city": data["name"],
            "temperature": round(data["main"]["temp"]),
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind": round(data["wind"]["speed"] * 3.6, 1),
            "feels_like": round(data["main"]["feels_like"])
        })

    except requests.RequestException:
        return jsonify({"error": "Não foi possível conectar ao serviço de clima."}), 503


if __name__ == "__main__":
    app.run(debug=True)
