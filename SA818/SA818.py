import board
import busio
import time

CTCSS = (
  "None", "67.0", "71.9", "74.4", "77.0", "79.7", "82.5", "85.4", "88.5",
  "91.5", "94.8", "97.4", "100.0", "103.5", "107.2", "110.9", "114.8", "118.8",
  "123.0", "127.3", "131.8", "136.5", "141.3", "146.2", "151.4", "156.7",
  "162.2", "167.9", "173.8", "179.9", "186.2", "192.8", "203.5", "210.7",
  "218.1", "225.7", "233.6", "241.8", "250.3"
)

DCS_CODES = [
  "023", "025", "026", "031", "032", "036", "043", "047", "051", "053", "054",
  "065", "071", "072", "073", "074", "114", "115", "116", "125", "131", "132",
  "134", "143", "152", "155", "156", "162", "165", "172", "174", "205", "223",
  "226", "243", "244", "245", "251", "261", "263", "265", "271", "306", "311",
  "315", "331", "343", "346", "351", "364", "365", "371", "411", "412", "413",
  "423", "431", "432", "445", "464", "465", "466", "503", "506", "516", "532",
  "546", "565", "606", "612", "624", "627", "631", "632", "654", "662", "664",
  "703", "712", "723", "731", "732", "734", "743", "754"
]

BAUD_RATES = [300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

DEFAULT_BAUDRATE = 9600

class SA818:
  EOL = "\r\n"
  INIT = "AT+DMOCONNECT"
  SETGRP = "AT+DMOSETGROUP"
  FILTER = "AT+SETFILTER"
  VOLUME = "AT+DMOSETVOLUME"
  TAIL = "AT+SETTAIL"
  NARROW = 0
  READ_TIMEOUT = 3.0
    
  frequency = 145.450
  ctcss = None  
  rx_tone = '0000'
  tx_tone = '0000'
  offset = 0
  bw = 0 # 0=NARROW (12.5KHz), 1=WIDE (25KHz)
  squelch = 1 # between 1 and 8
  closetail = None # or 0 or 1
  debug = False

  def __init__(self, tx=board.GP16, rx=board.GP17, debug=False, baud=DEFAULT_BAUDRATE):
    self.uart = busio.UART(tx, rx, baudrate=baud, bits=8, timeout=self.READ_TIMEOUT, stop=1, parity=None)
    self.debug = debug

    self.send(self.INIT)
    reply = self.readline()
    if reply != "+DMOCONNECT:0":
      raise SystemError('Connection error')

  def close(self):
    self.uart.close()

  def send(self, *args):
    data = ','.join(args)
    if self.debug is True:
        print('Sending: ' + data)
    data = bytes(data + self.EOL, 'ascii')
    self.uart.write(data)

  def readline(self):
    line = self.uart.readline()
    line = line.decode('ascii')
    return line.rstrip()

  def getVersion(self):
    self.send("AT+VERSION")
    time.sleep(0.5)
    reply = self.readline()
    try:
      _, version = reply.split('_')
    except ValueError:
      return('Unable to decode the firmware version')
    else:
      return version
  
  def setFrequency(self, freq):
    self.frequency = freq
    return self.frequency
  
  def getFrequency(self):
    return self.frequency

  def tune(self):
    if self.ctcss is None:
      tx_tone, rx_tone = ['0000', '0000']
    else:
      tx_tone = self.tx_tone
      rx_tone = self.rx_tone

    if self.offset == 0.0:
      tx_freq = rx_freq = "{:.4f}".format(self.frequency)
    else:
      rx_freq = "{:.4f}".format(self.frequency)
      tx_freq = "{:.4f}".format(self.frequency + self.offset)

    cmd = "{}={},{},{},{},{},{}".format(self.SETGRP, self.bw, tx_freq, rx_freq,
                                        tx_tone, self.squelch, rx_tone)
    self.send(cmd)
    time.sleep(1)
    response = self.readline()
    if response != '+DMOSETGROUP:0':
      if self.debug is True:
        print('SA818 programming error' + response)
      return False

    if self.closetail is not None and self.ctcss is not None:
      self.close_tail()
    elif self.closetail is not None:
      if self.debug is True:
        print('Ignoring "--close-tail" specified without ctcss')
    
    return True

  def setFilters(self, emphasis, highpass, lowpass):
    # filters are pre-emphasis, high-pass, low-pass
    cmd = "{}={},{},{}".format(self.FILTER, int(not emphasis),
                               int(highpass), int(lowpass))
    self.send(cmd)
    time.sleep(1)
    response = self.readline()
    if response != "+DMOSETFILTER:0":
      return False
    else:
      return True

  def setVolume(self, level):
    cmd = "{}={:d}".format(self.VOLUME, level)
    self.send(cmd)
    time.sleep(1)
    response = self.readline()
    if response != "+DMOSETVOLUME:0":
      if self.debug is True:
        print('SA818 set volume error')
      return False
    else:
      return True
  
  def setSquelch(self, level):
    self.squelch = level
    return self.tune()
  
  def setTxCTCSS(self, inttone):
    tone = str(inttone)
    if tone not in CTCSS:
      return False
    ctcss = CTCSS.index(tone)
    self.tx_tone = f"{ctcss:04d}"
    self.ctcss = True
    return self.tune()
  
  def setRxCTCSS(self, inttone):
    tone = str(inttone)
    if tone not in CTCSS:
      return False
    ctcss = CTCSS.index(tone)
    self.rx_tone = f"{ctcss:04d}"
    self.ctcss = True
    return self.tune()
  
  def setTxDCS(self, inttone, direction):
    tone = "{:03d}".format(int(inttone))
    if direction is not "I" and direction is not "N":
      return False
    if tone not in DCS_CODES:
      return False
    self.tx_tone = "{:03d}".format(int(inttone)) + direction
    self.ctcss = True
    return self.tune()
  
  def setRxDCS(self, inttone, direction):
    tone = "{:03d}".format(int(inttone))
    if direction is not "I" and direction is not "N":
      return False
    if tone not in DCS_CODES:
      return False
    self.rx_tone = "{:03d}".format(int(inttone)) + direction
    self.ctcss = True
    return self.tune()
  
  def disableTone(self):
    self.ctcss = None
    self.tx_tone, self.rx_tone = ['0000', '0000']
    return self.tune()
  
  def setOffset(self, offset):
    self.offset = offset
    return self.tune()

  def close_tail(self):
    cmd = "{}={}".format(self.TAIL, int(self.closetail))
    self.send(cmd)
    time.sleep(1)
    response = self.readline()
    if response != "+DMOSETTAIL:0":
      if self.debug is True:
        print('SA818 set filter error')
      return False
    else:
      return True