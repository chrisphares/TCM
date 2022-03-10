import uasyncio
from pyb import Pin, ADC
from time import ticks_ms, ticks_diff
from Data import Data

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
    
    def press(self):
        print(f"{self.gear}")

    def set_input_flags(self):
        reading = self.pin.value()
        if reading != self.lastInputState:
            self.lastDebounceTime = ticks_ms()
        debounce = ticks_diff(ticks_ms(), self.lastDebounceTime)
        if debounce > self.delay:
            self.inputFlags = reading
                
        self.lastInputState = reading

    def resolve_input_flags(self):
        if not self.inputFlags:
            self.press()

class Input:
    #gear selection inputs
    parkIO = Pin_IO('Y6', 250, Data.PARK)
    reverseIO = Pin_IO('Y7', 250, Data.REVERSE)
    nuetralIO = Pin_IO('Y8', 100, Data.NUETRAL)
    driveIO = Pin_IO('X9', 100, Data.DRIVE)
    
    #paddle gear input
    upIO = Pin_IO('Y2', 15, 'up')
    downIO = Pin_IO('Y3', 15, 'dn')
    
    #TC Lock button
    lockIO = Pin_IO('Y1', 15, 'tcc')

    inputs = (
        parkIO,
        reverseIO,
        nuetralIO,
        driveIO,
        upIO,
        downIO,
        lockIO,
        )

    def __init__(self, state):
        self.current = state

    async def evaluate(self):
        while True:
            for i in self.inputs:
                i.set_input_flags()
                i.resolve_input_flags()
            await uasyncio.sleep_ms(50)