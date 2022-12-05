import requests
from bs4 import BeautifulSoup
from lxml import etree
import argparse
import sys
import pandas as pd
from signal import signal, SIGPIPE, SIG_DFL


parser = argparse.ArgumentParser()
parser.add_argument('-rf', '--read-file', action="store_true", help="read from file")
parser.add_argument('-s', '--save', action="store_true", help="Save list of links as file")

args = parser.parse_args()

if args.read_file:
    inf = open("urls.txt").readlines()
else:
    if not sys.stdin.isatty():
        inf = sys.stdin.readlines()
    else:
        inf = sys.stdin

inf = list(map(lambda s: s.strip(), inf))
names = []
prices = []
for link in inf:
    signal(SIGPIPE,SIG_DFL)
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
    if args.save:
        print(f"{link.strip()}\t{name}\t{price}")
        names.append(name)
        prices.append(price)
    else:
        print(f"{link.strip()}\t{name}\t{price}")

if args.save:
    df = pd.DataFrame({"url":inf, "name":names, "price":prices})
    df.to_csv("out.tsv", sep="\t", index=False)
    
