import requests
from verktoy import finne_lagringsplass, finne_farge

def hent_produkt_liste(query, cat=2015, start_index=0):
    url = f"https://www.power.no/api/v2/productlists"
    params = {
        "size": 36,
        "cat": cat,
        "q": query,
        "s": 5,
        "from": start_index,
        "o": False
    }
    response = requests.get(url, params=params)
    svar = {
        "produkter": response.json()["products"],
        "antall": response.json()["totalProductCount"]
    }
    return svar


def hent_CNC_produkt_liste(query, butikk_id, cat=2015, start_index=0):
    url = f"https://www.power.no/api/v2/productlists"
    params = {
        "size": 36,
        "cat": cat,
        "q": query,
        "s": 5,
        "from": start_index,
        "o": False,
        "f": f"BasicCnC>>1<>{butikk_id}"
    }
    response = requests.get(url, params=params)
    svar = {
        "produkter": response.json()["products"],
        "antall": response.json()["totalProductCount"]
    }
    return svar


def hent_nettlager_produkt_liste(query, cat=2015, start_index=0):
    url = f"https://www.power.no/api/v2/productlists"
    params = {
        "size": 36,
        "cat": cat,
        "q": query,
        "s": 5,
        "from": start_index,
        "o": False,
        "f": "BasicInStock>>1<>WebStock"
    }
    response = requests.get(url, params=params)
    svar = {
        "produkter": response.json()["products"],
        "antall": response.json()["totalProductCount"]
    }
    return svar


def finn_produkt_liste_info(produkt_dict):
    return {
        "navn": produkt_dict.get("title", ""),
        "merke": produkt_dict.get("manufacturerName", ""),
        "pris": int(produkt_dict.get("price", "")),
        "beskrivelse": produkt_dict.get("shortDescription", ""),
        "salgsargument": produkt_dict.get("salesArguments", ""),
        "rating": round(produkt_dict.get("productReview", {}).get("overallAverageRating", 0), 2),
        "bilde": f"https://media.power-cdn.net{produkt_dict['productImage']['basePath']}/{produkt_dict["productImage"]["variants"][0]["filename"].replace('1200', '600').replace("150", "600")}",
        "url": f'https://www.power.no{ produkt_dict.get("url", "")}',
        "nettlager": produkt_dict.get("stockCount", 0),
        "nettlager_status": produkt_dict.get("webStockStatus", 3),
        "kategori": produkt_dict.get("categoryName", ""),
        "id": produkt_dict.get("productId", ""),
        "lagring": finne_lagringsplass(produkt_dict.get("title", "")),
        "farge": finne_farge(produkt_dict.get("title", ""))
    }

def finn_info_annen_farge_produkt(produkt_dict):
    return {
        "navn": produkt_dict.get("title", ""),
        "bilde": f"https://media.power-cdn.net{produkt_dict['productImage']['basePath']}/{produkt_dict["productImage"]["variants"][0]["filename"].replace('1200', '600').replace("150", "600")}",
        "nettlager": produkt_dict.get("stockCount", 0),
        "nettlager_status": produkt_dict.get("webStockStatus", 3),
        "id": produkt_dict.get("productId", ""),
        "lagring": finne_lagringsplass(produkt_dict.get("title", "")),
        "farge": finne_farge(produkt_dict.get("title", ""))
    }

def hent_frontpage(cat=2015):
    url = "https://www.power.no/api/v2/productlists"
    params = {
        "cat": cat,
        "size": 36,
        "s": 5,
        "from": 0,
        "o": False
    }
    response = requests.get(url, params=params)
    return response.json()["products"]



"""
dict_keys(['categoryId', 'categoryName', 'clickNCollectStoreCount', 'energyTier', 'isLimitedQuantity', 
'manufacturerName', 'manufacturerId', 'price', 'productId', 'salesArguments', 'shortDescription', 'stockCount', 
'storesStockCount', 'stockDeliveryDateConfirmed', 'stockLimitedRemaining', 'title', 'url', 'advertisingCampaigns', 
'breadcrumb', 'productReview', 'hasDescription', 'serviceCategoryId', 'vatPercent', 'modelType', 'priceType', 'barcode', 
'eanGtin12', 'showSavingsAs', 'productImage', 'productManuals', 'techLogo', 'campaignMediaUrl', 'campaignMediaAltText', 
'webStatus', 'productManufactorIdentity', 'webStockStatus', 'webStockText', 'webStockTextShort', 'webStockMeta', 
'cncStockStatus', 'cncStockText', 'canAddToCart', 'isOnDemand', 'elguideId', 'isRecurringPaymentProduct', 'depositPriceIncluded'])


"""