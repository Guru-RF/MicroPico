import board
import digitalio
import time

buttonENC= digitalio.DigitalInOut(board.GP16)
buttonENC.direction = digitalio.Direction.INPUT
buttonENC.pull = digitalio.Pull.UP

while True:
	print(buttonENC.value)
	time.sleep(2)
