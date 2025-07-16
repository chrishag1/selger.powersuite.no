import re

def sortere_norske_ord(ordet):
    alfabet = "abcdefghijklmnopqrstuvwxzyæøå"
    alfabet_dict = {bokstav: index for index, bokstav in enumerate(alfabet)}
    return [alfabet_dict.get(tegn, -1) for tegn in ordet.lower()]

def finne_lagringsplass_index(navn_liste):
    #Input: Apple iPhone 16 128 GB, svart
    #Output: 4

    if "tb" in navn_liste:
        lagring_index = navn_liste.index("tb")
    elif "gb" in navn_liste:
        lagring_index = navn_liste.index("gb")
    else:
        print(f"{IndexError} Fant ikke lagringsplass i navnet. {navn_liste}")
        navn_liste.append("16")
        navn_liste.append("mb")
        lagring_index = navn_liste.index("mb")

    return lagring_index

def filtrer_ut_produktnavn(produkt_tittel):
    #Input: Apple iPhone 16 128 GB, svart
    #Output: apple iphone 16

    uten_farge = produkt_tittel.lower().split(", ")[0]
    navn_liste = uten_farge.split(" ")
    lagring_index = finne_lagringsplass_index(navn_liste)
    navn_liste.pop(lagring_index - 1)
    navn_liste.pop(lagring_index - 1)

    return " ".join(navn_liste)

def finne_lagringsplass(produkt_tittel):
    #Input: Apple iPhone 16 128 GB, svart
    #Output: 128

    uten_farge = produkt_tittel.lower().replace("(","").replace(")","")
    uten_farge = re.sub(r'(?<=\d)/(?=\d)', ' ', uten_farge).split(", ")[0]
    navn_liste = uten_farge.split(" ")
    lagring_index = finne_lagringsplass_index(navn_liste)
    lagring = navn_liste[lagring_index - 1]
    if navn_liste[lagring_index] == "tb":
        lagring = int(lagring) * 1024
    elif navn_liste[lagring_index] == "mb":
        lagring = int(lagring) / 1024

    return str(lagring)


def finne_farge(produkt_tittel):
    #Input: Apple iPhone 16 128 GB, svart
    #Output: svart
    farge = ""
    if "gb" in produkt_tittel.lower():
        farge = produkt_tittel.lower().split("gb")[1]

    elif "tb" in produkt_tittel.lower():
        farge = produkt_tittel.lower().split("tb")[1]

    else:
        farge = produkt_tittel.lower().split(" ")[-1]

    return farge.replace(",", "").removeprefix(" ").capitalize()