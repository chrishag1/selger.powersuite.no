import sqlite3
import requests
from verktoy import sortere_norske_ord


def hent_power_butikker():
    url = "https://www.power.no/api/v2/products/1549292/stores?postalCode=1785"
    params = {
        "postalCode": 1785,
    }
    response = requests.get(url, params=params)
    return response.json()


def oppdater_power_butikker():
    butikker = []
    for butikk in hent_power_butikker():
        butikker.append({
            "id": butikk["storeId"],
            "navn": butikk["name"]
        })

    conn = sqlite3.connect('database.db')
    peker = conn.cursor()
    for butikk in butikker:
        navn = butikk["navn"].lower().replace("power ", "").replace("  ", " ").lower()
        peker.execute("INSERT INTO butikker (id, navn) VALUES (?, ?)", (butikk["id"], navn))
    conn.commit()
    conn.close()


def hent_alle_butikker():
    # Hente butikker fra SQL database
    conn = sqlite3.connect('database.db')
    peker = conn.cursor()
    peker.execute("SELECT navn FROM butikker")

    alle_butikker = []
    for butikk in peker.fetchall():
        alle_butikker.append(
            butikk[0].capitalize()
        )

    alle_butikker.sort(key=sortere_norske_ord)
    conn.close()

    return alle_butikker

def hent_butikk_id(navn):
    # Hente butikker fra SQL database
    conn = sqlite3.connect('database.db')
    peker = conn.cursor()
    peker.execute("SELECT id FROM butikker WHERE navn LIKE ?", (navn.lower(),))

    try:
        butikk_id = peker.fetchone()[0]
    except TypeError:
        butikk_id = 9700
    print(butikk_id)
    conn.close()

    return butikk_id

def hent_butikk_navn(id):
    # Hente butikker fra SQL database
    conn = sqlite3.connect('database.db')
    peker = conn.cursor()
    peker.execute("SELECT navn FROM butikker WHERE id = ?", (id,))

    try:
        butikk_navn = peker.fetchone()[0]
    except TypeError:
        butikk_navn = "Nettbutikk"
    print(butikk_navn)
    conn.close()

    return butikk_navn