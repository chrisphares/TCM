import uasyncio
from time import sleep_ms

#---User Modules
import View, ValveBody, Pin_IO, Sensors, Data

async def main():
    state = Data.State()

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