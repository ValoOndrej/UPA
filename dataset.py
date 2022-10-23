import pandas as pd
import numpy as np
import json
import os
import requests
import zipfile
import xml.etree.ElementTree as ET

import xmltodict
import json
import pprint

from bs4 import BeautifulSoup
from pymongo import MongoClient

class Dataset:

    def __init__(self, name, workers=1):
        """Sets up the connection between remote db and local client.
        Args:
            name (str): mongo database name
        """
        self.name = name
        self.connection_string = "mongodb://ubuntu:klat8klat@ec2-54-87-72-203.compute-1.amazonaws.com:27017/{}?authSource=admin".format(self.name)
        self.workers = workers
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.name]


    def download_and_process(self, url):
        """Downloads the data from url specified in params proces them to corect format
        and inserts them into the db.
        Args:
            url (str): link for downloading data
        """
        print(f"Processing {url}... ")

        collection_name = 'CZPTTCISMessages'

        collection = self.db[collection_name]
            
        req = requests.get(url)
        filename = url.split('/')[-1]
        with open(filename,'wb') as output_file:
            output_file.write(req.content)
        print('Downloaded data from', url)

        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall('data/')
            for name in zip_ref.namelist():
                name = 'data/' + name
                print('opening ' + name)
                
                with open(name) as xml_file:
                    data_dict = xmltodict.parse(xml_file.read())

                json_data = json.dumps(data_dict)

                with open(name[:-4] + '.json', "w") as json_file:
                    json_file.write(json_data)

                with open(name[:-4] + '.json') as file:
                    file_data = json.load(file)

                if isinstance(file_data, list):
                    collection.insert_many(file_data) 
                else:
                    collection.insert_one(file_data)
                    
                os.remove(name)
                os.remove(name[:-4] + '.json')
                print('deleting ' + name)
                print('===================================================')
        os.remove(filename)
        