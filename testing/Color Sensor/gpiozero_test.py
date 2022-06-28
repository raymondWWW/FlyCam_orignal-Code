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

from gpiozero import Device, LED, Button
from gpiozero.pins.mock import MockFactory, MockPWMPin


def main3():
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)

    led = LED(2)

    print(led.value)
    pass

def main2():
    Device.pin_factory = MockFactory()

    # LED/Button Test
    led = LED(17)
    btn = Button(16)

    # Bug for me, led.source = btn isn't working

    btn.when_pressed = led.on
    btn.when_released = led.off

    # Initially, the button isn't pressed so the LED should be off
    print(led.value)

    # Press the button
    btn.pin.drive_low()

    print(led.value)

    # Release the button
    btn.pin.drive_high()

    print(led.value)


def main():
    # https://gpiozero.readthedocs.io/en/stable/api_pins.html?highlight=mock#mock-pins
    # Simple LED off/on check
    Device.pin_factory = MockFactory()

    led = LED(2)

    print(led.value)

    led.on()

    print(led.value)


if __name__ == "__main__":
    # main()
    # main2()
    main3()

