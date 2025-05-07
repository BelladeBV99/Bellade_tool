from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bellade_logic import bereken_rendement
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/bereken', methods=['POST'])
def bereken():
    data = request.get_json()
    try:
        resultaat = bereken_rendement(data)
        return jsonify(resultaat)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

