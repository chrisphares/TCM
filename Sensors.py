import uasyncio
from pyb import ADC, Pin
from time import ticks_ms, ticks_us, ticks_diff, ticks_add
from Data import Data
#testing
import random

class Pressure_Sensor:
    def __init__(self, pin):
        self.io = Pin(pin, Pin.IN, Pin.PULL_UP)

    def value(self):
        return self.io.value() 

class Temp_Sensor:
    def __init__(self, pin, min, max):
        self.pin = pin
        self.min = min
        self.max = max
        self.io = ADC(self.pin)
        
    def value(self):
        return int(self.io.read() / (4095 / (self.max - self.min)) + self.min) #/ +math

class Speed_Sensor:
    rpm = 0
    count = 0
    timeout = 15000 #microseconds
    
    def __init__(self, pin, teeth=80):
        self.io = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.teeth = teeth

    def calc(self):
        edge = self.io.value()
        while self.io.value() == edge:
            pass
        while self.count < self.teeth / 5:
            while self.io.value() != edge:
                ...
            while self.io.value() == edge:
                ...
            self.count += 1
        
    def value(self):
        deadline = ticks_add(ticks_us(), self.timeout)
        while ticks_diff(deadline, ticks_us()) > 0:
            self.calc()
            
            #self.rpm = int(self.teeth / self.resolution * 15000000 / duration)
        #print(f"{self.count}")
        return self.rpm

class Rotary_Sensor:
    def __init__(self, pin: Pin) -> None:
        self.adc = ADC(Pin(pin))

    def value(self, sensMap: list) -> int:
        r = self.adc.read()
        if not r:
            return 0
        for i, val in enumerate(sensMap):
            if r <= val:
                return i

class Read:
    adjPS = Rotary_Sensor('X19')
    adjTCC = Rotary_Sensor('X20')

    ps1 = Pressure_Sensor('X17')
    ps2 = Pressure_Sensor('X18')

    tft = Temp_Sensor('Y11', 30, 100)

    #oss = Speed_Sensor('X19')
    #iss = Speed_Sensor('X20')

    def __init__(self, state: State) -> None:
        self.state = state
    
    async def update(self) -> None:
        while True:
            #for loop for getting sensor data
            self.state.rpm = random.randint(0, 5400)
            self.state.adjTCC = self.adjTCC.value(Data.tccMap)
            self.state.adjPS = self.adjPS.value(Data.psMap)
            self.state.ps1 = self.ps1.value()
            self.state.ps2 = self.ps2.value()
            self.state.tft = self.tft.value()

            await uasyncio.sleep_ms(40)