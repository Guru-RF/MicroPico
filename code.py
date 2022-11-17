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
from rainbowio import colorwheel


async def buttonTask(cc):
    while (True):
        await asyncio.sleep(0.1)
        if µPICO.buttonLeft.value is False:
            print("ButtonLeft Pressed!")
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        if µPICO.buttonRight.value is False:
            print("ButtonRight Pressed!")
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)

async def buzzerTask():
    while (True):
	for f in (262, 294, 330, 349, 392, 440, 494, 523):
		simpleio.tone(board.GP10, f, duration=0.25)
        await asyncio.sleep(5)

async def blinkyTask():
    while (True):
	for i in range(255):
		i = (i + 1) % 256
		µPICO.RGBled1.color = colorwheel(i)
		await asyncio.sleep(0.01)

async def blinkyTaskTwo():
    while (True):
	for i in range(255):
		i = (i + 1) % 256
		µPICO.RGBled2.color = colorwheel(i)
		await asyncio.sleep(0.01)

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
    blinky_task = asyncio.create_task(blinkyTask())
    blinky_task_two = asyncio.create_task(blinkyTaskTwo())
    buzzer_task = asyncio.create_task(buzzerTask())

    loop.run_until_complete(button_task)
    loop.close()


asyncio.run(main())
