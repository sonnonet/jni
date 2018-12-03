import HPMA115S0
import time
import json
import requests
import datetime
import time

url = "http://127.0.0.1:4242/api/put?details"

try:
    print("Starting")
    hpma115S0 = HPMA115S0.HPMA115S0("/dev/ttyAMA0")

    hpma115S0.init()
    hpma115S0.startParticleMeasurement()

    while 1:
        if (hpma115S0.readParticleMeasurement()):
            data = {
                    "metric": "sonnonet.2_5_Dust.ug",
                    "timestamp":time.time(),
                    "value":hpma115S0._pm2_5,
                    "tags": {
                        "id" : "1",
                        "sensor" : "Honeywell_DustSensor",
                        "building" : "SONNONET",
                        "city" : "Bucheon"
                        }
                    }
            data1 = {
                    "metric": "sonnonet.10_Dust.ug",
                    "timestamp":time.time(),
                    "value":hpma115S0._pm10,
                    "tags": {
                        "id" : "2",
                        "sensor" : "Honeywell_DustSensor",
                        "building" : "SONNONET",
                        "city" : "Bucheon"
                        }
                    }
        try:
            ret = requests.post(url, data=json.dumps(data))
            ret = requests.post(url, data=json.dumps(data1))
            print("PM2.5: %d ug/m3" % (hpma115S0._pm2_5))
            print("PM10: %d ug/m3" % (hpma115S0._pm10))
        except:
            pass
        time.sleep(1)

except KeyboardInterrupt:
    print("program stopped")
