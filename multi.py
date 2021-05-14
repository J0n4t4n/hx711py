#! /usr/bin/python3

import time
import sys

EMULATE_HX711=True

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = []
hx.append(HX711(5, 6))

for dev in hx:
    dev.set_reading_format("MSB", "MSB")
    dev.set_reference_unit(referenceUnit)

    dev.reset()
    dev.tare()

print("Tares done! Add weight now...")

while True:
    try:
        for i in range(0, len(hx)):
            hx[i].power_up()
            time.sleep(0.1)

            val = hx[i].get_weight(5)
            print("Weight " + str(i) + ": " + str(val))

            hx[i].power_down()

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
