import board
import digitalio
import analogio

ledTopPico = digitalio.DigitalInOut(board.GP14)
ledTopPico.direction = digitalio.Direction.OUTPUT
ledTopPico.value = True

ledBottomPico = digitalio.DigitalInOut(board.GP13)
ledBottomPico.direction = digitalio.Direction.OUTPUT
ledBottomPico.value = True

buttonLeftPico = digitalio.DigitalInOut(board.GP18)
buttonLeftPico.direction = digitalio.Direction.INPUT
buttonLeftPico.pull = digitalio.Pull.UP

buttonRightPico = digitalio.DigitalInOut(board.GP19)
buttonRightPico.direction = digitalio.Direction.INPUT
buttonRightPico.pull = digitalio.Pull.UP
