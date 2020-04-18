#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

ledPins = [11, 12, 13, 15, 16, 18, 22, 3, 5, 24]

sleepTime = 0.05


def oddLedBarGraph():
    for i in range(5):
        j = i * 2
        GPIO.output(ledPins[j], GPIO.HIGH)
        time.sleep(sleepTime)
        GPIO.output(ledPins[j], GPIO.LOW)


def evenLedBarGraph():
    for i in range(5):
        j = i * 2 + 1
        GPIO.output(ledPins[j], GPIO.HIGH)
        time.sleep(sleepTime)
        GPIO.output(ledPins[j], GPIO.LOW)


def allLedBarGraph():
    for i in ledPins[1:-1]:
        GPIO.output(i, GPIO.HIGH)
        time.sleep(sleepTime)
        GPIO.output(i, GPIO.LOW)
    ledPins.reverse()
    for i in ledPins[1:-1]:
        GPIO.output(i,GPIO.HIGH)
        time.sleep(sleepTime)
        GPIO.output(i,GPIO.LOW)
        # print(last)
    ledPins.reverse()

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)        # Numbers GPIOs by physical location
    for i in ledPins:
        GPIO.setup(i, GPIO.OUT)   # Set all ledPins' mode is output
        GPIO.output(i, GPIO.LOW) # Set all ledPins to high(+3.3V) to off led

def loop():
    while True:
        # oddLedBarGraph()
        # time.sleep(2)
        # evenLedBarGraph()
        # time.sleep(2)
        allLedBarGraph()
        # time.sleep(1)

def destroy():
    for pin in ledPins:
        GPIO.output(pin, GPIO.LOW)    # turn off all leds
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
        destroy()
