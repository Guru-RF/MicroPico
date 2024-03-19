import time
import busio
import board
import cedargrove_ad5245

ad5245 = cedargrove_ad5245.AD5245(address=0x2C)

while True:
	ad5245.wiper = 255
	print("Wiper set to %d"%ad5245.wiper)

	time.sleep(10)

	ad5245.wiper = 0
	print("Wiper set to %d"%ad5245.wiper)
	
	time.sleep(10)
