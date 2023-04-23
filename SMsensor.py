from machine import Pin, ADC
import time

# Set up the ADC pin
adc = ADC(Pin(13))

# Define a function to calculate the moisture percentage
def get_moisture():
    # Read the analog value from the ADC pin
    analog_value = adc.read()

    # Convert the analog value to a moisture percentage (assuming a linear relationship)
    moisture_percentage = ((4095 - analog_value) / 4095) * 100

    return moisture_percentage

# Continuously read the moisture sensor and print the percentage
while True:
    moisture = get_moisture()
    print("Moisture percentage:", moisture)
    time.sleep(1)  # wait for 1 second before taking the next reading