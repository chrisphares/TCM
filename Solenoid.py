import uasyncio
from pyb import Timer, Pin   
from Data import Data

class OnOff_Solenoid:
    def __init__(self, pin, value: bool):
        self.io = Pin(pin, Pin.OUT)
        self.io.value(value)
        
    def toggle(self, state: bool):
        self.io.value(state)

    def compareState(self, value: int):
        return self.io.value() == value
        
class PWM_Solenoid:
    def __init__(self, pin, value: int, lowPS: int, highPS: int):
        self.tim = Timer(Data.PIN[pin][0], freq=300) #timer dict lookup
        self.io = self.tim.channel(Data.PIN[pin][1], Timer.PWM, pin=Pin(pin)) #channel dict lookup
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

class Valve_Body:
    OFF = const(0)
    ON = const(1)

    n88 = OnOff_Solenoid('X22', OFF)
    n89 = OnOff_Solenoid('X21', OFF)
    
    n90 = PWM_Solenoid('X4', 10, 10, 60)
    n92 = PWM_Solenoid('X2', 10, 20, 60)
    n282 = PWM_Solenoid('Y10', 10, 30, 60)
    n283 = PWM_Solenoid('Y9', 10, 40, 90)

    n91 = PWM_Solenoid('X3', 50, 20, 60) #converter clutch
    n93 = PWM_Solenoid('X1', 60, 20, 60) #main line presssure

    vb = (n88, n89, n90, n92, n282, n283)
    
    def __init__(self, state):
        self.state = state

    def shift(self):
        print(f"from x to y")
        

    async def adjust(self):
        while True:
            for _ in self.vb:
                if isinstance(_, OnOff_Solenoid):#wrong place for this
                    pass
                elif isinstance(_, PWM_Solenoid):
                    _.set_ps(_.lowPS)

            if self.state.shifting == True:
                self.state.gear = self.state.selectGear
                
            await uasyncio.sleep_ms(40)