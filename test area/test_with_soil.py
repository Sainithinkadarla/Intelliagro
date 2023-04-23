from machine import Pin, ADC
import network
import time
from umqqt.simple import MQTTClient
import wifi_cred

timeout =0
# setting to station mode 
wifi = network.WLAN(network.STA_IF)

#restating WIFI
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

wifi.connect(wifi_cred.ssid,wifi_cred.passwd)

if not wifi.isconnected():
    print("Connecting...")
    while(not wifi.isconnected() and timeout<5):
        timeout+=1
        time.sleep(1)

if(wifi.isconnected()):
    print('Connected')
    wifi.ifconfig()
else:
    print('Timeout')


# Set up the ADC pin
adc = ADC(Pin(13))

# Define a function to calculate the moisture percentage
def get_moisture():
    # Read the analog value from the ADC pin
    analog_value = adc.read()

    # Convert the analog value to a moisture percentage (assuming a linear relationship)
    moisture_percentage = ((4095 - analog_value) / 4095) * 100

    return moisture_percentage

SERVER = "mqtt.thingspeak.com"
client =MQTTClient("umqtt_client", SERVER)
CHANNEL_ID = "2118052"
WRITE_API_KEY ="3Y7087YE4WC98ZS9"
topic= "channels/"+CHANNEL_ID+"/publish/"+WRITE_API_KEY
last_update = time.ticks_ms()
UPDATE_TIME_INTERVAL=5000


while True:
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        m=get_moisture()
        payload= "field1={}".format(str(m))
        client.connect()
        client.publish(topic,payload)
        client.disconnect()
        print(payload)
        last_update = time.ticks_ms()
        
