from time import sleep_ms

#---User Modules
import View, Control

def main():
    view = View.View()#, oss, iss)
    o9g = Control.Control()

    while True:
        o9g.run()
        view.update(o9g.rpm, o9g.gear, o9g.lock)
        sleep_ms(50) #slow for testing

#---Main Function---
if __name__=='__main__':
    main()