from machine import Pin
import time

# define the pin number where the rain sensor is connected
rain_sensor_pin = 13

# create a pin object for the rain sensor pin
rain_sensor = Pin(rain_sensor_pin, Pin.IN)

while True:
    # read the state of the rain sensor pin
    is_raining = rain_sensor.value()

    if is_raining:
        print("It's not Raining.")
    else:
        print("It's Raining")

    # wait for 1 second before reading the state of the sensor again
    time.sleep(1)