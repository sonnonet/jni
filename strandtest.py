#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import xml.etree.ElementTree as etree
import argparse

# LED strip configuration:
LED_COUNT      = 6      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 

pm10 = 0

def pm10Data():
    global pm10
    tree = etree.parse('sample.xml')
    root = tree.getroot()
    Next = root.find('body')
    Third = Next.find('items')
    data = Third.find('item')
    pm10 = data.findtext('pm10Value')

if __name__ == '__main__':
    # Process arguments
    pm10Data()
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    pm10 = int(pm10)
    print(type(pm10))
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    try:
        while True:        
            if pm10<16:    
                strip.setPixelColor(0, Color(255, 0, 0))
                strip.setPixelColor(2, Color(0,0,0))
                strip.setPixelColor(4, Color(0,0,0))
            elif pm10>50:
                strip.setPixelColor(4, Color(0, 255, 0))
                strip.setPixelColor(0, Color(0,0,0))
                strip.setPixelColor(2, Color(0,0,0))
            else:
                strip.setPixelColor(2, Color(255,255,0))
                strip.setPixelColor(0, Color(0,0,0))
                strip.setPixelColor(4, Color(0,0,0))
            strip.show()
            time.sleep(2)
                
    except KeyboardInterrupt:
        if args.clear:
            for i in range(strip.numPixel()):
                strip.setPixelColor(i, Color(0,0,0))
                strip.show()
