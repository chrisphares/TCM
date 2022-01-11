from time import sleep_ms
from pyb import Pin

#---User Modules
from LED import NeoPixel, DotStar

class View:
    def __init__(self):
        pass
        #self.c = Colors(0.1)#/?
        #self.spi = SPI(1, SPI.CONTROLLER, baudrate=42_000_000)
        #self.matrix = DotStar(spi, 64)
        #self.led_1 = Pin('X8', Pin.OUT)
        #self.ledstrip=NeoPixel(self.led_1, 10)
        
    def show_rpm(self, rpm):
        r = int(rpm / 500) * 500
        self.showLED(self.ledstrip, self.c.RPM[r])
    
    def show_kitt(self, kitt):
        if kitt < len(self.c.KITT):
            self.showLED(self.ledstrip, self.c.KITT[kitt])
            self.kitt += 1
        else:
            self.kitt = 0
            self.showLED(self.ledstrip, self.c.KITT[0])

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
        pass
    
    def update(self, r, g, l):
        #self.updateStrip(r)
        #self.updateMatrix(g)
        print(f"rpm:{r} gear:{g} lock:{l}")