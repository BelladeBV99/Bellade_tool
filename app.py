from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/bereken", methods=["POST"])
def bereken():
    data = request.get_json()

    try:
        # Conversie en standaardwaardes
        parsed = {
            'vermogen': float(data.get('vermogen', 0)),
            'opstartkost': float(data.get('opstartkost', 0)),
            'huurprijs': float(data.get('huurprijs', 0)),
            'huurprijs_later': float(data.get('huurprijs_later', 0)),
            'starttarief': float(data.get('starttarief', 0)),
            'kwhprijs': float(data.get('kwhprijs', 0)),
            'parkeertarief': float(data.get('parkeertarief', 1)),
            'laadsessies': float(data.get('laadsessies', 0)),
            'kostprijsenergie': float(data.get('kostprijsenergie', 0)),
            'maandstijging': float(data.get('maandstijging', 0)),
            'verbruik_per_sessie': float(data.get('verbruik_per_sessie', 0)),
        }
    except Exception as e:
        return jsonify({"fout": f"Conversiefout in input: {e}"}), 400

    return jsonify(bereken_rendement(parsed))


def bereken_rendement(data):
    vermogen = data['vermogen']
    opstartkost = data['opstartkost']
    huurprijs = data['huurprijs']
    huurprijs_later = data['huurprijs_later']
    starttarief = data['starttarief']
    kwhprijs = data['kwhprijs']
    parkeertarief = data['parkeertarief']
    initiële_laadsessies = data['laadsessies']
    kostprijsenergie = data['kostprijsenergie']
    maandgroei = data['maandstijging']
    verbruik_per_sessie = data['verbruik_per_sessie']

    dagen_per_maand = 30
    g8 = (50 * vermogen) / 12
    k8 = g8 / 0.35

    sessies_rij_46 = []
    sessies = initiële_laadsessies
    for _ in range(144):
        sessies_rij_46.append(sessies)
        sessies *= (1 + maandgroei)

    maandwinsten = []
    for maand in range(144):
        sessies_dag = sessies_rij_46[maand]
        sessies_maand = sessies_dag * dagen_per_maand
        energie = sessies_maand * verbruik_per_sessie

        omzet = (
            sessies_maand * verbruik_per_sessie * kwhprijs +
            (starttarief + parkeertarief) * sessies_maand
        )

        energiekost = energie * kostprijsenergie
        capaciteitskost = g8 if energie > k8 else energie * 0.35
        huur = huurprijs if maand < 60 else huurprijs_later
        winst = omzet - energiekost - capaciteitskost - huur

        maandwinsten.append(winst)

    grafiek_data = []
    cumulatief = maandwinsten[0] - opstartkost
    grafiek_data.append(cumulatief)

    for i in range(1, 144):
        cumulatief += maandwinsten[i]
        grafiek_data.append(cumulatief)

    rendement_jaarlijks_lineair = round(
        (grafiek_data[-1]) / (opstartkost + (huurprijs * 60)) / 12 * 100, 2
    )

    return {
        'grafiek_data': [round(x, 2) for x in grafiek_data],
        'sessies_rij': sessies_rij_46,  # ✅ toegevoegd voor frontend maandvergelijking
        'energiehoeveelheid': round(sessies_rij_46[0] * dagen_per_maand * verbruik_per_sessie, 2),
        'energiekost': round((sessies_rij_46[0] * dagen_per_maand * verbruik_per_sessie) * kostprijsenergie, 2),
        'capaciteitskost': round(g8 if (sessies_rij_46[0] * dagen_per_maand * verbruik_per_sessie) > k8 else (sessies_rij_46[0] * dagen_per_maand * verbruik_per_sessie * 0.35), 2),
        'huurprijs': round(huurprijs, 2),
        'omzet': round(
            (sessies_rij_46[0] * dagen_per_maand * verbruik_per_sessie * kwhprijs) +
            (starttarief + parkeertarief) * sessies_rij_46[0] * dagen_per_maand,
        2),
        'rendement_maand_61': round(maandwinsten[60], 2),
        'rendement_12jaar': round(grafiek_data[-1], 2),
        'max_verlies': round(min(grafiek_data), 2),
        'terugverdentijd': next((i + 1 for i, val in enumerate(grafiek_data) if val >= 0), 144),
        'rendement_jaarlijks': rendement_jaarlijks_lineair
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
