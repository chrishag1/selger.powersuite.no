from mobil_api_request import hent_CNC_produkt_liste, hent_produkt_liste
from database import oppdater_power_butikker


def klikke_9700():
    print(hent_produkt_liste("iphone 16")[0]["manufacturerName"])


klikke_9700()
