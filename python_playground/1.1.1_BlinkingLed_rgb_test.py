#!/usr/bin/env python3
# FCG:
#   To be used with the RGB LED (Using pins: {'r':17, 'g':18, 'b':27})
#
# I learned that
#   - HIGH is 1, turned on
#   - LOW  is 0, turned off
import RPi.GPIO as GPIO
import time
LedPin = [17, 18, 27] #{'r':17, 'g':18, 'b':27}

print('GPIO.LOW',GPIO.LOW)
print('GPIO.HIGH',GPIO.HIGH)

def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set LedPin's mode to output,and initial level to High(3.3v)
    #GPIO.setup(LedPin, GPIO.OUT, initial=GPIO.HIGH)
    for p in LedPin:
        GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)

# Define a main function for main process
def main():
    while True:
        for p in LedPin:
            print ('...LED ON')
            # Turn on LED
            GPIO.output(p, GPIO.HIGH)
            time.sleep(0.5)
            print ('LED OFF...')
            # Turn off LED
            GPIO.output(p, GPIO.LOW)
            time.sleep(0.5)
            # break

# Define a destroy function for clean up everything after the script finished
def destroy():
    # Turn off LED
    #GPIO.output(LedPin, GPIO.HIGH)
    for p in LedPin:
        GPIO.output(p, GPIO.HIGH)
    # Release resource
    GPIO.cleanup()
# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        # pass
        main()
    # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()
