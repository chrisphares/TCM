import uasyncio
from time import sleep_ms

#---User Modules
import View, Solenoid, Pin_IO, Sensors, Data

async def main():
    current = Data.State()

    view = View.View(current)
    vb = Solenoid.Valve_Body(current)
    io = Pin_IO.Input(current)
    read = Sensors.Read(current)

    uasyncio.create_task(view.update())
    uasyncio.create_task(vb.adjust())
    uasyncio.create_task(io.get_input())
    uasyncio.create_task(read.update())

    while True:        
        await uasyncio.sleep_ms(40)

#---Main Function---
if __name__=='__main__':
    uasyncio.run(main())