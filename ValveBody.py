import uasyncio
from pyb import Timer, Pin   
from Data import Data

#testing
from time import sleep_ms

class OnOff_Solenoid:
    def __init__(self, pin: Pin, value: bool) -> None:
        self.io = Pin(pin, Pin.OUT)
        self.io.value(value)
        
    def toggle(self, state: bool) -> None:
        self.io.value(state)
        
class PWM_Solenoid:
    def __init__(self, pin: Pin, value: int=10, lowPS: int=10, highPS: int=60) -> None:
        self.tim = Timer(Data.PIN[pin][0], freq=300) #timer dict lookup
        self.io = self.tim.channel(Data.PIN[pin][1], Timer.PWM, pin=Pin(pin)) #channel dict lookup
        self.lowPS = lowPS
        self.highPS = highPS
        self.io.pulse_width_percent(value)

    def set_ps(self, value: int) -> None:
        self.io.pulse_width_percent(value)

    def toggle(self, enable: bool) -> None:
        if enable:
            self.io.pulse_width_percent(self.lowPS)
        if not enable:
            self.io.pulse_width_percent(self.highPS)

class Valve_Body:
    OFF = const(0)
    ON = const(1)

    n88 = OnOff_Solenoid('X22', OFF)
    n89 = OnOff_Solenoid('X21', OFF)
    
    n90 = PWM_Solenoid('X4') #use defaults
    n92 = PWM_Solenoid('X2', 10, 20)
    n282 = PWM_Solenoid('Y10', 10, 30, 60)
    n283 = PWM_Solenoid('Y9', 10, 10, 75)

    n91 = PWM_Solenoid('X3', 10) #converter clutch / normally vented / initial value, then use TCCMAP in Data
    #change to use math ^

    n93 = PWM_Solenoid('X1', 60) #main line presssure

    def __init__(self, state: State) -> None:
        self.state = state

    def get_tcc_pressure(self, lowVal: int, highVal: int) -> int:
        return int(((highVal - lowVal) * (Data.TCCMAP[self.state.adjTCC] / 100)) + lowVal)

    def get_gear_change(self) -> callable:
        return self.GEARCHANGE[str(self.state.gear) + "to" + str(self.state.nextGear)](self)

    def none_to_park(self) -> bool:
        #read output shaft speed
        self.n88.toggle(Data.PARK[0])
        self.n89.toggle(Data.PARK[1])
        self.n90.toggle(Data.PARK[2])
        self.n92.toggle(Data.PARK[3])
        self.n282.toggle(Data.PARK[4])
        self.n283.toggle(Data.PARK[5])
        return True

    def none_to_reverse(self) -> bool:
        self.n88.toggle(Data.REVERSE[0])
        self.n89.toggle(Data.REVERSE[1])
        self.n90.toggle(Data.REVERSE[2])
        self.n92.toggle(Data.REVERSE[3])
        self.n282.toggle(Data.REVERSE[4])
        self.n283.toggle(Data.REVERSE[5])
        return True

    def none_to_nuetral(self) -> bool:
        self.n88.toggle(Data.NUETRAL[0])
        self.n89.toggle(Data.NUETRAL[1])
        self.n90.toggle(Data.NUETRAL[2])
        self.n92.toggle(Data.NUETRAL[3])
        self.n282.toggle(Data.NUETRAL[4])
        self.n283.toggle(Data.NUETRAL[5])
        return True

    def none_to_drive(self) -> bool: #add checks for RPM/OSS
        self.n88.toggle(Data.FIRST[0])
        self.n89.toggle(Data.FIRST[1])
        self.n90.toggle(Data.FIRST[2])
        self.n92.toggle(Data.FIRST[3])
        self.n282.toggle(Data.FIRST[4])
        self.n283.toggle(Data.FIRST[5])
        return True

    def first_to_second(self) -> bool:
        self.n88.toggle(OFF)
        self.n89.toggle(OFF)

        stepN283 = ((self.n283.highPS - self.n283.lowPS) // 15) * -1
        valN283 = list(range(self.n283.highPS, self.n283.lowPS,  stepN283))

        if (self.state.shiftStage <= 15):
            self.n283.set_ps(valN283[self.state.shiftStage])
            self.state.shiftStage += 1
            return False
        else:
            self.n283.set_ps(self.n283.lowPS)
            return True

    def second_to_third(self) -> bool:
        stepN283 = ((self.n283.highPS - self.n283.lowPS) // 15) * -1
        stepN90 = ((self.n90.highPS - self.n90.lowPS) // 15)
        
        valN283 = list(range(self.n283.highPS, self.n283.lowPS,  stepN283))
        valN90 = list(range(self.n90.lowPS, self.n90.highPS, stepN90))

        for i in range(10):
            valN283.insert(0, self.n283.highPS)
            valN90.append(self.n90.highPS)

        if (self.state.shiftStage == 0):
            self.n88.toggle(ON)
            self.n89.toggle(self.state.lock)
            self.state.shiftStage += 1
            return False
        elif (self.state.shiftStage <= 25):
            self.n283.set_ps(valN283[self.state.shiftStage])
            self.n90.set_ps(valN90[self.state.shiftStage])
            self.state.shiftStage += 1
            return False
        else:
            self.n283.set_ps(self.n283.lowPS)
            self.n90.set_ps(self.n90.highPS)
            self.n88.toggle(OFF)
            return True

    def third_to_fourth(self) -> bool:
        stepN90 = ((self.n90.highPS - self.n90.lowPS) // 15) * -1
        stepN282 = ((self.n282.highPS - self.n282.lowPS) // 15)
        
        valN90 = list(range(self.n90.highPS, self.n90.lowPS,  stepN90))
        valN282 = list(range(self.n282.lowPS, self.n282.highPS, stepN282))

        for i in range(10):
            valN90.insert(0, self.n90.highPS)
            valN282.append(self.n282.highPS)

        if (self.state.shiftStage == 0):
            self.n88.toggle(ON)
            self.n89.toggle(self.state.lock)
            self.state.shiftStage += 1
            return False
        elif (self.state.shiftStage <= 25):
            self.n90.set_ps(valN90[self.state.shiftStage])
            self.n282.set_ps(valN90[self.state.shiftStage])
            self.state.shiftStage += 1
            return False
        else:
            self.n90.set_ps(self.n90.lowPS)
            self.n282.set_ps(self.n90.highPS)
            self.n88.toggle(OFF)
            return True

    def fourth_to_third(self) -> bool:
        stepN282 = ((self.n282.highPS - self.n282.lowPS) // 15) * -1
        stepN90 = ((self.n90.highPS - self.n90.lowPS) // 15)
        
        valN282 = list(range(self.n282.highPS, self.n282.lowPS,  stepN282))
        valN90 = list(range(self.n90.lowPS, self.n90.highPS, stepN90))

        for i in range(10):
            valN282.insert(0, self.n282.highPS)
            valN90.append(self.n90.highPS)

        if (self.state.shiftStage == 0):
            self.n88.toggle(ON)
            self.n89.toggle(self.state.lock)
            self.state.shiftStage += 1
            return False
        elif (self.state.shiftStage <= 25):
            self.n90.set_ps(valN90[self.state.shiftStage])
            self.n282.set_ps(valN90[self.state.shiftStage])
            self.state.shiftStage += 1
            return False
        else:
            self.n90.set_ps(self.n90.highPS)
            self.n282.set_ps(self.n90.lowPS)
            self.n88.toggle(OFF)
            return True

    GEARCHANGE = {
        "Noneto0": none_to_park,
        "Noneto1": none_to_reverse,
        "Noneto2": none_to_nuetral,
        "Noneto3": none_to_drive,

        "1to0": none_to_park,
        "2to0": none_to_park,
        "3to0": none_to_park,
        "4to0": none_to_park,
        "5to0": none_to_park,
        "6to0": none_to_park,
        "7to0": none_to_park,
        "8to0": none_to_park,
        
        "0to1": "park to reverse",
        "2to1": "nuetral to reverse",
        "3to1": "first to reverse",
        "4to1": "second to reverse",
        "5to1": "third to reverse",
        "6to1": "fourth to reverse",
        "7to1": "fifth to reverse",
        "8to1": "sixth to reverse",

        "0to2": "park to nuetral",
        "1to2": "reverse to nuetral",
        "3to2": "first to nuetral",
        "4to2": "second to nuetral",
        "5to2": "dthird to nuetral",
        "6to2": "fourth to nuetral",
        "7to2": "fifth to nuetral",
        "8to2": "sixth to nuetral",
        
        "0to3": "park to drive",
        "1to3": "reverse to drive",
        "2to3": "nuetral to drive",

        #paddle shifting
        "3to4": first_to_second,
        "4to5": second_to_third,
        "5to6": third_to_fourth,
        "6to7": "fourth to fifth",
        "7to8": "fifth to sixth",

        "8to7": "sixth to fifth",
        "7to6": "5 -> 4",
        "6to5": fourth_to_third,
        "5to4": "3 -> 2",
        "4to3": "2 -> 1"
    }

    def shift(self) -> None:
        if (self.get_gear_change()):
            self.state.gear = self.state.nextGear
            self.state.nextGear = None
            self.state.shifting = False
            self.state.shiftStage = 0

    def engage_TCC(self) -> None:
        self.n91.set_ps(self.get_tcc_pressure(self.n91.lowPS, self.n91.highPS))

    def disengage_TCC(self) -> None:
        self.n91.set_ps(self.n91.lowPS)

    async def adjust(self) -> None:
        while True:
            #for _ in self.vb:
                #if isinstance(_, OnOff_Solenoid):#wrong place for this
                    #pass
                #elif isinstance(_, PWM_Solenoid):
                    #_.set_ps(_.lowPS)

            if (self.state.shifting):
                self.shift()
            
            if (self.state.lock and not self.state.shifting):
                self.engage_TCC()

            if (not self.state.lock):
                self.disengage_TCC()
            
            await uasyncio.sleep_ms(40)