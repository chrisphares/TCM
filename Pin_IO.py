from pyb import Pin, ADC
from time import ticks_ms, ticks_diff

class Pin_IO:
    inputFlags = 0
    lastInputState = 0
    lastDebounceTime = 0
        
    def __init__(self, pin, delay, gear=None):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.delay = delay
        self.gear = gear
    
    def value(self):
        return self.pin.value()
    
    def press(self, currentGear, onOff):
        return onOff

class Select_IO(Pin_IO):
    def press(self, vb):
        for i, g in enumerate(self.gear):
            if not vb[i].compareState(g):
                vb[i].adjustState(g)

class Drive_IO(Pin_IO):
    def press(self, vb):
        for i, g in enumerate(self.gear):
            if not vb[i].compareState(g):
                vb[i].adjustState(g)
        
class Paddle_Up_IO(Pin_IO):
    def press(self, currentGear):
        if currentGear:
            return currentGear + 1
        
class Paddle_Down_IO(Pin_IO):
    def press(self, currentGear):
        if currentGear:
            return currentGear - 1

class Adjust_IO:
    def __init__(self, pin)
        self.adc = ADC(Pin(pin))

    def value(self):
        value = int(4096 / self.adc.read())
        return value