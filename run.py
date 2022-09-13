import requests
from requests.auth import HTTPDigestAuth
import json
import xmltodict
from datetime import datetime, timedelta
import time

def sendData(platetype,platenumber,platechar1,platechar2,platechar3):
    print(platetype,platenumber,platechar1,platechar2,platechar3)
    pass

now = datetime.now()
date_time = now.strftime("%Y%m%dT%H%M%S")
while True:
    #try:
    print(date_time)
    #url = 'http://192.168.10.69/ISAPI/Traffic/channels/1/vehicleDetect/plates/'
    url = 'http://192.168.8.59//ISAPI/Traffic/channels/1/vehicleDetect/plates/'
    data = "<AfterTime><picTime>"+date_time+"</picTime></AfterTime>"
    #data = "<AfterTime><picTime>20210912T212608</picTime></AfterTime>"
    r=requests.get(url, data =data,auth=HTTPDigestAuth('admin', 'Hik12345'))
    print(r.text)
    data_dict = xmltodict.parse(r.text)
    intx = 0
    try:
        intx = isinstance(len(data_dict["Plates"]["Plate"]), int)
    except:
        pass
    print(intx)
    if(intx):
        for i in range(len(data_dict["Plates"]["Plate"])):
            print(data_dict["Plates"]["Plate"][i]["plateNumber"])
            #sendData(platetype,platenumber,platechar1,platechar2,platechar3)
            date_time = data_dict["Plates"]["Plate"][i]["plateNumber"]
    else:
        now = datetime.now() - timedelta(seconds = 2)
        date_time = now.strftime("%Y%m%dT%H%M%S")
    time.sleep(2)
   
    
    
