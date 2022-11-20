import adafruit_shtc3
import time
import busio
import board

# Create the I2C interface.
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

sht = adafruit_shtc3.SHTC3(i2c)

while True:
    temperature, relative_humidity = sht.measurements
    print("Temperature: %0.1f C" % temperature)
    print("Humidity: %0.1f %%" % relative_humidity)
    print("")
    time.sleep(1)


