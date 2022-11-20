import adafruit_bme680
import time
import busio
import board

# Create the I2C interface.
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

while not i2c.try_lock():
    pass

try:
    while True:
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in i2c.scan()],
        )
        time.sleep(2)

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()
