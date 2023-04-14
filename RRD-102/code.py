import busio, board
from TEA5767 import Radio
    
i2c = busio.I2C(scl=board.GP21, sda=board.GP20, frequency=400000)
radio = Radio(i2c, freq=102.1)

print(f'Frequency: FM {radio.frequency}')
print(f'Ready: {radio.is_ready}')
print(f'Stereo: {radio.is_stereo}')
print(f'DC level: {radio.signal_adc_level}')
