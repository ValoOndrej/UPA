import requests
import argparse
import datetime
from pprint import pprint
from bs4 import BeautifulSoup

from dataset import Dataset


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', nargs='+', type=str, help="url do download from", default = 'https://portal.cisjr.cz/pub/draha/celostatni/szdc/2022/')
parser.add_argument('-d', '--download', action="store_true" , help="Clears the database and downloads oriinal datasets")
parser.add_argument('-up', '--update', action="store_true" , help="update database with corections of chosen routs")
parser.add_argument('-cup', '--cancel_update', action="store_true" , help="removed canceld routs and updates database with corections of chosen routs")
parser.add_argument('-c', '--clear', action="store_true", help="Clears the database")
parser.add_argument('-t', '--time', type=lambda s: datetime.datetime.strptime(s, '%Y/%m/%d-%H:%M:%S'), help="Datetime of departure for query in format YYYY/MM/DD-HH:MM:SS")
parser.add_argument('-from', '--from_city', type=str, help="Start city in query")
parser.add_argument('-to', '--to_city', type=str, help="Destination city in query")


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
                u = requests.compat.urljoin(url, l.get('href'))
                cancel = 'cancel' in u
                if cancel:
                    dataset.download_and_insert(u, update=True, dont_remove=False)
                else:
                    dataset.download_and_insert(u, update=True)

if args.time:
    startDate = args.time.isoformat()
    print(startDate)

if args.from_city:
    srcCity = args.from_city
if args.to_city:
    dstCity = args.to_city

#Checks if dates are inserted, and their correct order (start<end)
if (not args.time) or (not args.from_city) or (not args.to_city):
    print("Error Missing or location ot  datetime detected!")
    exit(1)

#Tested on  >> python3 download.py -t 03/09/2022-00:00:00 -from Břeclav -to "Bad Schandau"
results = dataset.db.CZPTTCISMessages.find(
    {'$and':[
    { "CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.StartDateTime" : {'$gte': startDate} }, #4.1 without Bitmap check
    { "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.Location.PrimaryLocationName" : srcCity , "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.TrainActivity.TrainActivityType" : '0001'} , #4.2 with stop check (0001 flag)
    { "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.Location.PrimaryLocationName" : dstCity , "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.TrainActivity.TrainActivityType" : '0001'} #4.3 with stop check (0001 flag)
    ]}
    )


print("Records found: "+str(results.count()))


#4.4 Printing list of stops during transport 
for res in results:
   
    for timeInfo in  res['CZPTTCISMessage']['CZPTTInformation']['CZPTTLocation']:
        print(timeInfo['Location']['PrimaryLocationName'])
        timings = timeInfo['TimingAtLocation']['Timing']

        if type(timings) == list:
           for timing in timings:
                print("TIME: " + str(timing['Time']) + " OFFSET "+str(timing['Offset']))
                #pprint(timing) # Not formatted data print
        else:
            print("TIME: " + str(timings['Time']) + " OFFSET "+str(timings['Offset']))
            #pprint(timings)
            
        print("-------------")

    print("===================================\n")
