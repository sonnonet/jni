import HPMA115S0
import time
import json
import requests
import datetime
import time
from neopixel import *
import xml.etree.ElementTree as etree
import argparse

# LED Strip configuration

LED_COUNT = 6
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

pm2_5 = 0

def pm2_5Data():
    global pm2_5
    tree = etree.parse('sample.xml')
    root = tree.getroot()
    Next = root.find('body')
    Third = Next.find('items')
    data = Third.find('item')
    pm2_5 = data.findtext('pm10Value')


url = "http://127.0.0.1:4242/api/put?details"
#pm2_5Data()
if __name__ == '__main__':
    
    strip=Adafruit_NeoPixel(LED_COUNT,LED_PIN,LED_FREQ_HZ,LED_DMA,LED_INVERT,LED_BRIGHTNESS,LED_CHANNEL)
    strip.begin()
    for i in range(0, strip.numPixels(),1):
        strip.setPixelColor(i, Color(0,0,0))

#pm2_5 = int(pm2_5)


    try:
        print("Starting")
        hpma115S0 = HPMA115S0.HPMA115S0("/dev/ttyAMA0")
        hpma115S0.init()
        hpma115S0.startParticleMeasurement()

        while 1:
            if (hpma115S0.readParticleMeasurement()):
                data = {
                    "metric": "Clome.2_5_Dust.ug",
                    "timestamp":time.time(),
                    "value":hpma115S0._pm2_5,
                    "tags": {
                        "id" : "1",
                        "sensor" : "Honeywell_DustSensor",
                        "building" : "COEX",
                        "city" : "SEOUL"
                        }
                    }
                data1 = {
                    "metric": "Clome.10_Dust.ug",
                    "timestamp":time.time(),
                    "value":hpma115S0._pm10,
                    "tags": {
                        "id" : "2",
                        "sensor" : "Honeywell_DustSensor",
                        "building" : "COEX",
                        "city" : "SEOUL"
                        }
                    }
            try:
                ret = requests.post(url, data=json.dumps(data))
                ret = requests.post(url, data=json.dumps(data1))
                print("PM2.5: %d ug/m3" % (hpma115S0._pm2_5))
                print("PM10: %d ug/m3" % (hpma115S0._pm10))
            
                if hpma115S0._pm2_5<55:
                    strip.setPixelColor(0, Color(255,0,0))
                    strip.setPixelColor(2, Color(0,0,0))
                    strip.setPixelColor(4, Color(0,0,0))
                    print("LED Green!")
                elif hpma115S0._pm2_5>100:
                    strip.setPixelColor(4, Color(0,255,0))
                    strip.setPixelColor(0, Color(0,0,0))
                    strip.setPixelColor(2, Color(0,0,0))
                    print("LED Red!")
                else:
                    strip.setPixelColor(2, Color(255,255,0))
                    strip.setPixelColor(0, Color(0,0,0))
                    strip.setPixelColor(4, Color(0,0,0))
                    print("LED Yellow!")

            except:
                print("except")
                pass
            strip.show()
            time.sleep(1)
#        for i in range(strip.numPixels()):
#            strip.setPixelColor(i, Color(0,0,0))
#            strip.show()

    except KeyboardInterrupt:
        print("program stopped")
