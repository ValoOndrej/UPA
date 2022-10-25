import argparse
import datetime
from pprint import pprint

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
    print("Error Missing or location of datetime detected!")
    exit(1)


#Tested on  >> python3 lookup.py -t 2021/12/31-00:00:00 -from "Praha hl. n." -to "Čadca"
cursor_results = dataset.db.CZPTTCISMessages.find(
    { '$and' : [
    { '$and' : [{"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.StartDateTime" : {'$lte': startDate}} , {"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.EndDateTime" : {'$gte': startDate}}  ]}, #4.1 without Bitmap check
    { "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.Location.PrimaryLocationName" : srcCity , "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.TrainActivity.TrainActivityType" : '0001'} , #4.2 with stop check (0001 flag)
    { "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.Location.PrimaryLocationName" : dstCity , "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.TrainActivity.TrainActivityType" : '0001'} #4.3 with stop check (0001 flag)
    ]}
    )

results = list(cursor_results)
final_results = []

for res in results:
    final_results.append(res)
    core0 = res["CZPTTCISMessage"]["Identifiers"]["PlannedTransportIdentifiers"][0]["Core"]
    core1 = res["CZPTTCISMessage"]["Identifiers"]["PlannedTransportIdentifiers"][1]["Core"]
    start_day = datetime.datetime.strptime(res["CZPTTCISMessage"]["CZPTTInformation"]["PlannedCalendar"]["ValidityPeriod"]["StartDateTime"], '%Y-%m-%dT%H:%M:%S')
    end_day = datetime.datetime.strptime(res["CZPTTCISMessage"]["CZPTTInformation"]["PlannedCalendar"]["ValidityPeriod"]["EndDateTime"], '%Y-%m-%dT%H:%M:%S')
    
    looking_date = datetime.datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
    bit_map = list(res["CZPTTCISMessage"]["CZPTTInformation"]["PlannedCalendar"]["BitmapDays"])
    valid = bit_map[(looking_date - start_day).days]
    if(valid == '0'):
        final_results.remove(res)
   
    canceled_results = dataset.db.CZCanceledPTTMessages.find(
        { '$and' : [
        { '$and' : [{"CZCanceledPTTMessage.PlannedCalendar.ValidityPeriod.StartDateTime" : {'$lte': startDate}} , {"CZCanceledPTTMessage.PlannedCalendar.ValidityPeriod.EndDateTime" : {'$gte': startDate}}  ]}, #4.1 without Bitmap check
        { '$or' : [{"CZCanceledPTTMessage.PlannedTransportIdentifiers.Core" : core0 } , {"CZPTTCISMessage.Identifiers.PlannedTransportIdentifiers.Core" : core1 }]} , 
        ]}
        )
    c_results = list(canceled_results)


    for c in c_results:
        c_core0 = c["CZCanceledPTTMessage"]["PlannedTransportIdentifiers"][0]["Core"]
        c_core1 = c["CZCanceledPTTMessage"]["PlannedTransportIdentifiers"][1]["Core"]
        c_start_day = datetime.datetime.strptime(c["CZCanceledPTTMessage"]["PlannedCalendar"]["ValidityPeriod"]["StartDateTime"], '%Y-%m-%dT%H:%M:%S')
        if res in final_results:
            if c_core0 == core0 and c_core1 == core1:
                final_results.remove(res)
            else:
                final_results.remove(res)
                c_bit_map = list(c["CZCanceledPTTMessage"]["PlannedCalendar"]["BitmapDays"])
                c_valid = bit_map[(looking_date - c_start_day).days]

                if len(c_results) > 0:
                    updated_results = dataset.db.CZUpdatedPTTMessages.find(
                    { '$and' : [
                    { '$and' : [{"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.StartDateTime" : {'$lte': startDate}} , {"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.EndDateTime" : {'$gte': startDate}}  ]},
                    { "$and" : [{"CZPTTCISMessage.Identifiers.PlannedTransportIdentifiers.Core" : c_core0 } , {"CZPTTCISMessage.Identifiers.PlannedTransportIdentifiers.Core" : c_core1}]},
                    ]}
                    )
                    u_results = list(updated_results)
                    for u in u_results:
                        final_results.append(u)
                        u_core0 = u["CZPTTCISMessage"]["Identifiers"]["PlannedTransportIdentifiers"][0]["Core"]
                        u_core1 = u["CZPTTCISMessage"]["Identifiers"]["PlannedTransportIdentifiers"][1]["Core"]
                        u_start_day = datetime.datetime.strptime(u["CZPTTCISMessage"]["CZPTTInformation"]["PlannedCalendar"]["ValidityPeriod"]["StartDateTime"], '%Y-%m-%dT%H:%M:%S')
                        u_bit_map = list(u["CZPTTCISMessage"]["CZPTTInformation"]["PlannedCalendar"]["BitmapDays"])
                        u_valid = u_bit_map[(looking_date - u_start_day).days]




print(f"Corect records found: {len(list(final_results))}")
print("--------------------------------------------------------------------------------------------")
#4.4 Printing list of stops during transport 
for res in final_results:
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
