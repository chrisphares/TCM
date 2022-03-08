from time import ticks_ms, ticks_diff, sleep_ms

#---user modules
from Solenoid import OnOff_Solenoid, PWM_Solenoid
from Pin_IO import Pin_IO, Adjust_IO
from Sensors import Pressure_Sensor, Temp_Sensor, Speed_Sensor
from Data import Data

#testing
import random

#---Control Class---
class Control:   
    OFF = const(0)
    ON = const(1)
    
    #/n90, n92, n282, n283/
    PARK = (OFF, OFF, ON, OFF, OFF, ON)
    REVERSE = (OFF, OFF, OFF, ON, ON, ON)
    NUETRAL = (OFF, OFF, ON, ON, ON, ON)
    FIRST = (ON, ON, OFF, ON, ON, ON)
    SECOND = (OFF, OFF, ON, OFF, ON, OFF)
    THIRD = (ON, ON, OFF, OFF, ON, ON)
    FOURTH = (ON, ON, ON, OFF, OFF, ON)
    FIFTH = (ON, ON, OFF, ON, OFF, ON)
    SIXTH = (ON, ON, ON, ON, OFF, OFF)
    DRIVE = FIRST #set this to second maybe?

    #on/off solenoids
    n88 = OnOff_Solenoid('X22', OFF)
    n89 = OnOff_Solenoid('X21', OFF)
    
    #control solenoids
    n90 = PWM_Solenoid('X4', 10, 10, 60)
    n92 = PWM_Solenoid('X2', 10, 20, 60)
    n282 = PWM_Solenoid('Y10', 10, 30, 60)
    n283 = PWM_Solenoid('Y9', 10, 40, 90)

    #pressure solenoids
    n91 = PWM_Solenoid('X3', 50, 20, 60) #converter clutch
    n93 = PWM_Solenoid('X1', 60, 20, 60) #main line presssure

    #solenoids
    vb = (n88, n89, n90, n92, n282, n283)
    
    #gear selection inputs
    parkIO = Pin_IO('Y6', 250, PARK)
    reverseIO = Pin_IO('Y7', 250, REVERSE)
    nuetralIO = Pin_IO('Y8', 100, NUETRAL)
    driveIO = Pin_IO('X9', 100, DRIVE)
    
    #paddle gear inputs
    upIO = Pin_IO('Y2', 15, 'up')
    downIO = Pin_IO('Y3', 15, 'dn')
    
    #TC Lock button input
    lockIO = Pin_IO('Y1', 15, 'tcc')

    #pressure adjustment rotary inputs
    adjPS = Adjust_IO('X11')
    adjTCC = Adjust_IO('X12')

    #input array
    inputs = (
        parkIO,
        reverseIO,
        nuetralIO,
        driveIO,
        upIO,
        downIO,
        lockIO,
        )

    ps1 = Pressure_Sensor('X17')
    ps2 = Pressure_Sensor('X18')
    tft = Temp_Sensor('Y11', 30, 100)
    #oss = Speed_Sensor('X6')
    #iss = Speed_Sensor('X7')

    def __init__(self):# add rpm/oss for overrev protection & init gear selection       
        self.rpm = 0
        self.gear = None
        self.lock = OFF #range of 0-10?
            
    def set_input_flags(self):
        for i, io in enumerate(self.inputs):
            reading = io.value()
            if reading != io.lastInputState:
                io.lastDebounceTime = ticks_ms()
            debounce = ticks_diff(ticks_ms(), io.lastDebounceTime)
            if debounce > io.delay:
                io.inputFlags = reading
                    
            io.lastInputState = reading

    def resolve_input_flags(self):
        for i, io in enumerate(self.inputs):
            if not io.inputFlags:
                io.press(self.vb)
                print(f"{i=}")

    def set_pwm_sol(self, pwmSol, target):
        pwmSol.set_ps(target)#slow thi down for real/asyncio

    def get_adj_value(self, io):
        return io.value()

    def run(self):
        self.set_input_flags()
        self.resolve_input_flags()
        
        self.set_pwm_sol(self.n91, self.get_adj_value(self.adjPS))
        if self.lock:
            self.set_pwm_sol(self.n93, self.get_adj_value(self.adjTCC))

        #testing:
        self.rpm = random.randint(0, 5400)