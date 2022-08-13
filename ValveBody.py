import uasyncio
from pyb import Timer, Pin   
from Data import Data

class OnOff_Solenoid:
    def __init__(self, pin, value: bool):
        self.io = Pin(pin, Pin.OUT)
        self.io.value(value)
        
    def toggle(self, state: bool):
        self.io.value(state)

    def compare_state(self, value: int):
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

    def gear_change(self):
        return self.GEARCHANGE[str(self.state.gear) + "to" + str(self.state.nextGear)](self)

    def none_to_park(self):
        print (f"{Data.PARK}")

    def none_to_reverse(self):
        print (f"{Data.REVERSE}")

    def none_to_nuetral(self):
        print (f"{Data.NUETRAL}")

    def none_to_drive(self):
        print (f"{Data.FIRST}") #start in first? add checks for speed
        for i, sol in enumerate(self.vb):
            if (sol.compare_state(Data.FIRST[i])):
                print(f"{i}{Data.FIRST[i]}")

    GEARCHANGE = {
        "Noneto0": none_to_park,
        "Noneto1": none_to_reverse,
        "Noneto2": none_to_nuetral,
        "Noneto3": none_to_drive,

        "1to0": "reverse to park",
        "2to0": "nuetral to park",
        "3to0": "first to park",
        "4to0": "second to park",
        "5to0": "third to park",
        "6to0": "fourth to park",
        "7to0": "fifth to park",
        "8to0": "sixth to park",

        "0to2": "park to nuetral",
        "1to2": "reverse to nuetral",
        "3to2": "first to nuetral",
        "4to2": "second to nuetral",
        "5to2": "dthird to nuetral",
        "6to2": "fourth to nuetral",
        "7to2": "fifth to nuetral",
        "8to2": "sixth to nuetral",
        
        "0to1": "park to reverse",
        "2to1": "nuetral to reverse",
        "3to1": "first to reverse",
        "4to1": "second to reverse",
        "5to1": "third to reverse",
        "6to1": "fourth to reverse",
        "7to1": "fifth to reverse",
        "8to1": "sixth to reverse",
        
        "0to3": "park to drive",
        "1to3": "reverse to drive",
        "2to3": "nuetral to drive",

        #paddle shifting
        "3to4": "first to second",
        "4to5": "second to third",
        "5to6": "third to fourth",
        "6to7": "fourth to fifth",
        "7to8": "fifth to sixth",

        "8to7": "sixth to fifth",
        "7to6": "sixth to fifth",
        "6to5": "sixth to fifth",
        "5to4": "sixth to fifth",
        "4to3": "sixth to fifth"
    }

    def shift(self):
        self.gear_change()
        self.state.gear = self.state.nextGear
        self.state.nextGear = None
        self.state.shifting = False
        
    async def adjust(self):
        while True:
            for _ in self.vb:
                if isinstance(_, OnOff_Solenoid):#wrong place for this
                    pass
                elif isinstance(_, PWM_Solenoid):
                    _.set_ps(_.lowPS)

            if self.state.shifting == True:
                self.shift()
                
            await uasyncio.sleep_ms(40)