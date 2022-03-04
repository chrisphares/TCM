from pyb import Timer, Pin   
from Data import Data

class OnOff_Solenoid:
    def __init__(self, pin, value):
        self.io = Pin(pin, Pin.OUT)
        self.io.value(value)
        
    def toggle(self, state):
        self.io.value(state)

    def compareState(self, value):
        return self.io.value() == value
        
class Pressure_Solenoid:
    def __init__(self, p, ps: int):
        self.t = Data.PIN[p][0]#timer lookup
        self.c = Data.PIN[p][1]#channel lookup
        self.tim = Timer(self.t, freq=300)
        self.io = self.tim.channel(self.c, Timer.PWM, pin=Pin(p))
        self.io.pulse_width_percent(ps)

    def setPS(self, ps: int):
        #ps = int(65535 - (self.io.duty_u16() * ((100 - value) / 100)))
        self.io.pulse_width_percent(int(ps))
        
class Control_Solenoid:
    def __init__(self, p, lowPS: int, highPS: int):
        self.t = Data.PIN[p][0]#timer lookup
        self.c = Data.PIN[p][1]#channel lookup
        self.tim = Timer(self.t, freq=300) #300hz is solenoid requirement
        self.io = self.tim.channel(self.c, Timer.PWM, pin=Pin(p))
        self.lowPS = lowPS
        self.highPS = highPS
        self.duty = lowPS # **this seems duplicative
        self.stepON = int((self.highPS - self.lowPS) / 60)# **define this number
        self.stepOFF = int((self.highPS - self.lowPS) / 30)# **define this number
        #self.ps = lowPS # **identify why this is duplicative
        self.io.pulse_width_percent(self.duty)

    def adjustState(self, value):
        if value:
            self.duty = self.duty + self.stepON
        if not value:
            self.duty = self.duty - self.stepOFF

    def compareState(self, value):
        if value:
            return self.duty >= self.highPS
        if not value:
            return self.duty <= self.lowPS