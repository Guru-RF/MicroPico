import time
import board
import busio
import digitalio
import adafruit_rfm9x
import EasyCrypt

print("Intializing µPico")

RADIO_FREQ_MHZ = 433.775
CS = digitalio.DigitalInOut(board.GP21)
RESET = digitalio.DigitalInOut(board.GP20)
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Initialze RFM radio with a more conservative baudrate
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 5

#
rfm9x.signal_bandwidth = 125000
rfm9x.coding_rate = 5
rfm9x.spreading_factor = 7
#rfm9x.enable_crc = True

while True:
    #packet = rfm9x.receive(timeout=0.5)
    packet = rfm9x.receive(keep_listening=True, with_header=False, with_ack=False, timeout=None)
    if packet is not None:
        print("Received (raw): {0}".format(packet))


    



