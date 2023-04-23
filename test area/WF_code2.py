from machine import Pin
import time

def measure_flow(pin_no):
    flow_sensor_pin = Pin(pin_no, Pin.IN)
    total_water = 0
    flow_rate = 0
    last_time = 0
    pulses = 0
    last_pin_state = 0

    while True:
        pin_state = flow_sensor_pin.value()

        if pin_state != last_pin_state:
            if pin_state == 1:
                pulses += 1

        last_pin_state = pin_state

        current_time = time.ticks_ms()

        if current_time - last_time > 1000:
            duration = current_time - last_time
            flow_rate = (pulses / duration) * 1000 * 60 / 600 # liters per minute
            total_water += (pulses / 600) # total liters passed
            pulses = 0
            last_time = current_time

            print("Flow rate: {:.2f} L/min, Total water passed: {:.2f} L".format(flow_rate, total_water))
            return total_water, flow_rate
        







