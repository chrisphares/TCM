import uasyncio
from pyb import SPI
from time import sleep_ms
from pyb import Pin

#---User Modules
from LED import NeoPixel, DotStar
from Data import Data

class View:
    def __init__(self, state):
        self.state = state
        spi = SPI(1, SPI.CONTROLLER, baudrate=42_000_000)
        self.matrix = DotStar(spi, 64)
        self.led_1 = Pin('X10', Pin.OUT)
        self.ledstrip=NeoPixel(self.led_1, 10)
    
    def convert_rpm(self, rpm: int):
        return int(rpm / 500) * 500
        
    def show_rpm(self, rpm: int):
        self.updateStrip(self.ledstrip, Data.RPM[rpm])

    def show_kitt(self, kitt):
        if kitt < len(Data.KITT):
            self.updateStrip(self.ledstrip, Data.KITT[kitt])
            self.kitt += 1
        else:
            self.kitt = 0
            self.updateStrip(self.ledstrip, Data.KITT[0])
            
    def updateStrip(self, l, a): #l = length, a = colors
        for i in range(l.n):
            l[i] = a[i]
        l.write()

    def updateMatrix(self, gear):
        d = Data.R + Data.SPACE + Data.N10 #this is testing
        for i in range(len(d)):
            self.matrix[i] = d[i]
    
    async def update(self):
        while True:
            rpm = self.convert_rpm(self.state.rpm)
            self.show_rpm(rpm)

            #self.updateMatrix(1)
            print(f"shiting: {self.state.shifting} gear: {self.state.gear} | selectGear: {self.state.selectGear} | paddleGear: {self.state.paddleGear} | PS: {self.state.adjPS} | TC: {self.state.adjTCC}")
            await uasyncio.sleep_ms(40)