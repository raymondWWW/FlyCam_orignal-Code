"""
Code to practice playing around with GPIO Zero

Sources:
https://gpiozero.readthedocs.io/en/stable/api_pins.html?highlight=mock#mock-pins

First, test case, replicate code here, but with gpiozero
https://www.electronicshub.org/raspberry-pi-color-sensor-tutorial/

Color Sensor Datasheet, for mock values?
https://www.best-microcontroller-projects.com/support-files/tcs230.pdf

Color Sensor info
https://www.best-microcontroller-projects.com/tcs230.html
"""

from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory

Device.pin_factory = MockFactory()

led = LED(2)

print(led.value)

led.on()

print(led.value)