import uasyncio
from Data import Data

#---Control Class---
class Control:
    def __init__(self, state):# add rpm/oss for overrev protection & init gear selection       
        self.current = state

    async def run(self):
        while True:
            if self.current.gear != self.current.selectGear:
                print(f"select from {self.current.gear} to {self.current.selectGear}")
                self.current.gear = self.current.selectGear

            # if self.current.selectGear == Data.PARK:
            #     if self.current.gear != self.current.nextGear:
            #         print(f"select from {self.current.gear} to {self.current.selectGear}")
            #         self.current.gear = self.current.nextGear


            await uasyncio.sleep_ms(40)