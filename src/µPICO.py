import board
import digitalio
import adafruit_rgbled

RGBled1 = adafruit_rgbled.RGBLED(board.GP14, board.GP13, board.GP12, invert_pwm=True)
RGBled2 = adafruit_rgbled.RGBLED(board.GP3, board.GP4, board.GP5, invert_pwm=True)

buttonLeft= digitalio.DigitalInOut(board.GP9)
buttonLeft.direction = digitalio.Direction.INPUT
buttonLeft.pull = digitalio.Pull.UP

buttonRight= digitalio.DigitalInOut(board.GP15)
buttonRight.direction = digitalio.Direction.INPUT
buttonRight.pull = digitalio.Pull.UP
