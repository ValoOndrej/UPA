import requests
import argparse
import zipfile
import threading
import os
import gzip
from pprint import pprint
from bs4 import BeautifulSoup

from dataset import Dataset

class ProcessingThread(threading.Thread):

    def __init__(self, url, idx, names, cancel_or_not, link):
        """Thread used for parallel processing & dowloading of data.
        Args:
            url (url): 
            idx (int): index of thread
            names (list) Names of downloadet data files
            cancel_or_not
            link
        """
        threading.Thread.__init__(self)
        self.names = names
        self.url = url
        self.idx = idx
        self.cancel_or_not = cancel_or_not
        self.link = link
 
    def run(self):
        for l in self.link:
            u = requests.compat.urljoin(self.url, l.get('href'))
            req = requests.get(u)
            filename =  'data/' + u.split('/')[-1]
            with open(filename,'wb') as output_file:
                output_file.write(req.content)
            
            with gzip.open(filename, 'r') as f:
                with open(filename[:-4],'wb') as output_file:
                    output_file.write(f.read())
            self.names.append(filename[5:-4])
            os.remove(filename)

        print(f"Worker {self.idx} has finished downloading {self.name}")



def genarate_chunks(lst, n):
        """Yield successive n-sized chunks from lst.
        Args:
            lst (list): list of elements
            n: (int) size of chunks
        Returns:
            list of lists
        """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]


def get_list_of_names_from_zip(url):
    print(f"Processing {url}... ")
    req = requests.get(url)
    filename =  'data/' + url.split('/')[-1]
    with open(filename,'wb') as output_file:
        output_file.write(req.content)
    names = []
    if zipfile.is_zipfile(filename):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall('data/')
        names = zip_ref.namelist()
        os.remove(filename)
    return names

def get_list_of_names_from_gzips(url, cancel_or_not=True):
    print(f"Processing {url}... ")
    link_reqs = requests.get(url)
    link_soup = BeautifulSoup(link_reqs.text, 'html.parser')
    if cancel_or_not:
        links = link_soup.find_all('a', href=lambda href: href and "cancel" in href)
    else:
        links = link_soup.find_all('a', href=lambda href: href and "cancel" not in href)[1:]

    lists = genarate_chunks(links, int(len(links)/8) + 1)
    names = []
    threads = []
    for idx, link in enumerate(lists):
        threads.append(ProcessingThread(url = url,
                                        link = link,
                                        idx = idx,
                                        names = names,
                                        cancel_or_not = cancel_or_not))
        threads[idx].start()

        for t in threads:
            t.join()

        
    return names



parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', nargs='+', type=str, help="url do download from", default = 'https://portal.cisjr.cz/pub/draha/celostatni/szdc/2022/')
parser.add_argument('-d', '--download', action="store_true" , help="Clears the database and downloads oriinal datasets")
parser.add_argument('-up', '--update', action="store_true" , help="update database with corections of chosen routs")
parser.add_argument('-cup', '--cancel_update', action="store_true" , help="download collections for canceld routs and uploads them to database ")
parser.add_argument('-c', '--clear', action="store_true", help="Clears the database")


args = parser.parse_args()

#loads and pareses all links in given link
reqs = requests.get(args.url)
soup = BeautifulSoup(reqs.text, 'html.parser')

dataset = Dataset(name = 'upa')

if args.clear:
    dataset.clear()
    print("Cleard all collections")

if args.download:
    for link in soup.find_all('a'):
        url = requests.compat.urljoin(args.url, link.get('href'))
        downloadable = 'GVD2022.zip' in url
        if downloadable:
            names = get_list_of_names_from_zip(url)
            dataset.insert(names, collection_name = 'CZPTTCISMessages')

if args.update:
    for link in soup.find_all('a'):
        url = requests.compat.urljoin(args.url, link.get('href'))
        downloadable = 'GVD2022-oprava_poznamek_KJR_vybranych_tras20220126.zip' in url
        if downloadable:
            names = get_list_of_names_from_zip(url)
            dataset.insert(names, collection_name = 'CZPTTCISMessages', update=True)
            
if args.cancel_update:
    for link in soup.find_all('a')[1:]:
        url = requests.compat.urljoin(args.url, link.get('href'))
        downloadable = 'zip' not in url
        parent = 'Parent' not in url
        if downloadable and parent:
            canceled_names = get_list_of_names_from_gzips(url, cancel_or_not=True)
            dataset.insert(canceled_names, collection_name = 'CZCanceledPTTMessages')
            
            names = get_list_of_names_from_gzips(url, cancel_or_not=False)
            dataset.insert(names, collection_name = 'CZUpdatedPTTMessages')



