import uasyncio
from pyb import Pin, ADC
from time import ticks_ms, ticks_diff
from Data import Data

class Pin_IO:
    OFF = const(0)
    ON = const(1)

    def __init__(self, pin, delay: int, action: callable) -> None:
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.delay = delay
        self.action = action
        self.inputFlags = OFF
        self.lastInputState = OFF
        self.lastDebounceTime = 0
    
    def set_input_flags(self) -> None:
        reading = self.pin.value()
        if reading != self.lastInputState:
            self.lastDebounceTime = ticks_ms()
        debounce = ticks_diff(ticks_ms(), self.lastDebounceTime)
        if debounce > self.delay:
            self.inputFlags = reading
                
        self.lastInputState = reading

    def resolve_input_flags(self) -> None:
        return self.inputFlags

class Input:
    def __init__(self, state) -> None:
        self.state = state

        #gear selection inputs
        self.parkIO = Pin_IO('Y5', 250, self.select_gear_change)
        self.reverseIO = Pin_IO('Y6', 250, self.select_gear_change)
        self.nuetralIO = Pin_IO('Y7', 100, self.select_gear_change)
        self.driveIO = Pin_IO('Y8', 100, self.select_gear_change)
        
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

    def select_gear_change(self) -> None:
        #maybe add implausable values?
        bitPosition = (self.parkIO.inputFlags << 3) + (self.reverseIO.inputFlags << 2) + (self.nuetralIO.inputFlags << 1) + (self.driveIO.inputFlags)
        if (bitPosition is None):
            return
        if (self.state.selectGear != Data.SELECTGEAR[bitPosition]):
            self.state.shifting = True
            self.state.selectGear = Data.SELECTGEAR[bitPosition]
            self.state.nextGear = Data.SELECTGEAR[bitPosition]
            if (bitPosition == 1):
                self.state.paddleGear = 0
            else:
                self.state.paddleGear = None

    def paddle_up(self) -> None:
        if ((self.state.selectGear == Data.SELECT_DRIVE) and (self.state.paddleGear < Data.PADDLE_6)):
            self.state.shifting = True
            self.state.paddleGear += 1
            self.state.nextGear = Data.SELECT_DRIVE + self.state.paddleGear 

    def paddle_down(self) -> None:
        if ((self.state.selectGear == Data.SELECT_DRIVE) and (self.state.paddleGear > Data.PADDLE_1)):
            self.state.shifting = True
            self.state.paddleGear -= 1
            self.state.nextGear = Data.SELECT_DRIVE + self.state.paddleGear 

    def tc_lock(self) -> None:
        delay = ticks_diff(ticks_ms(), self.state.lockDelayTime)
        if ((delay > self.state.lockDelay) and (self.state.selectGear == Data.SELECT_DRIVE) and (self.state.paddleGear >= Data.PADDLE_3)):
            self.state.lock = not self.state.lock
            self.state.lockDelayTime = ticks_ms()

    async def get_input(self) -> None:
        while True:
            for _ in self.inputs:
                _.set_input_flags()
                if (not self.state.shifting and _.resolve_input_flags()):
                    _.action()
            await uasyncio.sleep_ms(40)