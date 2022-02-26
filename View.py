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
        
    def show_rpm(self, rpm):
        r = int(rpm / 500) * 500
        self.updateStrip(self.ledstrip, Data.RPM[r])
    
    def show_kitt(self, kitt):
        if kitt < len(Data.KITT):
            self.updateStrip(self.ledstrip, Data.KITT[kitt])
            self.kitt += 1
        else:
            self.kitt = 0
            self.updateStrip(self.ledstrip, Data.KITT[0])

        #if not selectGear == 0:
            #self.show_rpm(self.rpm)
        #else:
            #self.show_kitt(self.kitt)
            #sleep_ms(30)
            
    def updateStrip(self, l, a):
        for i in range(l.n):
            l[i] = a[i]
        l.write()

    def updateMatrix(self, gear):
        d = Data.R + Data.SPACE + Data.N10
        for i in range(len(d)):
            self.matrix[i] = d[i]
    
    def update(self, r, g, l):
        self.show_rpm(615)
        self.updateMatrix(g)
        print(f"rpm:{r} gear:{g} lock:{l}")