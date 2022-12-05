import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--base', type=str, help="Base page of eshop", default="https://www.bodyworld.eu")
parser.add_argument('-p', '--product', type=str, help="page with products in eshop", default="https://www.bodyworld.eu/cz/en/performance-c523")
parser.add_argument('-s', '--save', action="store_true", help="Save list of links as file")

args = parser.parse_args()

base_url = args.base
request = requests.get(args.product)
soup = BeautifulSoup(request.text, 'html.parser')

#get number of pages
pages = soup.find_all("li",{"class":"c-pager__item"})
number_of_pages = pages[-1:][0].text

#get all links for each page
product_links = []
for iterator in range(1,int(number_of_pages) + 1):
    request = requests.get(f"{args.product}?page={iterator}")
    soup = BeautifulSoup(request.text, 'html.parser')

    product_list = soup.find_all("div",{"class":"c-product-card c-product-card--alt"})

    for product in product_list:
        link = product.find("a",{"class":"c-product-card__img"}).get('href')
        if args.save:
            product_links.append(base_url + link)
        else:
            print(base_url + link)

#write links to .txt file or print to stdout
if args.save:
    with open(r'./links.txt', 'w') as fp:
        for item in product_links:
            fp.write("%s\n" % item)
