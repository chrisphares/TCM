import uasyncio
from pyb import Pin, ADC
from time import ticks_ms, ticks_diff
from Data import Data

class Pin_IO:
    OFF = const(0)
    ON = const(1)

    def __init__(self, pin, delay: int, action=None):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.delay = delay
        self.action = action
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
        return self.inputFlags

class Input:
    def __init__(self, state):
        self.state = state

        #gear selection inputs
        self.parkIO = Pin_IO('Y5', 250, self.park)
        self.reverseIO = Pin_IO('Y6', 250, self.reverse)
        self.nuetralIO = Pin_IO('Y7', 100, self.nuetral)
        self.driveIO = Pin_IO('Y8', 100, self.drive)
        
        #paddle gear input
        self.upIO = Pin_IO('Y1', 15, self.paddle_up)
        self.downIO = Pin_IO('Y2', 15, self.paddle_down)
        
        #TC Lock button
        self.lockIO = Pin_IO('Y12', 15, self.tc_lock)

        self.inputs = (
            self.parkIO,
            self.reverseIO,
            self.nuetralIO,
            self.driveIO,
            self.upIO,
            self.downIO,
            self.lockIO,
            )

    def is_shifting(self):
        return self.state.shifting

    def park(self):
        if (self.state.selectGear == Data.SELECT_PARK):
            pass
        else:
            self.state.shifting = True
            self.state.selectGear = Data.SELECT_PARK
            self.state.paddleGear = None
            self.state.nextGear = Data.SELECT_PARK

    def reverse(self):
        if (self.state.selectGear == Data.SELECT_REVERSE):
            pass
        else:
            self.state.shifting = True
            self.state.selectGear = Data.SELECT_REVERSE
            self.state.paddleGear = None
            self.state.nextGear = Data.SELECT_REVERSE

    def nuetral(self):
        if (self.state.selectGear == Data.SELECT_NUETRAL):
            pass
        else:
            self.state.shifting = True
            self.state.selectGear = Data.SELECT_NUETRAL
            self.state.paddleGear = None
            self.state.nextGear = Data.SELECT_NUETRAL

    def drive(self):
        if (self.state.selectGear == Data.SELECT_DRIVE):
            pass
        else:
            self.state.shifting = True
            self.state.selectGear = Data.SELECT_DRIVE
            self.state.paddleGear = 0 # first?
            self.state.nextGear = Data.SELECT_DRIVE #change to better initial selection with i/o & speed/rpm calc

    def paddle_up(self):
        if ((self.state.selectGear != Data.SELECT_DRIVE) or (self.state.paddleGear == Data.PADDLE_6) or (self.state.paddleGear == None)):
            pass
        else:
            self.state.shifting = True
            self.state.paddleGear += 1
            self.state.nextGear = Data.SELECT_DRIVE + self.state.paddleGear 

    def paddle_down(self):
        if ((self.state.selectGear != Data.SELECT_DRIVE) or (self.state.paddleGear == Data.PADDLE_1) or (self.state.paddleGear == None)):
            pass
        else:
            self.state.shifting = True
            self.state.paddleGear -= 1
            self.state.nextGear = Data.SELECT_DRIVE + self.state.paddleGear 

    def tc_lock(self):
        if not (self.state.selectGear == Data.SELECT_DRIVE):
            pass
        else:
            pass

    async def get_input(self):
        while True:
            for _ in self.inputs:
                _.set_input_flags()
                if self.is_shifting():
                    pass
                elif _.resolve_input_flags():
                    _.action()

            await uasyncio.sleep_ms(40)