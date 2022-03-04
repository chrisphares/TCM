from pyb import SPI
from time import sleep_ms
from pyb import Pin

#---User Modules
from LED import NeoPixel, DotStar
from Data import Data

class View:
    def __init__(self):
        spi = SPI(1, SPI.CONTROLLER, baudrate=42_000_000)
        self.matrix = DotStar(spi, 64)
        self.led_1 = Pin('Y8', Pin.OUT)
        self.ledstrip=NeoPixel(self.led_1, 10)
        self.lastRPM = 0
        self.lastGear = None
        
    def show_rpm(self, r):
        self.updateStrip(self.ledstrip, Data.RPM[r])
    
    def show_kitt(self, kitt):
        if kitt < len(Data.KITT):
            self.updateStrip(self.ledstrip, Data.KITT[kitt])
            self.kitt += 1
        else:
            self.kitt = 0
            self.updateStrip(self.ledstrip, Data.KITT[0])
            
    def updateStrip(self, l, a):
        for i in range(l.n):
            l[i] = a[i]
        l.write()

    def updateMatrix(self, gear):
        d = Data.R + Data.SPACE + Data.N10
        for i in range(len(d)):
            self.matrix[i] = d[i]
    
    def update(self, rpm, g, l):
        rpm = int(rpm / 500) * 500
        if not rpm == self.lastRPM:
            self.lastRPM = rpm
            self.show_rpm(self.lastRPM)
        #self.updateMatrix(g)
        #print(f"rpm:{r} gear:{g} lock:{l}")