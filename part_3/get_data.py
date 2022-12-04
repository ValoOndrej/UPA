import requests
from bs4 import BeautifulSoup
from lxml import etree
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

args = parser.parse_args()

file = open(args.infile.name, "r")
text = file.readlines()

for link in text[0:100]:
    request = requests.get(link)
    soup = BeautifulSoup(request.text, 'html.parser')
    dom = etree.HTML(str(soup))
    
    #try to get name of pruduct if dos not exist set None
    try:
        name_xpath = '//*[@id="app"]/main/div/div[1]/div[1]/div[2]/h1/text()'
        name = "".join(dom.xpath(name_xpath)).strip()
    except:
        name = None

    #try to get discountedd price of product, if discount does not exist get normal price else None
    try:
        price_xpath = '//*[@id="app"]/main/div/div[1]/div[1]/div[3]/div[2]/div[1]/span'
        price = dom.xpath(price_xpath)[0].text
    except:
        try:
            price_xpath = '//*[@id="app"]/main/div/div[1]/div[1]/div[3]/div[1]/div/span'
            price = dom.xpath(price_xpath)[0].text
        except:
            price = None

    print(name, price)

    
