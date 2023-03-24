import time
import board
import busio
import digitalio
import adafruit_rfm9x
import EasyCrypt

print("Intializing µPico")

RADIO_FREQ_MHZ = 868.0
CS = digitalio.DigitalInOut(board.GP21)
RESET = digitalio.DigitalInOut(board.GP20)
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Initialze RFM radio with a more conservative baudrate
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 5

#
rfm9x.signal_bandwidth = 62500
rfm9x.coding_rate = 6
rfm9x.spreading_factor = 8
rfm9x.enable_crc = True

file = open("localcounter", "r")
count = int(file.read())
file.close()
toggle = False
port = 1
while True:
    count = count+1
    value = str(count) + ',SW,' + str(port) + ',' + str(toggle)
    if toggle is False:
        toggle = True
    else:
        toggle = False
        port = port + 1
    if port is 5:
        port = 1
    key = '821ccb7eb5157bb2'
    ivs = "aba0a3bde34a03487eda3ec96d5736a8"
    encrypted = EasyCrypt.encrypt_string(key, value, ivs)

    print("Send (encrypted): {0}".format(value))
    rfm9x.send(encrypted)
        
    time_now = time.monotonic()
    packet = rfm9x.receive(timeout=0.5)
    if packet is not None:
        print("Received (raw): {0}".format(packet))
        decrypted = EasyCrypt.decrypt_string(key, packet, ivs)
        if decrypted is not False:
            print("Received (decrypted): {0}".format(decrypted))
    sleeptime = max(0, 0.45 - (time.monotonic() - time_now)) 
    time.sleep(sleeptime)


    



