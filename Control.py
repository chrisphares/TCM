from time import ticks_ms, ticks_diff, sleep_ms

#---user modules
from Solenoid import OnOff_Solenoid, Pressure_Solenoid, Control_Solenoid
from Pin_IO import Pin_IO, Select_IO, Drive_IO, Paddle_Up_IO, Paddle_Down_IO
from Sensors import Pressure_Sensor, Temp_Sensor, Speed_Sensor
from Data import Data

#---Control Class---
class Control:   
    OFF = const(0)
    ON = const(1)
    
    #/n88, n89, n90, n92, n282, n283/
    park = (OFF, OFF, ON, OFF, OFF, ON)
    reverse = (OFF, OFF, OFF, ON, ON, ON)
    nuetral = (OFF, OFF, ON, ON, ON, ON)
    first = (ON, ON, OFF, ON, ON, ON)
    second = (OFF, OFF, ON, OFF, ON, OFF)
    third = (ON, ON, OFF, OFF, ON, ON)
    fourth = (ON, ON, ON, OFF, OFF, ON)
    fifth = (ON, ON, OFF, ON, OFF, ON)
    sixth = (ON, ON, ON, ON, OFF, OFF)
    drive = first #set this to second maybe?

    def __init__(self):# prolly oss for overrev protection        
        
        #/pin, blahhh
        self.n88 = OnOff_Solenoid('X4', OFF)
        self.n89 = OnOff_Solenoid('X3', OFF)
        
        self.n90 = Control_Solenoid('Y1', 10, 60)
        self.n92 = Control_Solenoid('Y7', 10, 60)
        self.n282 = Control_Solenoid('X9', 10, 60)
        self.n283 = Control_Solenoid('X10', 10, 90)

        #all but the pressure solenoids
        self.vb = (self.n88, self.n89, self.n90, self.n92, self.n282, self.n283)#class or tuple??

        self.n91 = Pressure_Solenoid('Y2', 50)
        self.n93 = Pressure_Solenoid('Y8', 50)
        
        #/pin, delay, Gear/
        self.parkIO = Select_IO('X19', 250, self.park)
        self.reverseIO = Select_IO('X20', 250, self.reverse)
        self.nuetralIO = Select_IO('X21', 100, self.nuetral)
        
        self.driveIO = Drive_IO('X22', 100, self.drive)
        
        #/pin, delay/
        self.upIO = Paddle_Up_IO('X1', 15)
        self.downIO = Paddle_Down_IO('X2', 15)
        
        self.lockIO = Pin_IO('X7', 15)
        
        self.inputs = (
            self.parkIO,
            self.reverseIO,
            self.nuetralIO,
            self.driveIO,
            self.upIO,
            self.downIO,
            self.lockIO,
            )
        
        ps1 = Pressure_Sensor('X11', 20, 80) #main line pressure
        ps2 = Pressure_Sensor('X12', 12, 100) #lockup pressure
        tft = Temp_Sensor('Y12', 30, 100)
        #oss = Speed_Sensor('X6')
        #iss = Speed_Sensor('X7')
        
        self.rpm = 0
        self.gear = None
        self.lock = OFF
            
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
        value = 50 #sensor value?
        self.n93.setPS(value)

    def adjustTC(self):
        value = 30
        self.n91.setPS(value)#get a value and actually adjust?

    def run(self):
        self.setInputFlags()
        self.resolveInputFlags()
        
        self.adjustMain()
        self.adjustTC()
        self.reverseIO.press(self.vb)
        print(f"{self.vb[2].duty} {self.vb[3].duty} {self.vb[4].duty} {self.vb[5].duty}")