import requests
import argparse

from bs4 import BeautifulSoup

from dataset import Dataset

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', nargs='+', type=str, help="url do download from", default = 'https://portal.cisjr.cz/pub/draha/celostatni/szdc/2022/')
parser.add_argument('-d', '--download', action="store_true" , help="Clears the database and downloads datasets")

args = parser.parse_args()

reqs = requests.get(args.url)

soup = BeautifulSoup(reqs.text, 'html.parser')

dataset = Dataset(name = 'upa')

if args.download:
    for link in soup.find_all('a'):
        url = requests.compat.urljoin(args.url, link.get('href'))
        downloadable = 'zip' in url
        if(downloadable):
            dataset.download_and_process(url)
            

