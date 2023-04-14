import board
import countio
import time

# Count rising edges only.
pin_counter = countio.Counter(board.GP17, edge=countio.Edge.RISE)
# Reset the count after 100 counts.
oldtime=time.monotonic()
while True:
    time.sleep(0.001)
    if pin_counter.count >= 500:
	    oldcount=0
	    while pin_counter.count >= 2000:
		pin_counter.reset()
		time.sleep(0.3)
		count=(float(pin_counter.count)/(time.monotonic()-oldtime))*80
		count=count/1000
		if count >= oldcount:
			print(count) 
		oldcount=count

    oldcount=0
    pin_counter.reset()
    oldtime=time.monotonic()

