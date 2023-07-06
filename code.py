import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import analogio
from ulab import numpy as np
import usb_cdc
import supervisor

print("---Pico Pad Keyboard---")



MEDIA = 1
KEY = 2

adc0 = analogio.AnalogIn(board.A3)
adc1 = analogio.AnalogIn(board.A2)
adc2 = analogio.AnalogIn(board.A1)
adc3 = analogio.AnalogIn(board.A0)

m = 65520
usbl = usb_cdc.data

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

pins = (
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
)


keymap = {
    (0): (KEY, [Keycode.F13]),
    (1): (KEY, [Keycode.F16]),
    (2): (KEY, [Keycode.F19]),
    (3): (KEY, [Keycode.F14]),
    (4): (KEY, [Keycode.F17]),
    (5): (KEY, [Keycode.F20]),
    (6): (KEY, [Keycode.F15]),
    (7): (KEY, [Keycode.F18]),
    (8): (KEY, [Keycode.F21]),
    (9): (MEDIA, ConsumerControlCode.SCAN_PREVIOUS_TRACK),
    (10): (MEDIA, ConsumerControlCode.PLAY_PAUSE),
    (11): (MEDIA, ConsumerControlCode.SCAN_NEXT_TRACK),  # plus key
    
}

num = [1,2,3]
same = [[],[],[]]
di = {1:same[0],2:same[1],3:same[2]}
di2 = {1:adc1,2:adc2,3:adc3}

switches = []
switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(len(pins)):
    switch = DigitalInOut(pins[i])
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    switches.append(switch)

def send_data(data):
    data = bytes(data+"\n", 'utf-8')
    usbl.write(data)

def read_data(i):
    data = usbl.readline(i)
    
    return data


def adc():
    time.sleep(0.03)
    for i in num:
        val = int(abs(np.ceil((abs((di2[i].value) - m) / m) *100 + 0.5)-101))
        if val > 100:
            val = 100

        if val in di[i]:
            di[i].clear()
            di[i].append(val)
            d = 0
        else:
            print(f"ADC{i}:{val}")
            send_data(f"ADC{i}:{val}")
            di[i].append(val)
            if usbl.connected != True:
                supervisor.reload()






def mkey():
    for button in range(12):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][1])
                        print(keymap[button][1])
                    else:
                        cc.send(keymap[button][1])
                except ValueError:  # deals with six key limit
                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][1])

                except ValueError:
                    pass
                switch_state[button] = 0
    time.sleep(0.01) 



def start():
    while 1:
        adc()
        mkey()

def only_key():
    mkey()

usbl.flush()
while 1:
    if usbl.connected:
        i =usb_cdc.data.in_waiting
        if i> 0:
            data = read_data(i)
            print(data)
            if data == b'Creams\n':
                send_data("productions")
                print('productions')
                time.sleep(1)
                start()
            else:
                send_data("kanker op")
                mkey()

        else:
            pass
    else:
        mkey()