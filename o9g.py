import uasyncio
from time import sleep_ms

#---User Modules
import View, Solenoid, Pin_IO, Sensors, Control, Data

async def main():
    current = Data.State()

    view = View.View(current)
    sol = Solenoid.Valve_Body(current)
    io = Pin_IO.Input(current)
    read = Sensors.Read(current)
    o9g = Control.Control(current)

    uasyncio.create_task(o9g.run())
    uasyncio.create_task(view.update())
    uasyncio.create_task(sol.adjust())
    uasyncio.create_task(io.evaluate())
    uasyncio.create_task(read.update())

    while True:        
        await uasyncio.sleep_ms(50)

#---Main Function---
if __name__=='__main__':
    uasyncio.run(main())