import requests
import argparse
import datetime
from pprint import pprint
from bs4 import BeautifulSoup

from dataset import Dataset


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', type=lambda s: datetime.datetime.strptime(s, '%Y/%m/%d-%H:%M:%S'), help="Datetime of departure for query in format YYYY/MM/DD-HH:MM:SS")
parser.add_argument('-from', '--from_city', type=str, help="Start city in query")
parser.add_argument('-to', '--to_city', type=str, help="Destination city in query")

args = parser.parse_args()

dataset = Dataset(name = 'upa')

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
