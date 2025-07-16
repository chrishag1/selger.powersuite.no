from flask import Flask, render_template, request, url_for
from mobil_api_request import hent_produkt_liste, finn_produkt_liste_info, hent_CNC_produkt_liste, finn_info_annen_farge_produkt, hent_nettlager_produkt_liste, hent_frontpage
from verktoy import filtrer_ut_produktnavn, sortere_norske_ord
from database import hent_alle_butikker, hent_butikk_id
import sqlite3
import math

app = Flask(__name__)


@app.route('/')
def index():
    """
    Ting å legge til:

    filtrer på "merke"

    sortering:
        "mest relevant" : 5
        "kundeanmeldelser" : 8
        "alfabetisk" : 3
        "laveste pris" : 1
        "høyeste pris" : 2
        "merke" : 4

    """

    alle_butikker = hent_alle_butikker()
    alle_butikker.insert(0, "Nettbutikk")
    alle_butikker.insert(0, "Alle butikker")

    butikk = request.args.get("butikk", "Alle butikker")

    side = int(request.args.get("side", 0))

    produkt = request.args.get("produkt_sok", "")
    produkter = []
    if butikk == "Alle butikker":
        hentet_verdi = hent_produkt_liste(produkt, start_index=side*36)
        produkt_liste = hentet_verdi["produkter"]
        antall_produkter = hentet_verdi["antall"]
    elif butikk == "Nettbutikk":
        hentet_verdi = hent_nettlager_produkt_liste(produkt, start_index=side*36)
        produkt_liste = hentet_verdi["produkter"]
        antall_produkter = hentet_verdi["antall"]
    else:
        butikk_id = hent_butikk_id(butikk)
        hentet_verdi = hent_CNC_produkt_liste(produkt, butikk_id, start_index=side*36)
        produkt_liste = hentet_verdi["produkter"]
        antall_produkter = hentet_verdi["antall"]

    for produkt in produkt_liste:
        info = finn_produkt_liste_info(produkt)
        if info["kategori"].lower() == "mobiltelefon":
            info["url"] = url_for("mobiler", produkt=info["id"])
        #print(info)
        produkter.append(info)

    return render_template("produkter_grid.html",
                           produkt=produkt,
                           produkter=produkter,
                           alle_butikker=alle_butikker,
                           valgt_butikk=butikk,
                           side=side,
                           antall_sider=math.ceil(antall_produkter/36)
                           )

@app.route("/mobiler")
def mobiler():
    """

    :return:
    """
    kategori_nummer = 2015

    """Hente opp trykket produkt"""
    produkt_id = request.args.get("produkt")
    butikk = request.args.get("butikk", "Nettbutikk")
    butikk_id = 9700

    """Hente specs"""
    produkt_info = hent_produkt_liste(produkt_id)["produkter"][0]
    hoved_produkt = finn_produkt_liste_info(produkt_info)
    del produkt_info


    """Hente samme produkt, men annen lagring"""
    produkt_navn = filtrer_ut_produktnavn(hoved_produkt["navn"])
    like_produkter = hent_produkt_liste(produkt_navn, kategori_nummer)["produkter"]

    produkt_infoer = []
    ider = []
    for produkt in like_produkter:
        info = finn_info_annen_farge_produkt(produkt)
        navn = filtrer_ut_produktnavn(info["navn"])
        if navn == produkt_navn:
            print(info)
            info["tilgjengelighet"] = 0 #0=Ikke tilgjengelig, 9700=nettlager, {butikk_id}=butikk, 9800=kommer
            if info["nettlager"] > 0:
                info["tilgjengelighet"] = 9700

            elif info["nettlager_status"] == 2:     #Kommer til butikk
                info["tilgjengelighet"] = 9900

            produkt_infoer.append(info)
            ider.append(str(info["id"]))
    query = ",".join(ider)
    if butikk == "Alle butikker" or butikk == "Nettbutikk":
        cnc_produkter = hent_nettlager_produkt_liste(query, kategori_nummer)["produkter"]
    else:
        butikk_id = hent_butikk_id(butikk)
        cnc_produkter = hent_CNC_produkt_liste(query, butikk_id, kategori_nummer)["produkter"]
    cnc_ider = []

    for produkt in cnc_produkter:
        info = finn_produkt_liste_info(produkt)
        cnc_ider.append(info["id"])

    for produkt in produkt_infoer:
        if produkt["id"] in cnc_ider:
            produkt["tilgjengelighet"] = butikk_id

    sortert_produkter = {}
    produkt_infoer.sort(key=lambda x: float(x["lagring"]))
    for produkt in produkt_infoer:
        antall = sortert_produkter.get(produkt["lagring"], [])
        if antall:
            sortert_produkter[produkt["lagring"]].append(produkt)
        else:
            sortert_produkter[produkt["lagring"]] = [produkt]

    hoved_produkt_lagringer = {}
    for lagring in sortert_produkter.keys():
        for produkt in sortert_produkter[lagring]:
            if hoved_produkt["farge"] in produkt.values():
                hoved_produkt_lagringer[float(lagring)] = produkt["id"]

    samme_produkt_andre_farger = sortert_produkter.pop(hoved_produkt.get("lagring"), [hoved_produkt])

    alle_butikker = hent_alle_butikker()
    alle_butikker.insert(0, "Nettbutikk")
    alle_butikker.insert(0, "Alle butikker")

    return render_template("mobiler.html",
                           butikk_id=butikk_id,
                           valgt_butikk=butikk,
                           alle_butikker=alle_butikker,
                           kategori_nummer=kategori_nummer,
                           hoved_produkt=hoved_produkt,
                           andre_farger=samme_produkt_andre_farger,
                           annen_lagringsplass=sortert_produkter,
                           hoved_produkt_lagringer=hoved_produkt_lagringer
                           )




if __name__ == '__main__':
    app.run()

"""def main():
    url = "https://backend.pointandplace.com/matched/no/38c0f958-cc72-419c-9cfb-05eddad80a00?sku=3614194"
    #params = {"ids": "1512986,2669641,2671640,3568859,3614193,3614194,3614195,3614196,3614197,3614399,3615133,3615147,3615150,3615173,3615174,4041796,4042319"}

    svar = requests.get(url)
    print(svar.content)

if __name__ == '__main__':
    main()"""


"""

to sider:
moblier

laptop



#Teknisk
ved full string: kan hente flere elementer med komma-separator

iphone 16, 3614193 - 3614197
3 -> 7

categoryId: 2015 -> mobiler
"""