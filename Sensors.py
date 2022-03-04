from pyb import ADC, Pin
from time import ticks_ms, ticks_us, ticks_diff, ticks_add

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
