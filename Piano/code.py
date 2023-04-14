import time
import board
import simpleio
import touchio

cKey = touchio.TouchIn(board.GP21)


while True:
	print(cKey.raw_value)
	if cKey.value:
		simpleio.tone(board.GP10, 440, duration=0.25)
		print("Touched!")
	time.sleep(0.05)
