from time import ticks_ms, ticks_diff, sleep_ms
import array

#---User Modules
import View
import Control

#---Main Function---
if __name__=='__main__':
    
    view = View.View()#, oss, iss)
    o9g = Control.Control()
    
    while True:
        o9g.run()
        view.update(o9g.rpm, o9g.gear, o9g.lock)
        sleep_ms(50) #slow for testing