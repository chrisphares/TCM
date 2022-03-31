import uasyncio
from pyb import Pin, ADC
from time import ticks_ms, ticks_diff
from Data import Data

class Pin_IO:
    OFF = const(0)
    ON = const(1)

    def __init__(self, pin, delay: int, gear=None, action=None):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.delay = delay
        self.gear = gear#wrong label
        self.action= action
        self.state = OFF##
        self.lastState = OFF##
        self.inputFlags = OFF
        self.lastInputState = OFF
        self.lastDebounceTime = 0
    
    def value(self):
        return self.pin.value()
    
    def set_input_flags(self):
        reading = self.value()
        if reading != self.lastInputState:
            self.lastDebounceTime = ticks_ms()
        debounce = ticks_diff(ticks_ms(), self.lastDebounceTime)
        if debounce > self.delay:
            self.inputFlags = reading
                
        self.lastInputState = reading

    def resolve_input_flags(self):
        return not self.inputFlags

class Input:
    def __init__(self, state):
        self.current = state

        #gear selection inputs
        self.parkIO = Pin_IO('Y6', 250, Data.PARK, self.park)
        self.reverseIO = Pin_IO('Y7', 250, Data.REVERSE, self.reverse)
        self.nuetralIO = Pin_IO('Y8', 100, Data.NUETRAL, self.nuetral)
        self.driveIO = Pin_IO('X9', 100, Data.DRIVE, self.drive)
        
        #paddle gear input
        self.upIO = Pin_IO('Y1', 15, 'up', self.paddle_up)
        self.downIO = Pin_IO('Y2', 15, 'dn', self.paddle_down)
        
        #TC Lock button
        self.lockIO = Pin_IO('Y5', 15, 'tcc', self.tc_lock)

        self.inputs = (
            self.parkIO,
            self.reverseIO,
            self.nuetralIO,
            self.driveIO,
            self.upIO,
            self.downIO,
            self.lockIO,
            )

    def park(self):
        self.current.selectGear = "P"
        self.current.nextGear = "P"
        print(f"park")

    def reverse(self):
        self.current.selectGear = "R"
        self.current.nextGear = "R"
        print(f"reverse")

    def nuetral(self):
        self.current.selectGear = "N"
        self.current.nextGear = "N"
        print(f"nuetral")

    def drive(self):
        self.current.selectGear = "D"
        self.current.nextGear = "D"
        print(f"drive")

    def paddle_up(self):
        if not self.current.selectGear == "D":
            pass
        else:
            self.current.nextGear = "up"
            print(f"up")

    def paddle_down(self):
        if not self.current.selectGear == "D":
            pass
        else:
            self.current.nextGear = "dn"
            print(f"dn")

    def tc_lock(self):
        self.current.lock = not self.current.lock
        print(f"{self.current.lock}")

    async def evaluate(self):
        while True:
            for _ in self.inputs:
                _.set_input_flags()
                if _.resolve_input_flags(): #and not self.current.shifting:
                    _.action()

            await uasyncio.sleep_ms(40)