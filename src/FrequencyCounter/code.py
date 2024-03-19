import board
import countio
import time

# Count rising edges only.
pin_counter = countio.Counter(board.GP17, edge=countio.Edge.FALL)
# Reset the count after 100 counts.
oldtime=time.monotonic()
while True:
    if pin_counter.count >= 10:
	    oldcount=0
	    while pin_counter.count >= 20:	
		pin_counter.reset()
		time.sleep(1)
		count=(float(pin_counter.count)/(time.monotonic()-oldtime))
		count=(count/1000000)
		if count >= oldcount:
			if count > 1:
				print(count) 
		oldcount=count
	    print("reset")

    oldcount=0
    pin_counter.reset()
    oldtime=time.monotonic()

