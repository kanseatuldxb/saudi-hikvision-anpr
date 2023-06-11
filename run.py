import requests
from requests.auth import HTTPDigestAuth
import json
import xmltodict
from datetime import datetime, timedelta
import time
import base64
import requests
import traceback

def sendData(platetype,platenumber,platechar1,platechar2,platechar3):
    print(platetype,platenumber,platechar1,platechar2,platechar3)
    pass

#CameraIP = "http://10.10.36.2"
CameraIP = "http://192.168.10.81"
CameraUser = "admin"
CameraPass = "TEKTRON@123"
CameraId = "10.10.36.2"
ServerURL = "http://10.10.24.224/Kashef/API/Kashef/VehicleLogs"


now = datetime.now() - timedelta(days = 1)
date_time = now.strftime("%Y%m%dT%H%M%S")
print(date_time)
rtext = '''<?xml version="1.0" encoding="UTF-8"?>
<Plates version="2.0" xmlns="http://www.std-cgi.com/ver20/XMLSchema">
    <Plate>
    <captureTime>20340109T094130+0400</captureTime>
    <plateNumber>A 39837</plateNumber>
    <picName>203401090941300600</picName>
    <country>NON</country>
    <laneNo>1</laneNo>
    <direction>reverse</direction>
    <matchingResult>otherlist</matchingResult>
    </Plate>
</Plates>'''


data_dict = xmltodict.parse(rtext)
plates = []
try:
    print(data_dict["Plates"]["Plate"])
    if(isinstance(data_dict["Plates"]["Plate"], list)):
        print("Multiple Plates")
        plates = data_dict["Plates"]["Plate"]
    else:
        plates.append(data_dict["Plates"]["Plate"])
        print("Single Plates")
except KeyError:
    print("No Plates")
except:
    traceback.print_exc()

print(plates,type(plates))





lastDetectedVehicleTime = ""
for i in range(0,100):
    print("Run -> " + str(i))
    try:
        #print(date_time)
        url = CameraIP + '/ISAPI/Traffic/channels/1/vehicleDetect/plates/'
        data = "<AfterTime><picTime>"+date_time+"</picTime></AfterTime>"
        r=requests.get(url, data =data,auth=HTTPDigestAuth(CameraUser, CameraPass),timeout=2)
        print(r.status_code,type(r.status_code))
        if(r.status_code == 200):
            data_dict = xmltodict.parse(r.text)
            print(data_dict)
            intx = 0
            #print(len(data_dict["Plates"]["Plate"]))
            try:
                print(data_dict["Plates"]["Plate"])
                intx = isinstance(len(data_dict["Plates"]["Plate"]), int)
            except KeyError:
                print("No Plates")
            except:
                traceback.print_exc()

            if(intx):
                i = len(data_dict["Plates"]["Plate"])-1
                picName = data_dict["Plates"]["Plate"][i]["picName"]
                if(picName != lastDetectedVehicleTime):
                    lastDetectedVehicleTime = picName
                    print("New Vehicle Detected")
                    plateNumberx = data_dict["Plates"]["Plate"][i]["plateNumber"]
                    captureTime = data_dict["Plates"]["Plate"][i]["captureTime"]
                    country = data_dict["Plates"]["Plate"][i]["country"]
                    laneNo = data_dict["Plates"]["Plate"][i]["laneNo"]
                    direction = data_dict["Plates"]["Plate"][i]["direction"]
                    imageurl = CameraIP + "/doc/ui/images/plate/"+ picName+ ".jpg"
                    print(imageurl)
                    Base64Image = base64.b64encode(requests.get(imageurl).content)
                    
                    plateType = "1"
                    plateNumber = plateNumberx[:-3]
                    plateEnLetter1 = plateNumberx[-3]
                    plateEnLetter2 = plateNumberx[-2]
                    plateEnLetter3 = plateNumberx[-1]
                    CameraIPx = CameraId
                    CaptureTimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Country = "Saudi Arabia"
                    PhotoB64 = Base64Image.decode('UTF-8')
                    BodyParams = {
                                "plateType":"1", 
                                "plateNumber":plateNumber,
                                "plateEnLetter1":plateEnLetter1,
                                "plateEnLetter2":plateEnLetter2,
                                "plateEnLetter3":plateEnLetter3,
                                "CameraIP":CameraIPx,
                                "CaptureTimeStamp":CaptureTimeStamp,
                                "Country":Country,
                                "PhotoB64":PhotoB64,
                            }
                    Resp = requests.post(ServerURL, json = BodyParams,timeout=5)
                    print(Resp.text)
                    
            now = datetime.now() - timedelta(days = 1) 
            date_time = now.strftime("%Y%m%dT%H%M%S")
            time.sleep(2)
    except:
        exit()