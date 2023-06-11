from flask import Flask, request
import xmltodict
import json
import requests
from datetime import datetime 
import sys
import os
import base64

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)
#sys.stdout = sys.stderr = open(os.devnull, 'w')
#sys.stdout = open('log.txt', 'w')

@app.route('/vehicle-alert', methods=['POST'])
def vehicle_alert():
    # f = request.files["anpr.xml"]
    f = request.files.get("anpr.xml")  # Use get() to avoid KeyError if the file is missing
    xml_data = f.read()
    #dict_data = xmljson.badgerfish.data(xml_data)
    dict_data = xmltodict.parse(xml_data)
    json_data = json.dumps(dict_data)
    json_data = json.loads(json_data)
    print(json_data)
    #try:
    licensePlatePicture_string = ""
    fx = request.files["licensePlatePicture.jpg"]
    licensePlatePicture_string = base64.b64encode(fx.read())
    PlateNumber = json_data["EventNotificationAlert"]["ANPR"]["licensePlate"]
    DeviceIPAddress = json_data["EventNotificationAlert"]["ipAddress"]
    DeviceName = json_data["EventNotificationAlert"]["channelName"]
    PlateConfidance = json_data["EventNotificationAlert"]["ANPR"]["confidenceLevel"]
    PlateCountry = json_data["EventNotificationAlert"]["ANPR"]["country"]
    PlateProvince = json_data["EventNotificationAlert"]["ANPR"]["area"]
    PlateNumber = json_data["EventNotificationAlert"]["ANPR"]["licensePlate"]
    PlateCategory = json_data["EventNotificationAlert"]["ANPR"]["category"]
    PlateColor = json_data["EventNotificationAlert"]["ANPR"]["plateColor"]
    PlateSize = json_data["EventNotificationAlert"]["ANPR"]["plateSize"]
    PlateType = json_data["EventNotificationAlert"]["ANPR"]["plateType"]
    Direction = json_data["EventNotificationAlert"]["ANPR"]["direction"]
    VehicleColor = json_data["EventNotificationAlert"]["ANPR"]["vehicleInfo"]["color"]
    VehicleType = json_data["EventNotificationAlert"]["ANPR"]["vehicleType"]
    EventTime = json_data["EventNotificationAlert"]["dateTime"]
    LibraryName = json_data["EventNotificationAlert"]["ANPR"]["vehicleListName"]
    print(PlateNumber,DeviceIPAddress,DeviceName,PlateConfidance,PlateCountry,PlateProvince,PlateNumber,PlateCategory,PlateColor,PlateSize,PlateType,Direction,VehicleColor,VehicleType,EventTime,LibraryName)
    if(PlateCountry != "KSA"):
            if PlateColor == "White":
                 plateType = "1"
            elif PlateColor == "Yellow":
                 plateType = "2"
            elif PlateColor == "Blue":
                 plateType = "3"
            elif PlateColor == "Green":
                 plateType = "9"
            elif PlateColor == "Gray":
                 plateType = "8"
            else:
                 plateType = "1"
            plateNumber = PlateNumber[:-3]
            plateEnLetter1 = PlateNumber[-3]
            plateEnLetter2 = PlateNumber[-2]
            plateEnLetter3 = PlateNumber[-1]
            CameraIPx = DeviceIPAddress
            CaptureTimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Country = "Saudi Arabia"
            #PhotoB64 = "Base64Image".decode('UTF-8')
            BodyParams = {
                        "plateType":plateType, 
                        "plateNumber":plateNumber,
                        "plateEnLetter1":plateEnLetter1,
                        "plateEnLetter2":plateEnLetter2,
                        "plateEnLetter3":plateEnLetter3,
                        "CameraIP":CameraIPx,
                        "CaptureTimeStamp":CaptureTimeStamp,
                        "Country":Country,
                        "PhotoB64":licensePlatePicture_string.decode('UTF-8'),
                    }
            Resp = requests.post("http://localhost/Kashef/API/Kashef/VehicleLogs", json = BodyParams,timeout=5)
            print(Resp.text)
    # except:
    #      print("Error while Processing Requests")
    #      return "Error"
    return "Success"  # Return a response indicating successful processing

if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0', port=4300)

