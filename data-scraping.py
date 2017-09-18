import urllib
from bs4 import BeautifulSoup
from retrying import retry
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time
import csv

class Product:
    
    def __init__(self, sku="",description="",image_url="",download_link="",date_modified=""):
        self.sku = ""
        self.description = ""
        self.image_url = ""
        self.download_link = ""
        self.date_modified = ""

def find_sku(ele):
    try:
        spans = ele.find_elements_by_tag_name("span")
        for span in spans:
            if "textTitleWhite" not in span.get_attribute("class"):
                return span.text
    except Exception:
        return ""

def find_description(ele):
    try:
        strong = ele.find_element_by_tag_name("strong")
        return strong.text
    except Exception:
        return ""

def find_image(ele):
    try:
        spans = ele.find_element_by_tag_name("img")
        return spans.get_attribute("src")
    except Exception:
        return ""

def find_download_link(ele):
    try:
        spans = ele.find_element_by_tag_name("a")
        return spans.get_attribute("href")
    except Exception:
        return ""

def find_last_modified(ele):
    try:
        strong = ele.find_elements_by_class_name("smaller")
        return strong[1].text
    except Exception:
        return ""
def travsers_links(link):
    linkUrl = baseUrl+link['href']
    linkSoup = driver.get(linkUrl)
    element = True

    while element==True:
        try:
            button = driver.find_element_by_id('showMore')
            time.sleep(10)
            button.click()
        except Exception:
            break
    #linkPage = BeautifulSoup(page = urllib.request.urlopen(baseUrl+linkUrl))
    products_on_page = driver.find_elements_by_class_name("productContainer")
    for prod in products_on_page:
        skuContainer = prod.find_element_by_class_name("prodNrBar")
        sku = find_sku(skuContainer)
        descriptionContainer = prod.find_element_by_class_name("prodText")
        description = find_description(descriptionContainer)
        modified = find_last_modified(descriptionContainer)
        downloadContainer = prod.find_element_by_class_name("fileDownload")
        download = find_download_link(downloadContainer)
        imageContainer = prod.find_element_by_class_name("prodImageContainer")
        image = find_image(imageContainer)
        newProduct = Product()
        newProduct.description = description
        newProduct.sku = sku
        newProduct.date_modified = modified
        newProduct.image_url = image
        newProduct.download_link = download
        match = [prod for prod in products if prod.sku == sku]
        if len(match)<1:
            products.append(newProduct)

    return products


quote_page = 'https://atsspec.net/bim/sloan'
baseUrl = 'https://atsspec.net'
page = urllib.request.urlopen(quote_page)

soup = BeautifulSoup(page, 'html.parser')
menu = soup.find('div',attrs={'class':'sideMenu'})
products = []
driver = webdriver.Chrome()
links = menu.findAll('a', attrs={'class':None})
for link in links:
    products = travsers_links(link)
    time.sleep(1)

driver.quit()
with open('./csvfile.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Sku","Description","Image_Url","Dowload_Link","Last_Modified"])
    for product in products:
        line =[product.sku,product.description,product.image_url,product.download_link,product.date_modified]
        writer.writerow(line)


