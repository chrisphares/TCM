from pyb import Pin, ADC
from time import ticks_ms, ticks_diff

class Pin_IO:
    inputFlags = 0
    lastInputState = 0
    lastDebounceTime = 0
        
    def __init__(self, pin, delay: int, gear=None):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.delay = delay
        self.gear = gear
    
    def value(self):
        return self.pin.value()
    
    def press(self, currentGear):
        if self.gear is None:
            pass
        else:
            print(f"{self.gear=}")

class Adjust_IO:
    def __init__(self, pin):
        self.adc = ADC(Pin(pin))

    def value(self):
        r = self.adc.read()
        if not r:
            return 0
        elif r < 250:
            return 0
        elif r < 800:
            return 1
        elif r < 1400:
            return 2
        elif r < 2000:
            return 3
        elif r < 2600:
            return 4
        elif r < 3200:
            return 5
        elif r < 3600:
            return 6
        elif r >= 3600:
            return 7