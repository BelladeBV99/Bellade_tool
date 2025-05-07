from flask import Flask, request, jsonify
from bellade_logic import bereken_rendement
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/bereken", methods=["POST"])
def bereken():
    data = request.get_json()

    # Komma naar punt en string naar float conversie
    try:
        data = {k: float(str(v).replace(',', '.')) for k, v in data.items()}
    except Exception as e:
        return jsonify({"fout": f"Conversiefout in input: {e}"}), 400

    resultaat = bereken_rendement(data)
    return jsonify(resultaat)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

