import requests
from bs4 import BeautifulSoup
import argparse
from signal import signal, SIGPIPE, SIG_DFL

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
    signal(SIGPIPE,SIG_DFL)
    request = requests.get(f"{args.product}?page={iterator}")
    soup = BeautifulSoup(request.text, 'html.parser')

    links = soup.find_all("a",{"class":"c-product-card__img"})
    if args.save:
        for link in links: product_links.append(base_url + link.get('href'))
    else:
        for link in links: print(base_url+ link.get('href'))

#write links to .txt file or print to stdout
if args.save:
    with open(r'./links.txt', 'w') as fp:
        for item in product_links:
            fp.write("%s\n" % item)
