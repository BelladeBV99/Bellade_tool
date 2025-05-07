from flask import Flask, request, jsonify
from bellade_logic import bereken_rendement
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/bereken", methods=["POST"])
def bereken():
    data = request.get_json()
    keys = [
        'vermogen', 'opstartkost', 'huurprijs', 'huurprijs_later', 'starttarief',
        'kwhprijs', 'parkeertarief', 'laadsessies', 'kostprijsenergie',
        'maandstijging', 'verbruik_per_sessie'
    ]
    try:
        data = {k: float(str(data.get(k, 0)).replace(',', '.')) for k in keys}
    except Exception as e:
        return jsonify({'fout': str(e)}), 400
    resultaat = bereken_rendement(data)
    return jsonify(resultaat)

if __name__ == "__main__":
    app.run(debug=True)

