import argparse
import datetime
from pprint import pprint
import time


from dataset import Dataset


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', type=lambda s: datetime.datetime.strptime(s, '%Y/%m/%d-%H:%M:%S'), help="Datetime of departure for query in format YYYY/MM/DD-HH:MM:SS")
parser.add_argument('-from', '--from_city', type=str, help="Start city in query")
parser.add_argument('-to', '--to_city', type=str, help="Destination city in query")

args = parser.parse_args()

dataset = Dataset(name = 'upa')

if args.time:
    startDate = args.time.isoformat()

if args.from_city:
    srcCity = args.from_city

if args.to_city:
    dstCity = args.to_city

#Checks if cities and datetime are inserted
if (not args.time) or (not args.from_city):
    print("Error Missing or location of datetime detected!")
    exit(1)


#Tested on  >> python3 lookup.py -t 2021/12/31-00:00:00 -from "Praha hl. n." -to "Čadca"

if args.to_city is not None:
    cursor_results = dataset.db.CZPTTCISMessages.find(
        { '$and' : [
        { '$and' : [{"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.StartDateTime" : {'$lte': startDate}} , {"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.EndDateTime" : {'$gte': startDate}}  ]},
        { "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.Location.PrimaryLocationName" : srcCity , "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.TrainActivity.TrainActivityType" : '0001'} , 
        { "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.Location.PrimaryLocationName" : dstCity , "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.TrainActivity.TrainActivityType" : '0001'} 
        ]}
        )
else:
    cursor_results = dataset.db.CZPTTCISMessages.find(
        { '$and' : [
        { '$and' : [{"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.StartDateTime" : {'$lte': startDate}} , {"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.EndDateTime" : {'$gte': startDate}}  ]},
        { "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.Location.PrimaryLocationName" : srcCity , "CZPTTCISMessage.CZPTTInformation.CZPTTLocation.TrainActivity.TrainActivityType" : '0001'}
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
    # print(start_day)
    # print(core0, core1)
    
    
    looking_date = datetime.datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
    bit_map = list(res["CZPTTCISMessage"]["CZPTTInformation"]["PlannedCalendar"]["BitmapDays"])
    valid = bit_map[(looking_date - start_day).days]
    if(valid == '0'):
        final_results.remove(res)
    # print(f"Correct valid: {valid}")
   
    canceled_results = dataset.db.CZCanceledPTTMessages.find(
        { '$and' : [
        { '$and' : [{"CZCanceledPTTMessage.PlannedCalendar.ValidityPeriod.StartDateTime" : {'$lte': startDate}} , {"CZCanceledPTTMessage.PlannedCalendar.ValidityPeriod.EndDateTime" : {'$gte': startDate}}  ]}, #4.1 without Bitmap check
        { '$or' : [{"CZCanceledPTTMessage.PlannedTransportIdentifiers.Core" : core0 } , {"CZPTTCISMessage.Identifiers.PlannedTransportIdentifiers.Core" : core1 }]} , 
        ]}
        )
    c_results = list(canceled_results)
    # print(f"    Canceled records found: {len(c_results)}")


    for c in c_results:
        c_core0 = c["CZCanceledPTTMessage"]["PlannedTransportIdentifiers"][0]["Core"]
        c_core1 = c["CZCanceledPTTMessage"]["PlannedTransportIdentifiers"][1]["Core"]
        c_start_day = datetime.datetime.strptime(c["CZCanceledPTTMessage"]["PlannedCalendar"]["ValidityPeriod"]["StartDateTime"], '%Y-%m-%dT%H:%M:%S')
        if res in final_results:
            final_results.remove(res)
        if c_core0 != core0 or c_core1 != core1:
            # print(f"    {c_core0},{c_core1}")
            c_bit_map = list(c["CZCanceledPTTMessage"]["PlannedCalendar"]["BitmapDays"])
            c_valid = bit_map[(looking_date - c_start_day).days]
            # print(f"    Canceled valid: {c_valid}")

            if len(c_results) > 0:
                updated_results = dataset.db.CZUpdatedPTTMessages.find(
                { '$and' : [
                { '$and' : [{"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.StartDateTime" : {'$lte': startDate}} , {"CZPTTCISMessage.CZPTTInformation.PlannedCalendar.ValidityPeriod.EndDateTime" : {'$gte': startDate}}  ]},
                { "$and" : [{"CZPTTCISMessage.Identifiers.PlannedTransportIdentifiers.Core" : c_core0 } , {"CZPTTCISMessage.Identifiers.PlannedTransportIdentifiers.Core" : c_core1}]},
                ]}
                )
                u_results = list(updated_results)
                # print(f"        Updated records found: {len(u_results)}")
                for u in u_results:
                    final_results.append(u)
                    u_core0 = u["CZPTTCISMessage"]["Identifiers"]["PlannedTransportIdentifiers"][0]["Core"]
                    u_core1 = u["CZPTTCISMessage"]["Identifiers"]["PlannedTransportIdentifiers"][1]["Core"]
                    u_start_day = datetime.datetime.strptime(u["CZPTTCISMessage"]["CZPTTInformation"]["PlannedCalendar"]["ValidityPeriod"]["StartDateTime"], '%Y-%m-%dT%H:%M:%S')
                    # print(f"        {u_core0},{u_core1}")
                    u_bit_map = list(u["CZPTTCISMessage"]["CZPTTInformation"]["PlannedCalendar"]["BitmapDays"])
                    u_valid = u_bit_map[(looking_date - u_start_day).days]
                    # print(f"        Correct valid: {u_valid}")
    
    # print(end_day)
    # print("==============================================================================")



print(f"Corect records found: {len(list(final_results))}")
print("--------------------------------------------------------------------------------------------")

#4.4 Printing list of stops during transport 
for res in final_results:

    foundSrc = False
    foundDst = False
    stopCounter = 0;

    #Prints file identifier at first
    textResult = '\n' + res['CZPTTCISMessage']['Identifiers']['PlannedTransportIdentifiers'][0]['ObjectType']+'_'
    textResult = textResult + res['CZPTTCISMessage']['Identifiers']['PlannedTransportIdentifiers'][0]['Company']+'_'
    textResult = textResult + res['CZPTTCISMessage']['Identifiers']['PlannedTransportIdentifiers'][0]['Core'] + '\n'

    for timeInfo in  res['CZPTTCISMessage']['CZPTTInformation']['CZPTTLocation']:
        actCity = timeInfo['Location']['PrimaryLocationName']

        if actCity == srcCity:
            foundSrc = True

        
        if foundSrc and not(foundDst):

          
            underline = len(actCity)*'='

            
            timings = timeInfo['TimingAtLocation']['Timing']
            textResult =  textResult +'\n'+ actCity + '\n' + underline + '\n'
            if type(timings) == list:
                for timing in timings:

                    msg = '['
                    if timing['@TimingQualifierCode'] == 'ALA':
                        msg = msg + 'ARRIVAL]: '
                    elif timing['@TimingQualifierCode'] == 'ALD':
                        msg = msg + 'DEPARTURE]: '
                    else:
                        msg = msg + ' ]: '
                   
                    textResult = textResult + msg + str(timing['Time'][0:5])+'\n'

                    
            else:

                msg = '['
                if timings['@TimingQualifierCode'] == 'ALA':
                    msg = msg + 'ARRIVAL]: '
                elif timings['@TimingQualifierCode'] == 'ALD':
                    msg = msg + 'DEPARTURE]: '
                else:
                    msg = msg + ' ]: '

                textResult = textResult + msg + str(timings['Time'])[0:5]+'\n'


            stopCounter = stopCounter +1
            if args.to_city:
                if actCity == dstCity:
                    foundDst = True

    if args.to_city:
        if foundDst:
            print(textResult)
            print("#########################\n### End of train line ###\n#########################\n\n")

    else:
        #Elimintates printing found queries containg only start stop (ending line)
        if stopCounter > 1:
            print(textResult)
            print("#########################\n### End of train line ###\n#########################\n\n")
