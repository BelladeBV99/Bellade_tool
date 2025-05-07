from flask import Flask, request, jsonify
from bellade_logic import bereken_rendement
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/bereken", methods=["POST"])
def bereken():
    data = request.get_json()

    # Alleen de benodigde velden behouden en converteren
    benodigde_keys = [
        'vermogen', 'opstartkost', 'huurprijs', 'huurprijs_later',
        'starttarief', 'kwhprijs', 'laadsessies', 'kostprijsenergie',
        'maandstijging', 'verbruik_per_sessie'
    ]

    try:
        data = {
            k: float(str(data.get(k, 0)).replace(',', '.'))
            for k in benodigde_keys
        }
    except Exception as e:
        return jsonify({"fout": f"Conversiefout in input: {e}"}), 400

    resultaat = bereken_rendement(data)
    return jsonify(resultaat)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

