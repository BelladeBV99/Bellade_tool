from typing import Dict

def bereken_rendement(data: Dict[str, float]) -> Dict:
    vermogen = data['vermogen']
    opstartkost = data['opstartkost']
    huurprijs = data['huurprijs']
    huurprijs_later = data['huurprijs_later']
    starttarief = data['starttarief']
    kwhprijs = data['kwhprijs']
    parkeertarief = 1
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
            sessies_dag * 30 * verbruik_per_sessie * kwhprijs +
            (starttarief + parkeertarief) * sessies_dag * 30
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
        'energiehoeveelheid': round(sessies_rij_46[0] * dagen_per_maand * verbruik_per_sessie, 2),
        'energiekost': round((sessies_rij_46[0] * dagen_per_maand * verbruik_per_sessie) * kostprijsenergie, 2),
        'capaciteitskost': round(g8 if (sessies_rij_46[0] * dagen_per_maand * verbruik_per_sessie) > k8 else (sessies_rij_46[0] * dagen_per_maand * verbruik_per_sessie * 0.35), 2),
        'huurprijs': round(huurprijs, 2),
        'omzet': round(
            (sessies_rij_46[0] * 30 * verbruik_per_sessie * kwhprijs) +
            (starttarief + parkeertarief) * sessies_rij_46[0] * 30,
        2),
        'rendement_maand_61': round(maandwinsten[60], 2),
        'rendement_12jaar': round(grafiek_data[-1], 2),
        'max_verlies': round(min(grafiek_data), 2),
        'terugverdentijd': next((i + 1 for i, val in enumerate(grafiek_data) if val >= 0), 144),
        'rendement_jaarlijks': rendement_jaarlijks_lineair
    }
