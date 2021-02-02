from bs4 import BeautifulSoup
import requests,re,csv
from timeit import default_timer as timer

urls = []
with open('categories.csv','r') as readfile :
    rd = csv.DictReader(readfile,delimiter ='|')
    for row in rd:
        if row['link'] is not '':
            urls.append(row['link'])
produtcsList = []

def get_pages_number(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"html.parser")
    try:
        pageCount = max(list(map(lambda x :int(x['data-page']),soup.find_all(attrs={'data-page':re.compile(r".*")}) ))) # Get Number of Pages
        return pageCount
    except Exception:
        return 1

def get_products_names():
    global produtcsList
    for url in urls:
        try:
            count_pages = get_pages_number(url)+1
            print(count_pages)
            for count  in range(1,count_pages):
                print("--------- " + str(url+"?p="+str(count)) + '-----------')
                page = requests.get(url+"?p="+str(count))
                soup = BeautifulSoup(page.text, "html.parser")
                products = soup.select('.product-single__infos__title')
                for product in products:
                    print(product.text.strip())
                    if product.text.strip() not in produtcsList:
                        produtcsList.append(product.text.strip())
                print(len(produtcsList))

        except  Exception  as e:
            print(e)

def get_products_marques():
    global produtcsList
    for url in urls:
        try:
            count_pages = get_pages_number(url)+1
            print(count_pages)
            for count  in range(1,count_pages):
                print("--------- " + str(url+"?p="+str(count)) + '-----------')
                page = requests.get(url+"?p="+str(count))
                soup = BeautifulSoup(page.text, "html.parser")
                products = soup.select('.block-product__item')
                print(len(products))
                for product in products:
                    try:
                        title = (product.find('div',attrs=({'class':'product-single__infos__title'})))
                        marque = (product.find('div',attrs=({'product-single__brand'})))
                        print(title)
                        print(marque)
                        title = title.text.strip()
                        marque = marque.text.strip()
                        if marque+" "+title not in produtcsList:
                            print(marque+" "+title)
                            produtcsList.append(marque+" "+title)
                    except Exception as e:
                        print(e)
                print(len(produtcsList))

        except  Exception  as e:
            print(e)

start = timer()
#print(get_products_names())
get_products_marques()
end = timer()
print(end-start)
with open('prductsNamesMarques.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(produtcsList)