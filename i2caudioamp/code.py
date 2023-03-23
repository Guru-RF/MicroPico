import board
import cedargrove_ad5245
import simpleio
import time

ad5245 = cedargrove_ad5245.AD5245(address=0x2C)

ad5245.wiper = 255
print("Wiper set to %d"%ad5245.wiper)

while True:
	simpleio.tone(board.GP16, 523, duration=0.5)
	time.sleep(1)
