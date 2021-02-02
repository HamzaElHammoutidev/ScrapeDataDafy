# encoding: utf-8

from bs4 import BeautifulSoup
import requests,json,sys
from re import search


# -*- coding: utf-8 -*-

# List of Links of all Products Fetched from List
LinksList = []
ProductsList = []

# Mash Motos Pages List
motosList = ["http://www.mash-motors.fr/fr/203-motos","http://www.mash-motors.fr/fr/203-motos?p=2","http://www.mash-motors.fr/fr/203-motos?p=3","http://www.mash-motors.fr/fr/252-side-car"]
# Moto Table Defnition
moto_table = {
        "id":"",
        "date_debut_prod":"",
        "date_fin_prod":"",
        "name":"",
        "slug":"",
        "marque_id":"", #int
        "is_vente":"", #Booolen
        "img":"",
        "moto_type_id":"",
        "cylindre":"", #Int
        "distribution":"",
        "puissance_annoncee":"",
        "couple_annoncee":"",
        "alimentation":"",
        "demarreur":"",
        "consommation":"",
        "emission_coe":"",
        "boite":"",
        "embratage":"",
        "empattement":"",
        "suspension_avant":"",
        "suspension_arriere":"",
        "frein_avant":"",
        "frein_arriere":"",
        "pneu_avant":"",
        "pneu_arriere":"",
        "dimension":"",
        "hauteur_selle":"",
        "garde_sol":"",
        "essence":"",
        "huile":"",
        "poids":"",
        "garantie":"",
    }
moto_image_table = {
    "couleur":"",
    "id": "",
    "images": "",
    "moto_id": "",
}


"""
Get All Links from Products List 
:arg 
    - Links List as Global : Lists that where we store all of products links 
    - MotosList as Global : List of all product lists  to iterate over  
"""
def getLinks():
    global LinksList
    global motosList
    for motoPage in motosList:
        page = requests.get(motoPage)
        soup = BeautifulSoup(page.text, "html.parser")
        # Get Products Rectangles
        products = soup.select(".product-container")
        # Loop over products to fetch data
        for product in products:
            # Fetch link of every product
            LinksList.append(product.find('a',attrs={"class":"product_img_link"})["href"])
    print("Links Fetched !")


"""
Get All Product Details and Store them into a json 
:arg 
    - Links List to iterate over to find product detials 
    - Photos List 
    - Description 
    - Out : List of Products Details -> ProductsList
"""
def getProductData():
    global ProductList
    getLinks()
    global LinksList
    for productLink in LinksList: # Iterate Over all Product Links
        PhotosList = [] # Intiated Photos list for every product
        page = requests.get(productLink)
        soup = BeautifulSoup(page.text,"html.parser")
        # Select List of All Photos of any product
        phl = soup.find("ul",attrs={"id":"thumbs_list_frame"})
        productTitle = soup.find('h1',attrs={"itemprop":"name"}).text
        photos = phl.select("li")
        for photo in photos:
                PhotosList.append(photo.find("a")["href"]) # Inserting all of photos product links in our Photos List
        # Fetching prodcut Description
        description = soup.find("section", attrs={"class": "page-product-box"})
        #print(productLink)
        coloris = "default"
        itemsdsc = description.find("div", attrs={"class": "rte"})
        ps = itemsdsc.findAll("p")
        #print(len(ps))
        for item in ps:
            if "Coloris" in item.text:
                try:
                    coloris = item.text.split(":")[1]
                except Exception:
                    colors = "default"
                break
        #print(coloris)
        # Fetching La Fiche technique
        lafiche = soup.find("div", attrs={"class": "fiche-technique__container"})
        titles = lafiche.select(".fiche-technique__titre")
        content = lafiche.select(".list.hidden-xs")
        count = 0
        FicheList = []  # Fiche items List
        for i in range(0, int(len(content))):
            ItemList = []  # Loop Over Content Items And Append on List
            contentList = content[i].select("li")  # Get Section Content
            for itemContenct in contentList:  # Fetch over content Section
                ItemList.append(itemContenct.text)  # Get Every Conttent Item
            item = {titles[i].text.replace(" :", ""): ItemList}
            FicheList.append(item)
            count += 1
        # Create a Product Item

        product = {
            "titre": productTitle,
            "photos": PhotosList,
            "fiche-technique": FicheList,
            "coloris": coloris
        }

        print(json.dumps(product))
        ProductsList.append((product))
        with open("dataMash.json","w",encoding="utf-8") as jsonfile:
            json.dump(ProductsList,jsonfile,ensure_ascii=False)


"""
Form Data Model for Motos Table

"""
NeededBikes = ["FALCONE - ROUGE 125cc",
"FALCONE 125cc-Noir Mat	",
"SEVENTY 125 Copper",
"NEW SEVENTY 125cc-Noir",
"CAFE RACER 125cc",
"DIRT TRACK 125cc-Noir",
"DIRT TRACK 125cc-Blanc Mat",
"DIRT TRACK 125cc Blanc-Nouveauté 2020",
"BLACK SEVEN 125cc",
"SCRAMBLER 400cc - Rouge/Silver",
"SCRAMBLER 400cc - Orange/Gris",
"SCRAMBLER 400cc - CHROME",
"FIVE HUNDRED 400cc - Noir",
"DIRT TRACK - NOIR 650 cc",
"DIRT TRACK 650 cc -  GRIS",
"CAFE RACER 400cc - Candy Red",
"FAMILY SIDE 400cc-Vert"]
ListMoto = []
ListVariantes = []
def DataTransformation():
    id_moto = 3000
    variante_moto = 5000
    global ListMoto
    # Read Data from Json Mash File
    jsonfile= open("dataMash.json","r",encoding="utf-8")
    mash_data = json.load(jsonfile) # Read Data
    for moto in mash_data: # Looping over Mash moto Data from json
        # Check if moto is needed or not
        for needed_moto in NeededBikes:
            if moto["titre"] == needed_moto:
                moto_table["id"] = id_moto
                id_moto = id_moto + 1
                moto_image_table["moto_id"]= id_moto
                moto_image_table["id"] = variante_moto
                variante_moto += 1
                try:
                    moto_image_table["images"]= str(moto["photos"])
                except  Exception:
                    moto_image_table["images"] = str([])
                if moto["coloris"] == "default":
                    for col in ["Noir","Blanc Mat","Blanc","Rouge/Silver","Orange/Gris","CHROME","GRIS","Candy Red","Blanc Mat","Vert"]:
                        if search(col, moto["titre"]):
                            moto_image_table["couleur"] = col
                            break
                        else:
                            moto_image_table["couleur"] = "default"
                else:
                    moto_image_table["couleur"]= moto["coloris"]
                print(moto_image_table["couleur"])
                moto_table["date_debut_prod"] = 2020
                moto_table["marque_id"] = 194
                moto_table["is_vente"] = 1
                moto_table["name"] = moto["titre"] # name
                moto_table["slug"] = moto["titre"].lower().replace(" ","-")
                moto_table["img"] = moto["photos"][0]
                moto_table["moto_type_id"] = 1
                for element in (moto["fiche-technique"]):
                    keys = (element.keys()) # Get All Fiche Technique key to check if Item is elready there or not
                    for key in keys :
                        if "moteur" in str(key).lower(): # Get All Moteur Elements List
                            for LI in element[key]:
                                if "Cylindrée" in LI: # Check if Cylndrée in Moteur Elements List
                                    try:
                                        moto_table["cylindre"] = (str(LI.split(":")[1]).replace("cc","").strip()) # Clean and Insert Cylindre in to Moto Object if it contains ":" otherwise exception
                                    except Exception:
                                        moto_table["cylindre"] = (str(LI.replace("Cylindrée","").replace("cc","").strip())) # If element doesn't contain ":" it will be cleaned differently
                                if "Alimentation" in LI:  # Check if Allumage in Moteur Elements List
                                    try:
                                        moto_table["alimentation"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                "").strip())
                                    except Exception:
                                        moto_table["alimentation"] = (str(LI.replace("Alimentation", "").replace("cc",
                                                                                                         "").strip()))
                                if "Démarrage" in LI:
                                    try:
                                        moto_table["demarreur"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                    "").strip())
                                    except Exception:
                                        moto_table["demarreur"] = (str(LI.replace("Démarrage", "").replace("cc",
                                                                                                             "").strip()))
                                if "Couple" in LI:
                                    try:
                                        moto_table["couple_annoncee"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                    "").strip())
                                    except Exception:
                                        moto_table["couple_annoncee"] = (str(LI.replace("Couple", "").replace("cc",
                                                                                                        "").strip()))
                        if "châssis" in str(key).lower():
                            for LI in element[key]:
                                if "Suspension avant" in LI:
                                    try:
                                       moto_table["suspension_avant"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["suspension_avant"] = (str(LI.replace("Suspension avant", "").replace("cc",
                                                                                                            "").strip()))
                                if "Suspension avant" in LI:
                                    try:
                                       moto_table["suspension_avant"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["suspension_avant"] = (str(LI.replace("Suspension avant", "").replace("cc",
                                                                                                            "").strip()))
                                if "Frein avant" in LI:
                                    try:
                                       moto_table["frein_avant"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["frein_avant"] = (str(LI.replace("Frein avant", "").replace("cc",
                                                                                                            "").strip()))
                                if "Frein arrière" in LI:
                                    try:
                                       moto_table["frein_arriere"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["frein_arriere"] = (str(LI.replace("Frein arrière", "").replace("cc",
                                                                                                            "").strip()))
                                if "Suspension AR" in LI:
                                    try:
                                       moto_table["suspension_arriere"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["suspension_arriere"] = (str(LI.replace("Suspension AR", "").replace("cc",
                                                                                                            "").strip()))
                                if "Pneu arrière" in LI:
                                    try:
                                       moto_table["pneu_arriere"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["pneu_arriere"] = (str(LI.replace("Pneu arrière", "").replace("cc",
                                                                                                            "").strip()))
                                if "Pneu avant" in LI:
                                    try:
                                       moto_table["pneu_avant"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["pneu_avant"] = (str(LI.replace("Pneu avant", "").replace("cc",
                                                                                                            "").strip()))
                        if "dimensions" in str(key).lower():
                            for LI in element[key]:
                                if "Hauteur de selle" in LI:
                                    try:
                                       moto_table["hauteur_selle"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["hauteur_selle"] = (str(LI.replace("Hauteur de selle ", "").replace("cc",
                                                                                                            "").strip()))
                                if "L x l x h" in LI:
                                    try:
                                       moto_table["dimension"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["dimension"] = (str(LI.replace("L x l x h", "").replace("cc",
                                                                                                            "").strip()))
                                if "Poids à sec" in LI:
                                    try:
                                       moto_table["poids"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["poids"] = (str(LI.replace("Poids à sec", "").replace("cc",
                                                                                                            "").strip()))
                                if "Réservoir d’essence" in LI:
                                    try:
                                       moto_table["essence"] = (str(LI.split(":")[1]).replace("cc",
                                                                                                       "").strip())
                                    except Exception:
                                        moto_table["essence"] = (str(LI.replace("Réservoir d’essence", "").replace("cc",
                                                                                                            "").strip()))
                ListVariantes.append((moto_image_table.copy()))
                ListMoto.append(moto_table.copy())
                NeededBikes.remove(needed_moto)


getProductData()
DataTransformation()
print(json.dumps(ListMoto))
print(json.dumps(ListVariantes))
