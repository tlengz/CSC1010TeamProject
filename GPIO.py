from gpiozero import LED # sudo pip3 install rpi.gpio
                         # sudo pip3 install        gpiozero
                         # sudo apt install python3-gpiozero
from time import sleep

count = 0
turnOn = True
if turnOn:
    try:
        #led = LED("GPIO17")
        led = LED(17)
        while True and count < 3:
            led.on()
            sleep(1)
            led.off()
            sleep(1)
            count += 1
            print(count)
        led.off()
    except Exception as e:
        print(e)
else:
    LED("GPIO4").off()
    LED(4).off()
