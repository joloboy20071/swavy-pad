import supervisor
supervisor.set_usb_identification("Creams Productions","swavy pad" )
import usb_cdc

usb_cdc.enable(console=False, data=True)
import storage
import board
import digitalio

p1 = board.GP13

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button1 = digitalio.DigitalInOut(p1)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP



if button1.value:
    led.value = False
    storage.disable_usb_drive()
    
else :
    led.value = True
    storage.enable_usb_drive()



#