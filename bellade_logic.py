from typing import Dict
import numpy as np

def bereken_rendement(data: Dict[str, float]) -> Dict:
    vermogen = data['vermogen']
    opstartkost = data['opstartkost']
    huurprijs = data['huurprijs']
    starttarief = data['starttarief']
    kwh_prijs = data['kwhprijs']
    parkeertarief = 1
    laadsessies_per_dag = data['laadsessies']
    kostprijs_energie = data['kostprijsenergie']
    maandgroei = data['maandstijging']

    dagen_per_maand = 30
    maanden = 144
    vermogen_per_sessie = vermogen / 2

    energiehoeveelheid = laadsessies_per_dag * dagen_per_maand * vermogen_per_sessie
    omzet = laadsessies_per_dag * dagen_per_maand * (starttarief + parkeertarief + vermogen_per_sessie * kwh_prijs)
    energiekost = energiehoeveelheid * kostprijs_energie
    capaciteitskost = vermogen * 0.98

    grafiek_data = []
    cumulatief = -opstartkost
    maand_sessies = laadsessies_per_dag

    for maand in range(maanden):
        sessies = maand_sessies * dagen_per_maand
        energie = sessies * vermogen_per_sessie
        omzet_m = sessies * (starttarief + parkeertarief + vermogen_per_sessie * kwh_prijs)
        energiekost_m = energie * kostprijs_energie
        capaciteit_m = vermogen * 0.98
        winst = omzet_m - energiekost_m - capaciteit_m - huurprijs
        cumulatief += winst
        grafiek_data.append(cumulatief)
        maand_sessies *= (1 + maandgroei)

    rendement_maand_61 = grafiek_data[60] if len(grafiek_data) > 60 else 0
    rendement_12jaar = grafiek_data[-1]
    max_verlies = min(grafiek_data)
    terugverdentijd = next((i + 1 for i, val in enumerate(grafiek_data) if val >= 0), maanden)
    rendement_jaarlijks = ((rendement_12jaar + opstartkost) / opstartkost) ** (1 / 12) - 1

    return {
        'energiehoeveelheid': energiehoeveelheid,
        'omzet': omzet,
        'energiekost': energiekost,
        'capaciteitskost': capaciteitskost,
        'huurprijs': huurprijs,
        'grafiek_data': grafiek_data,
        'rendement_maand_61': rendement_maand_61,
        'rendement_12jaar': rendement_12jaar,
        'max_verlies': max_verlies,
        'terugverdentijd': terugverdentijd,
        'rendement_jaarlijks': rendement_jaarlijks * 100
    }