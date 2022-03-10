import uasyncio

#---Control Class---
class Control:   
    def __init__(self, state):# add rpm/oss for overrev protection & init gear selection       
        self.current = state

    async def run(self):
        while True:
            # self.set_pwm_sol(self.n91, self.adjPS.value())
            # if self.lock:
            #     self.set_pwm_sol(self.n93, self.get_adj_value(self.adjTCC))

            await uasyncio.sleep_ms(50)