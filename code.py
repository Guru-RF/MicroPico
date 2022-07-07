import supervisor
import asyncio
import time
import µPICO
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode


async def buttonTask(cc):
    while (True):
        await asyncio.sleep(0.2)
        if µPICO.buttonLeftPico.value is False:
            print("ButtonLeft Pressed!")
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        if µPICO.buttonRightPico.value is False:
            print("ButtonRight Pressed!")
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)

async def blinkyTask():
    while (True):
        µPICO.ledTopPico.value = True
        await asyncio.sleep(1)
        µPICO.ledTopPico.value = False
        await asyncio.sleep(1)
        µPICO.ledBottomPico.value = True
        await asyncio.sleep(1)
        µPICO.ledBottomPico.value = False
        await asyncio.sleep(1)

async def main():
    print("Intializing µPico")
    time.sleep(1)

    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    cc = ConsumerControl(usb_hid.devices)
    time.sleep(1)


    if supervisor.runtime.usb_connected:
        supervisor.disable_autoreload()

    print("Lets go async !")

    loop = asyncio.get_event_loop()


    loop = asyncio.get_event_loop()
    button_task = asyncio.create_task(buttonTask(cc))
    blinky_task = asyncio.create_task(blinkyTask())

    loop.run_until_complete(button_task)
    loop.close()


asyncio.run(main())
