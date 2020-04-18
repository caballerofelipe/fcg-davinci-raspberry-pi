import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pins = [17, 18, 27, 22, 23, 24, 25, 2, 3, 8]
pwm = None
pwm = {}

# def setlight(pos): low, medium, high = 99, 70, 0; map(lambda pos: pwm[pos].ChangeDutyCycle(100), pwm); pwm[pos - 3].ChangeDutyCycle(low) if pos - 3 >= 0 and pos - 3 <= 9 else None; pwm[pos - 2].ChangeDutyCycle(low) if pos - 2 >= 0 and pos - 2 <= 9 else None; pwm[pos - 1].ChangeDutyCycle(medium) if pos - 1 >= 0 and pos - 1 <= 9 else None; pwm[pos].ChangeDutyCycle(high) if pos >= 0 and pos <= 9 else None; pwm[pos + 1].ChangeDutyCycle(medium) if pos + 1 >= 0 and pos + 1 <= 9 else None; pwm[pos + 2].ChangeDutyCycle(low) if pos + 2 >= 0 and pos + 2 <= 9 else None; pwm[pos + 3].ChangeDutyCycle(low) if pos + 3 >= 0 and pos + 3 <= 9 else None;

def setup():
    map(lambda p: pwmsetup(p[1], p[0], frequency=500, initial_duty_cycle=100), enumerate(pins))
    map(lambda pos: pwm[pos].ChangeDutyCycle(100), pwm)

def pwmsetup(p, key, frequency=2000, initial_duty_cycle=100):
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, GPIO.LOW)
    pwm[key] = None
    pwm[key] = GPIO.PWM(p, frequency)
    pwm[key].start(initial_duty_cycle)

def loop():
    # raw_input()
    pos = 0
    DutyCycle = [100] * 10
    decay=10
    while True:
        if pos == 0:
            delta = 1
        elif pos == 9:
            delta = -1
        DutyCycle = [dc+decay if dc<=(100-decay) else dc for dc in DutyCycle]
        DutyCycle[pos] = 0
        print(DutyCycle)
        for led,dc in enumerate(DutyCycle):
            pwm[led].ChangeDutyCycle(dc)
        pos = pos + delta
        # raw_input()
        time.sleep(0.1)

def destroy():
	for pin in pins:
		GPIO.output(pin, GPIO.LOW)    # turn off all leds
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
		destroy()
