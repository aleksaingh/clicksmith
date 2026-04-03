import board
import digitalio
import usb_hid
import time
import microcontroller
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

PINS = [board.D7, board.D10, board.A0, board.D8, board.A1, board.A2, microcontroller.pin.GPIO4, board.A3, board.D5]

KEYS = [
    Keycode.ESCAPE, Keycode.SPACE, Keycode.THREE,
    Keycode.FOUR, Keycode.FIVE, Keycode.SIX,
    Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE
]

buttons = []
for pin in PINS:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append(btn)

led_r = digitalio.DigitalInOut(board.LED_RED)
led_r.direction = digitalio.Direction.OUTPUT
led_r.value = True

led_g = digitalio.DigitalInOut(board.LED_GREEN)
led_g.direction = digitalio.Direction.OUTPUT
led_g.value = True

led_b = digitalio.DigitalInOut(board.LED_BLUE)
led_b.direction = digitalio.Direction.OUTPUT
led_b.value = True

leds = [led_r, led_g, led_b]
color_index = 0

kbd = Keyboard(usb_hid.devices)
pressed = [False] * 9
last_debounce = [0] * 9
DEBOUNCE = 0.05

while True:
    now = time.monotonic()
    for i, btn in enumerate(buttons):
        if not btn.value and not pressed[i] and now - last_debounce[i] > DEBOUNCE:
            kbd.press(KEYS[i])
            pressed[i] = True
            last_debounce[i] = now
            leds[color_index].value = False
        elif btn.value and pressed[i] and now - last_debounce[i] > DEBOUNCE:
            kbd.release(KEYS[i])
            pressed[i] = False
            last_debounce[i] = now
            leds[color_index].value = True
            color_index = (color_index + 1) % 3
    time.sleep(0.001)