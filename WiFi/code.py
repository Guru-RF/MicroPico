import board
import busio
from digitalio import DigitalInOut

from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests

print("Raspberry Pi RP2040 - ESP32SPI hardware test")

esp32_cs = DigitalInOut(board.GP17)
esp32_ready = DigitalInOut(board.GP20)
esp32_reset = DigitalInOut(board.GP21)

spi = busio.SPI(board.GP18, board.GP19, board.GP16)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version)
print("MAC addr:", [hex(i) for i in esp.MAC_address])

for ap in esp.scan_networks():
    print("\t%s\t\tRSSI: %d" % (str(ap['ssid'], 'utf-8'), ap['rssi']))

print("Done!")
