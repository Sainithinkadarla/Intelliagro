from machine import Pin, ADC
import network
import time
from umqqt.simple import MQTTClient
import SMsensor as smsen
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
    
SERVER = "mqtt.thingspeak.com"
client =MQTTClient("umqtt_client", SERVER)
CHANNEL_ID = "2118052"
WRITE_API_KEY ="3Y7087YE4WC98ZS9"
topic= "channels/"+CHANNEL_ID+"/publish/"+WRITE_API_KEY
last_update = time.ticks_ms()
UPDATE_TIME_INTERVAL=5000


while True:
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        m=smsen.get_moisture()
        payload= "field1={}".format(str(m))
        client.connect()
        client.publish(topic,payload)
        client.disconnect()
        print(payload)
        last_update = time.ticks_ms()
        