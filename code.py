import supervisor
import asyncio
import time
import µPICO
import board
import usb_hid
import simpleio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

async def buttonTask(cc):
    while (True):
        await asyncio.sleep(0.2)
        if µPICO.buttonLeft.value is False:
            print("ButtonLeft Pressed!")
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        if µPICO.buttonRight.value is False:
            print("ButtonRight Pressed!")
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)

async def buzzerTask():
    while (True):
        simpleio.tone(board.GP10, 440, duration=0.5)
        await asyncio.sleep(5)

#async def blinkyTask():
#    while (True):
#        µPICO.RGBled1.color = (255, 0, 0)
#        await asyncio.sleep(2)
#        µPICO.RGBled1.color = (0, 255, 0)
#        await asyncio.sleep(2)
#        µPICO.RGBled1.color = (0, 0, 255)
#        await asyncio.sleep(2)
#        µPICO.RGBled1.color = (0, 255, 255)
#        await asyncio.sleep(2)
#        µPICO.RGBled1.color = (255, 255, 0)
#        await asyncio.sleep(2)
#        µPICO.RGBled1.color = (255, 255, 255)
#        await asyncio.sleep(2)

async def main():
    print("Intializing µPico")
    time.sleep(1)

    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    cc = ConsumerControl(usb_hid.devices)
    time.sleep(1)

    print("Lets go async !")

    loop = asyncio.get_event_loop()
    button_task = asyncio.create_task(buttonTask(cc))
    #blinky_task = asyncio.create_task(blinkyTask())
    buzzer_task = asyncio.create_task(buzzerTask())

    loop.run_until_complete(button_task)
    loop.close()


asyncio.run(main())
