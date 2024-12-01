'''
**********************************************************************
* Filename    : dht11.py
* Description : test for SunFoudner DHT11 humiture & temperature module
* Author      : sunfounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-09-30    New release
**********************************************************************
'''
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import os
import datetime
import csv

dhtPin = 17

GPIO.setmode(GPIO.BCM)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5


def readDht11():
    GPIO.setup(dhtPin, GPIO.OUT)
    GPIO.output(dhtPin, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(dhtPin, GPIO.LOW)
    time.sleep(0.02)
    GPIO.setup(dhtPin, GPIO.IN, GPIO.PUD_UP)

    unchanged_count = 0
    last = -1
    data = []
    while True:
        current = GPIO.input(dhtPin)
        data.append(current)
        if last != current:
            unchanged_count = 0
            last = current
        else:
            unchanged_count += 1
            if unchanged_count > MAX_UNCHANGE_COUNT:
                break

    state = STATE_INIT_PULL_DOWN

    lengths = []
    current_length = 0

    for current in data:
        current_length += 1

        if state == STATE_INIT_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_INIT_PULL_UP
            else:
                continue
        if state == STATE_INIT_PULL_UP:
            if current == GPIO.HIGH:
                state = STATE_DATA_FIRST_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_FIRST_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_DATA_PULL_UP
            else:
                continue
        if state == STATE_DATA_PULL_UP:
            if current == GPIO.HIGH:
                current_length = 0
                state = STATE_DATA_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_PULL_DOWN:
            if current == GPIO.LOW:
                lengths.append(current_length)
                state = STATE_DATA_PULL_UP
            else:
                continue
    if len(lengths) != 40:
        #print ("Data not good, skip")
        return False

    shortest_pull_up = min(lengths)
    longest_pull_up = max(lengths)
    halfway = (longest_pull_up + shortest_pull_up) / 2
    bits = []
    the_bytes = []
    byte = 0

    for length in lengths:
        bit = 0
        if length > halfway:
            bit = 1
        bits.append(bit)
    #print ("bits: %s, length: %d" % (bits, len(bits)))
    for i in range(0, len(bits)):
        byte = byte << 1
        if (bits[i]):
            byte = byte | 1
        else:
            byte = byte | 0
        if ((i + 1) % 8 == 0):
            the_bytes.append(byte)
            byte = 0
    #print (the_bytes)
    checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] +
                the_bytes[3]) & 0xFF
    if the_bytes[4] != checksum:
        #print ("Data not good, skip")
        return False

    return the_bytes[0], the_bytes[1], the_bytes[2], the_bytes[3]


def main():
    dir_path = os.path.dirname(__file__)
    file_name = 'DHT_log.csv'
    if not os.path.exists(f'{dir_path}/{file_name}'):
        pass
        # create
        # datetime.datetime.now()
        with open(f'{dir_path}/{file_name}', 'x') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=",", quotechar='"')
            filewriter.writerow(['datetime', 'humidity', 'temperature'])

    with open(f'{dir_path}/{file_name}', 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=",", quotechar='"')
        while True:
            result = readDht11()
            if result:
                datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                humidity, temperature = float(f'{result[0]}.{result[1]}'), float(
                    f'{result[2]}.{result[3]}')
                print(
                    f'datetime_str: {datetime_str} / result: {result} / humidity: {humidity}%, temperature: {temperature}ºC', flush=True)
                filewriter.writerow([datetime_str, humidity, temperature])
                csvfile.flush()  # Writes the output to the file, otherwise it get written when the program ends only
            time.sleep(60)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()