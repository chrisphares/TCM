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

    def park(self, state):
        if (state.gear == Data.PARK):
            pass
        else:
            state.selectGear = Data.SELECT_PARK
            print(f"park")

    def reverse(self, state):
        if (state.gear == Data.REVERSE):
            pass
        else:
            state.selectGear = Data.SELECT_REVERSE
            print(f"reverse")

    def nuetral(self, state):
        if (state.gear == Data.SELECT_NUETRAL):
            pass
        else:
            state.selectGear = Data.SELECT_NUETRAL
            print(f"nuetral")

    def drive(self, state):
        if (state.gear == Data.SELECT_DRIVE):
            pass
        else:
            state.paddleGear = Data.PADDLE_START
            state.selectGear = Data.SELECT_DRIVE
            print(f"drive")

    def paddle_up(self, state):
        if not (state.selectGear == Data.SELECT_DRIVE):
            pass
        else:
            if (state.paddleGear < Data.PADDLE_6):
                state.paddleGear += 1
                print(f"up")
            else:
                print(f"in 6th - do nothing")
                pass

    def paddle_down(self, state):
        if not (state.selectGear == Data.SELECT_DRIVE):
            pass
        else:
            if (state.paddleGear > Data.PADDLE_1):
                state.paddleGear -= 1
                print(f"dn")
            else:
                print(f"in 1st - do nothing")

    def tc_lock(self, state):
        if not (state.selectGear == Data.SELECT_DRIVE):
            pass
        else:
            print("lock")

    async def get_input(self):
        while True:
            for _ in self.inputs:
                _.set_input_flags()
                if _.resolve_input_flags(): #and not self.state.shifting:
                    _.action(self.state)

            await uasyncio.sleep_ms(40)