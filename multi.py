#! /usr/bin/python3

import time
from homie.device_integer import Device_Integer
import sys

mqtt_settings = {
    "MQTT_BROKER": "ezmeral52gateway1.demo.local",
    "MQTT_PORT": 10003,
    "MQTT_USERNAME": "ezmeral",
    "MQTT_PASSWORD": "",
    "MQTT_KEEPALIVE": 60,
    "MQTT_CLIENT_ID": None,
    "MQTT_SHARE_CLIENT": True,
    "MQTT_USE_TLS": True,
}

class Weight_Sensor(Device_Integer):
    def set_integer(self, value):
        print(
            "Received MQTT message to set the integer to {}. Must replace this method".format(
                value
            )
        )

sensors = []

for x in range(1, 10):
    sensor = Weight_Sensor(
        device_id="weight-sensor-{}".format(x),
        name="Weight Sensor {}".format(x),
        mqtt_settings=mqtt_settings,
    )
    sensors.append(sensor)

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
hx.append(HX711(7, 8))

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
            sensors[i].update_value(val)

            hx[i].power_down()
            time.sleep(5)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
