import threading
import json
import os

import xml.etree.ElementTree as ET

import xmltodict
import json

from pymongo import MongoClient

class Dataset:

    def __init__(self, name, workers=8):
        """Sets up the connection between remote db and local client.
        Args:
            name (str): mongo database name
        """
        self.name = name
        self.connection_string = "mongodb://ubuntu:klat8klat@ec2-54-87-72-203.compute-1.amazonaws.com:27017/{}?authSource=admin".format(self.name)
        self.workers = workers
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.name]

    def clear(self, collection_name=None):
        """Clears one collection from remote db if collection_name is specified, otherwise wipes the entire database. 
        Args:
            collection_name (str, optional): name of the collection to be cleared. Defaults to None.
        """
        if collection_name is not None:
            self.db[collection_name].drop()
        else:
            self.client.drop_database(self.name)
            self.db = self.client[self.name]

    def insert(self, names, collection_name, update=False):
        """Downloads the data from url specified in params proces them to corect format
        and inserts them into the db.
        Args:
            url (str): link for downloading data
            collection_name (str): name under which collection will be stored in db
            update (bool): if True, updates the existing table instead of only downloading new one
        """
        
                
        threads = []
        
        lists = self.chunks(names, int(len(names)/self.workers) + 1)
        for idx, names in enumerate(lists):
            threads.append(ProcessingThread(conn_string = self.connection_string,
                                            db_name=self.name,
                                            collection_name = collection_name,
                                            idx = idx,
                                            data_names = names,
                                            update = update))
            threads[idx].start()

        for t in threads:
            t.join()
        
        print(f"Done.")

    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst.
        Args:
            lst (list): list of elements
            n: (int) size of chunks
        Returns:
            list of lists
        """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

class ProcessingThread(threading.Thread):

    def __init__(self, conn_string, db_name, collection_name, idx, data_names, 
                 update=False):
        """Thread used for parallel processing & uploading of collections.
        Args:
            conn_string (str): connection string for MongoClient
            TODO
        """
        threading.Thread.__init__(self)
        self.client = MongoClient(conn_string)
        self.collection_name = collection_name
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.idx = idx
        self.data_names = data_names
        self.update = update


    def run(self):

        for name in self.data_names:
            name = 'data/' + name
            print(f"Processing {name}... ")
            
            with open(name) as xml_file:
                data_dict = xmltodict.parse(xml_file.read())

            json_data = json.dumps(data_dict)
            file_data = json.loads(json_data)

            if self.update:
                core0 = file_data["CZPTTCISMessage"]["Identifiers"]["PlannedTransportIdentifiers"][0]["Core"]
                core1 = file_data["CZPTTCISMessage"]["Identifiers"]["PlannedTransportIdentifiers"][1]["Core"]
                massage = self.collection.find_one({"$or":[{"CZPTTCISMessage.Identifiers.PlannedTransportIdentifiers.Core":core0},{"CZPTTCISMessage.Identifiers.PlannedTransportIdentifiers.Core":core1}]})
                if massage is not None:
                    self.collection.delete_one(massage)


                self.collection.insert_one(file_data)
            os.remove(name)

        print(f"Worker {self.idx} has finished uploading {self.name}")