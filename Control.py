from time import ticks_ms, ticks_diff, sleep_ms

#---user modules
from Solenoid import OnOff_Solenoid, Pressure_Solenoid, Control_Solenoid
from Pin_IO import Pin_IO, Select_IO, Drive_IO, Paddle_Up_IO, Paddle_Down_IO, Adjust_IO
from Sensors import Pressure_Sensor, Temp_Sensor, Speed_Sensor
from Data import Data

#testing
import random

#---Control Class---
class Control:   
    OFF = const(0)
    ON = const(1)
    
    #/n90, n92, n282, n283/
    park = (ON, OFF, OFF, ON)
    reverse = (OFF, ON, ON, ON)
    nuetral = (ON, ON, ON, ON)
    first = (OFF, ON, ON, ON)
    second = (ON, OFF, ON, OFF)
    third = (OFF, OFF, ON, ON)
    fourth = (ON, OFF, OFF, ON)
    fifth = (OFF, ON, OFF, ON)
    sixth = (ON, ON, OFF, OFF)
    drive = first #set this to second maybe?

    def __init__(self):# prolly oss for overrev protection        
        
        #/pin, blahhh
        self.n88 = OnOff_Solenoid('X22', OFF)
        self.n89 = OnOff_Solenoid('X21', OFF)
        
        self.n90 = Control_Solenoid('X4', 10, 60)
        self.n92 = Control_Solenoid('X2', 20, 60)
        self.n282 = Control_Solenoid('Y10', 30, 60)
        self.n283 = Control_Solenoid('Y9', 40, 90)

        #all but the pwm solenoids
        self.vb = (self.n90, self.n92, self.n282, self.n283)#class or tuple??

        self.n91 = Pressure_Solenoid('X3', 50)
        self.n93 = Pressure_Solenoid('X1', 60)
        
        #/pin, delay, Gear/
        self.parkIO = Select_IO('Y2', 250, self.park)
        self.reverseIO = Select_IO('Y3', 250, self.reverse)
        self.nuetralIO = Select_IO('Y6', 100, self.nuetral)
        self.driveIO = Drive_IO('Y7', 100, self.drive)
        
        #/pin, delay/
        self.upIO = Paddle_Up_IO('Y12', 15)
        self.downIO = Paddle_Down_IO('Y11', 15)
        
        self.lockIO = Pin_IO('Y1', 15)

        self.adj_ps = Adjust_IO('X11')
        self.adj_tcc = Adjust_IO('X12')
                
        self.inputs = (
            self.parkIO,
            self.reverseIO,
            self.nuetralIO,
            self.driveIO,
            self.upIO,
            self.downIO,
            self.lockIO,
            )
        
        #self dot?
        ps1 = Pressure_Sensor('X17') #//change to onoff input only
        ps2 = Pressure_Sensor('X18') #//change to onoff input only
        tft = Temp_Sensor('Y12', 30, 100)
        #oss = Speed_Sensor('X6')
        #iss = Speed_Sensor('X7')

        self.rpm = 0
        self.gear = None
        self.lock = OFF #range of 0-10?
            
    def setInputFlags(self):
        for i, io in enumerate(self.inputs):
            reading = io.value()
            if reading != io.lastInputState:
                io.lastDebounceTime = ticks_ms()
            debounce = ticks_diff(ticks_ms(), io.lastDebounceTime)
            if debounce > io.delay:
                io.inputFlags = reading
                    
            io.lastInputState = reading

    def resolveInputFlags(self):
        for i, io in enumerate(self.inputs):
            if io.inputFlags and not (io is self.lockIO):
                (io.press(self.vb))
                    
            if io.inputFlags and (io is self.lockIO):
                self.lock = ON
            if not io.inputFlags and (io is self.lockIO):
                self.lock = OFF

    def adjustMain(self):
        #value = 50 # test sensor value
        #self.n93.setPS(value)
        print(f"main ps: {self.adj_ps.value()}")

    def adjustTC(self):
        if not self.lock:
            pass
        else:

        #value = 30
        #self.n91.setPS(value)#get a value and actually adjust?        
            print(f"TCC switcher: {self.adj_tcc.value()}")

    def getADJValues(self):
        pass
        #if tc on


    def run(self):
        self.setInputFlags()
        self.resolveInputFlags()
        
        self.adjustMain()
        self.adjustTC() 

        #testing:
        self.rpm = random.randint(0, 5500)                                                                                                                                                                                                                                                      