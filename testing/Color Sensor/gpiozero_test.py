"""
Code to practice playing around with GPIO Zero

Sources:
https://gpiozero.readthedocs.io/en/stable/api_pins.html?highlight=mock#mock-pins

"""

from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory

Device.pin_factory = MockFactory()

led = LED(2)

print(led.value)

led.on()

print(led.value)