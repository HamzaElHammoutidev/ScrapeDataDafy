# encoding: utf-8

# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests,json,re


mainWebsite = "https://www.dafy-moto.com"
constructeursLinks = []
constructeursTypesLinks = []
constructeursMotosTypesLinks = []
constructeursYearsMotosTypesLinks = []
constructeursCategoryMotosLinks = []
constructeursCategoryMotosDataLinks = []

"""
HELPERS 
"""
def get_pages_number(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"html.parser")
    try:
        pageCount = max(list(map(lambda x :int(x['data-page']),soup.find_all(attrs={'data-page':re.compile(r".*")}) ))) # Get Number of Pages
        return pageCount
    except Exception:
        return 1



"""
function: Fetching all contrsucteur links of different marques
List : Links of Contrsuteurs 
"""
def getContrsucteurLinks():
    global constructeursLinks
    # Get Constructeurs Page
    constructeursPages = requests.get("https://www.dafy-moto.com/constructeurs-moto-scooter.html")
    # Conversion Html with BS4
    soup = BeautifulSoup(constructeursPages.text, "html.parser")
    constructeurs = (soup.select(".item-result-wrapper__list-item"))
    for constructeur in constructeurs:
        constructeurLink = constructeur.find("a")["href"]
        if len(constructeurLink.split("/")) <= 3:
            constructeursLinks.append(constructeurLink)


"""
function: get every constructeur different types 
List  : Contrsteur / Type / Link 
"""
def getConstructeurTypes():
    global constructeursTypesLinks
    for contrsuteur in constructeursLinks:
        req = requests.get(mainWebsite+contrsuteur)
        soup = BeautifulSoup(req.text, "html.parser")
        bread = (soup.find("ol",{"class":"breadcrumb"}))
        constructor = (bread.find_all("li")[2].text)
        types = soup.select(".item-result-wrapper__title.item-result-wrapper__title--border")
        for type in types:
            link = (type.find("a")["href"])
            type = (type.text.strip())
            item = {"constructeur" : constructor,
                    "link":link,
                    "type":type}
            constructeursTypesLinks.append(item)


"""
function: get Motos by constructeur and type
List : contstructeur, type, motos , link 
"""
def getMotosbyType():
    global constructeursMotosTypesLinks
    for type in constructeursTypesLinks:
        req = requests.get(type["link"])
        soup = BeautifulSoup(req.text, "html.parser")
        # Contrsuteur
        bread = (soup.find("ol", {"class": "breadcrumb"}))
        constructor = (bread.find_all("li")[2].text)
        type = (bread.find_all("li")[3].text)
        # Moto Data
        motos = (soup.select(".item-result-wrapper__list-item"))
        for moto in motos:
            link = (moto.find("a")["href"])
            textData = (moto.text.strip())
            item = {
                "constructeur":constructor,
                "type":type,
                "link-moto": link,
                "moto":textData
            }
            constructeursMotosTypesLinks.append(item)

"""
function: get all year of every moto
List : constructeur, type, moto, year, link 
"""
def getMotosByYear():
    global constructeursYearsMotosTypesLinks
    jsonfile = open("data/dataMotoType.json", "r", encoding="utf-8")
    typesMotosData  = json.load(jsonfile)  # Read Data
    for moto in typesMotosData:
        req = requests.get(mainWebsite+moto["link-moto"])
        soup = BeautifulSoup(req.text, "html.parser")
        yearsSelection = (soup.select(".c-select.form-control.js-select-vehicle"))
        years = (yearsSelection[0].find_all("option"))
        years = (years[1:])
        for year in years:
            year_link = moto["link-moto"].replace(".html", "") + "/" + str(year.text) + ".html"
            item = {
                "constructeur":moto["constructeur"],
                "type":moto["type"],
                "link-moto":moto["link-moto"],
                "moto":moto["moto"],
                "year":year.text,
                "year-link":year_link
            }
            print(json.dumps(item))
            constructeursYearsMotosTypesLinks.append((item))

"""
function: get Motocycle Categories Compatibility
List : Constructeur, Type, Moto, Year, Link, Category, Category-Link
"""
def getCategoryMoto():
    global constructeursCategoryMotosLinks
    jsonfile = open("data/dataMotoTypeYear.json", "r", encoding="utf-8")
    typesMotosData = json.load(jsonfile)  # Read Data
    for moto in typesMotosData:
        req = requests.get(mainWebsite+moto["year-link"])
        soup = BeautifulSoup(req.text, "html.parser")
        categories = (soup.select(".item-result-wrapper__list-item.js-custom-menu-link"))
        for category in categories:
            category_link = (category.find("a")["data-url"])
            category_text = (category.text.strip())
            item = {
                "constructeur" : moto["constructeur"],
                "type":moto["type"],
                "link-moto" : moto["link-moto"],
                "moto":moto["moto"],
                "year":moto["year"],
                "year-link": moto["year-link"],
                "category-link":category_link,
                "category":category_text
            }
            print(json.dumps(item)+",")
            constructeursCategoryMotosLinks.append(item)

"""
function: get Product Names by Motocyle and Category
List : Constructeur, Type, Moto , Year, Link, Category, Porduit, Produit-link
"""
def getProductData():
    global constructeursCategoryMotosDataLinks
    jsonfile = open("data/dataCategoryMoto.json", "r", encoding="utf-8")
    categoryMotodata = json.load(jsonfile)  # Read Data
    for moto in categoryMotodata:
        try:
            count_pages = get_pages_number(mainWebsite+moto["category-link"]) + 1
            #print(count_pages)
            for count in range(1, count_pages):
                print("--------- " + str(mainWebsite+moto["category-link"] + "&p=" + str(count)) + '-----------')
                page = requests.get(mainWebsite+moto["category-link"] + "&p=" + str(count))
                soup = BeautifulSoup(page.text, "html.parser")
                tab = soup.find("div",{"class":"js-es-products js-block-product"})
                products = tab.select('.product-single.js-product-single.product-single--with-hover')
                for product in products:
                    product_link = (product.find("a")["href"])
                    product_text = (product.select(".product-single__infos__title")[0].text.strip())
                    item = {
                        "constructeur":moto["constructeur"],
                        "type":moto["type"],
                        "link-moto":moto["link-moto"],
                        "moto":moto["moto"],
                        "year":moto["year"],
                        "year-link":moto["year-link"],
                        "category-link":moto["category-link"],
                        "category":moto["category"],
                        "product-link":product_link,
                        "product":product_text
                    }
                    #print(json.dumps(item))
                    constructeursCategoryMotosDataLinks.append(item)
        except  Exception as e :
            print(e)
        #print(mainWebsite+moto["category-link"])
        #print(get_pages_number(mainWebsite+moto["category-link"]))
        #products = get_products_names(mainWebsite+moto["category-link"])
        #req = requests.get(mainWebsite+moto["category-link"])
        #soup = BeautifulSoup(req.text, "html.parser")

print("Fetching links...")
getContrsucteurLinks()
print(constructeursLinks)
print("Links fetched!!")
print("Fetching types ...")
getConstructeurTypes()
print(json.dumps(constructeursTypesLinks))
print("Types fetched!")
print("Fetching Motos ...")
getMotosbyType()
with open("data/dataMotoType.json", "w", encoding="utf-8") as jsonfile:
    json.dump(constructeursMotosTypesLinks, jsonfile, ensure_ascii=False)
print(json.dumps(constructeursMotosTypesLinks))
print("Motos Fetched!!")
print("Fetching Years ...")
getMotosByYear()
print("-------")
print(json.dumps(constructeursYearsMotosTypesLinks))
print("Years Fetched!!")
with open("data/dataMotoTypeYear.json", "w", encoding="utf-8") as jsonfile:
    json.dump(constructeursYearsMotosTypesLinks, jsonfile, ensure_ascii=False)
print("Fetching Categories...")
getCategoryMoto()
with open("data/dataCategoryMoto.json", "w", encoding="utf-8") as jsonfile:
    json.dump(constructeursCategoryMotosLinks, jsonfile, ensure_ascii=False)
getProductData()
print("Categories Fetched!!")






