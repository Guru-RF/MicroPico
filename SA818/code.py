import board
from SA818 import SA818

radio = SA818(board.GP16, board.GP17, True) # debug
#radio = SA818(board.GP16, board.GP17) # normal

print(radio.getVersion()) # get firmware version
radio.setFilters(0,0,0) # emphasis, lowpass, highpass
radio.setFrequency(145.600) # set frequency
print(radio.getFrequency()) # get frequency
radio.tune()
radio.setVolume(8) # set Volume from 1 to 8
radio.setSquelch(8) # set Squelch from q to 8
#radio.setOffset(-6) # set the frequency split offset
#radio.setRxCTCSS(71.9)
#radio.setTxCTCSS(71.9)
radio.setRxDCS(25,"N")
radio.setTxDCS(25,"N")
#radio.disableTone()
