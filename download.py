import requests
import argparse

from bs4 import BeautifulSoup

from dataset import Dataset

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', nargs='+', type=str, help="url do download from", default = 'https://portal.cisjr.cz/pub/draha/celostatni/szdc/2022/')
parser.add_argument('-d', '--download', action="store_true" , help="Clears the database and downloads oriinal datasets")
parser.add_argument('-up', '--update', action="store_true" , help="update database with corections of chosen routs")
parser.add_argument('-cup', '--cancel_update', action="store_true" , help="removed canceld routs and updates database with corections of chosen routs")
parser.add_argument('-c', '--clear', action="store_true", help="Clears the database")

args = parser.parse_args()

#loads and pareses all links in given link
reqs = requests.get(args.url)
soup = BeautifulSoup(reqs.text, 'html.parser')

dataset = Dataset(name = 'upa')

if args.clear:
    dataset.clear()

if args.download:
    dataset.clear()
    for link in soup.find_all('a'):
        url = requests.compat.urljoin(args.url, link.get('href'))
        downloadable = 'GVD2022.zip' in url
        if downloadable:
            dataset.download_and_insert(url)

if args.update:
    for link in soup.find_all('a'):
        url = requests.compat.urljoin(args.url, link.get('href'))
        downloadable = 'GVD2022-oprava_poznamek_KJR_vybranych_tras20220126.zip' in url
        if downloadable:
            dataset.download_and_insert(url, update=True)
            
if args.cancel_update:
    for link in soup.find_all('a')[1:]:
        url = requests.compat.urljoin(args.url, link.get('href'))
        downloadable = 'zip' not in url
        parent = 'Parent' not in url
        if downloadable and parent:
            link_reqs = requests.get(url)
            link_soup = BeautifulSoup(link_reqs.text, 'html.parser')
            for l in link_soup.find_all('a')[1:]:
                print(l)
                u = requests.compat.urljoin(url, l.get('href'))
                cancel = 'cancel' in u
                if cancel:
                    dataset.download_and_insert(u, True, False)
                else:
                    dataset.download_and_insert(u, True)
