import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import json
import xmltodict
from datetime import datetime, timedelta
import time
import base64
import requests
import traceback

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import json


def response_parser(response, present='dict'):
    """ Convert Hikvision results
    """
    if isinstance(response, (list,)):
        result = "".join(response)
    else:
        result = response.text

    if present == 'dict':
        if isinstance(response, (list,)):
            events = []
            for event in response:
                e = json.loads(json.dumps(xmltodict.parse(event)))
                events.append(e)
            return events
        return json.loads(json.dumps(xmltodict.parse(result)))
    else:
        return result


class Client:

    def __init__(self, host, login=None, password=None, timeout=3, isapi_prefix='ISAPI'):
        self.host = host
        self.login = login
        self.password = password
        self.timeout = float(timeout)
        self.isapi_prefix = isapi_prefix
        self.req = self._check_session()
        self.count_events = 1

    def _check_session(self):
        """Check the connection with device
         :return request.session() object
        """
        full_url = urljoin(self.host, self.isapi_prefix + '/System/status')
        session = requests.session()
        session.auth = HTTPBasicAuth(self.login, self.password)
        response = session.get(full_url)
        if response.status_code == 401:
            session.auth = HTTPDigestAuth(self.login, self.password)
            response = session.get(full_url)
        response.raise_for_status()
        return session

    def getNumberPlates(self,date_time):
        print("Getting Data From -> " + date_time)
        payload = "<AfterTime><picTime>%s</picTime></AfterTime>".format("0")
        payload = "<AfterTime><picTime>"+date_time+"</picTime></AfterTime>"
        response = self.req.request(method='post', url= self.host +"/ISAPI/Traffic/channels/1/vehicleDetect/plates", timeout=self.timeout, stream=True, data=payload)
        return response

CameraIP = "10.10.36.1"

cam = Client("http://"+CameraIP, 'admin', 'TEKTRON@123')



now = datetime.now() - timedelta(days = 1)
date_time = now.strftime("%Y%m%dT%H%M%S")
print(date_time)
lastDetectedVehicleTime = ""
for i in range(0,100):
    print("Run -> " + str(i))
    res = cam.getNumberPlates(date_time)
    print(res.text)
    if(res.status_code == 200):
        json_resp = response_parser(res)
        print(json_resp)
        plates = []
        try:
            print(json_resp["Plates"]["Plate"])
            if(isinstance(json_resp["Plates"]["Plate"], list)):
                print("Multiple Plates")
                plates = json_resp["Plates"]["Plate"]
            else:
                plates.append(json_resp["Plates"]["Plate"])
                print("Single Plates")
        except KeyError:
            print("No Plates")
        except:
            traceback.print_exc()
        if(len(plates) >= 1):
            i = len(plates)-1
            picName = plates[i]["picName"]
            if(picName != lastDetectedVehicleTime):
                lastDetectedVehicleTime = picName
                print("New Vehicle Detected")
                plateNumberx = plates[i]["plateNumber"]
                captureTime = plates[i]["captureTime"]
                country = plates[i]["country"]
                laneNo = plates[i]["laneNo"]
                direction = plates[i]["direction"]
                imageurl = "http://"+ CameraIP + "/doc/ui/images/plate/"+ picName+ ".jpg"
                print(imageurl)
                Base64Image = base64.b64encode(requests.get(imageurl).content)
                if(country == "KSA"):
                    plateType = "1"
                    plateNumber = plateNumberx[:-3]
                    plateEnLetter1 = plateNumberx[-3]
                    plateEnLetter2 = plateNumberx[-2]
                    plateEnLetter3 = plateNumberx[-1]
                    CameraIPx = CameraIP
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
                    Resp = requests.post("http://localhost/Kashef/API/Kashef/VehicleLogs", json = BodyParams,timeout=5)
                    print(Resp.text)
    now = datetime.now() - timedelta(days = 1) 
    date_time = now.strftime("%Y%m%dT%H%M%S")
    time.sleep(2)
exit()