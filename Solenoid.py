from pyb import Timer, Pin   
from Data import Data

class OnOff_Solenoid:
    def __init__(self, pin, value: int):
        self.io = Pin(pin, Pin.OUT)
        self.io.value(value)
        
    def toggle(self, state: bool):
        self.io.value(state)

    def compareState(self, value: int):
        return self.io.value() == value
        
class PWM_Solenoid:
    def __init__(self, pin, value: int, lowPS: int, highPS: int):
        self.tim = Timer(Data.PIN[pin][0], freq=300) #timer lookup
        self.io = self.tim.channel(Data.PIN[pin][1], Timer.PWM, pin=Pin(pin)) #channel lookup
        self.lowPS = lowPS
        self.highPS = highPS
        self.io.pulse_width_percent(value)

    def set_ps(self, value: int):
        self.io.pulse_width_percent(value)

    def compare_state(self, value: int):
        if value:
            return self.io.pulse_width_percent() >= self.highPS
        if not value:
            return self.io.pulse_width_percent() <= self.lowPS