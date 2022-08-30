import uasyncio
from time import sleep_ms

#---User Modules
import View, ValveBody, Pin_IO, Sensors, Data

class State:
    def __init__(self) -> None:
        self.rpm = 0
        self.lock = False
        self.lockDelay = 500
        self.lockDelayTime = None
        self.shifting = False
        self.shiftStage = 0
        self.selectGear = None
        self.paddleGear = None
        self.gear = None
        self.nextGear = None
        self.adjPS = 0
        self.adjTCC = 0
        self.ps1 = 0
        self.ps2 = 0
        self.tft = 0

async def main() -> None:
    state = State()

    #standardise this crap
    view = View.View(state)
    vb = ValveBody.Valve_Body(state)
    io = Pin_IO.Input(state)
    read = Sensors.Read(state)

    uasyncio.create_task(view.update())
    uasyncio.create_task(vb.adjust())
    uasyncio.create_task(io.get_input())
    uasyncio.create_task(read.update())

    while True:        
        await uasyncio.sleep_ms(20)

#---Main Function---
if __name__=='__main__':
    uasyncio.run(main())