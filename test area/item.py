import machine, dht
import time
import math
import network
import urequests
import WF as wf
from machine import Pin

d = dht.DHT11(Pin(16, Pin.IN))
# def drip(duration):
#     #is_water_sufficient()
#     #timer.init(period=watering_time_sm*sm_check , mode=machine.Timer.PERIODIC, callback= lambda t: pump.value(not pump.value()))
#     pass

timer = machine.Timer(0)
# replace with your own WiFi network details
WIFI_SSID = "moto g(60)_ssk"
WIFI_PASSWORD = "#Bsnloverload"

# replace with your own ThingSpeak API key and channel ID
THINGSPEAK_API_KEY = "ZBXQK4LPTM5QUQ2T"
THINGSPEAK_CHANNEL_ID = "1712553"

# pin connected to the soil moisture sensor
sm1 =13 
sm2 =12

#pins connected to water flow sensors
wf1_pin =14
wf2_pin =27

buzzer =machine.Pin(32, machine.Pin.OUT)

#pin connected to waterpump
pump=machine.Pin(33, machine.Pin.OUT)
pump.value(0)
pump.value(1)
# read the soil moisture sensor and convert the raw value to percentage
def read_soil_moisture(SOIL_MOISTURE_SENSOR_PIN):
    adc = machine.ADC(machine.Pin(SOIL_MOISTURE_SENSOR_PIN))
    raw_value = adc.read()
    voltage = raw_value / 4095 * 3.3
    moisture_percentage = math.floor((1 - (voltage - 1.1) / 1.9) * 100)
    return moisture_percentage

# connect to WiFi
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print("Connected to WiFi:", sta_if.ifconfig())

# send data to ThingSpeak
def send_to_thingspeak(field1,field2,field3,field4):
    url = "https://api.thingspeak.com/update"
    data = {"api_key": THINGSPEAK_API_KEY, "field1": field1, "field2": field2, "field3": field3, "field4": field4}
    response = urequests.post(url, json=data)
    response.close()
    
    
#---------------------------------------------------------------------------------------------------
def read_rain():
    # define the pin number where the rain sensor is connected
    rain_sensor_pin = 15
    # create a pin object for the rain sensor pin
    rain_sensor = machine.Pin(rain_sensor_pin, Pin.IN)
    # read the state of the rain sensor pin
    is_raining = rain_sensor.value()
    if is_raining:
        return False
    else:
        return True

#         
# Tdt = 30 -5 #assume that 30cm  of tank is present (Total distance of tank) 
# 
# def is_water_sufficient():
#     #present= #distance calculated by ultrasonic sound sensor
#     if (present-Tdt) <= (Tdt*0.50): #12.5
#         #fill the tank to 20 cm
#     else:
#         return True
    
watering_time_sm = 10*60*60*100

def soil_moisture_check(moist):
    if moist >= 75 and moist <100: #75 - 100
        return float(0) 
    elif moist >= 50 and moist <75:
        return float(0.25)
    elif moist >= 35 and moist <50:
        return float(0.5)
    elif moist >=0 and moist<35:
        return float(1)




def watering(sm_data1, sm_data2):
        sm1_check= soil_moisture_check(sm_data1)
        sm2_check= soil_moisture_check(sm_data2)
        #water_check= is_water_sufficient()
        if (sm1_check <= sm2_check+5) or (sm1_check <=sm2_check-5):
            if  read_rain():
            #is_water_sufficient() #***
                timer.init(period=2000 , mode=machine.Timer.PERIODIC, callback= lambda t: pump.value(1))#***
                print("ncnskjdcnbdsb")
            #             drip(watering_time_sm*sm_check)
            else:
            #is_water_sufficient()#***
                timer.init(period=2000 , mode=machine.Timer.PERIODIC, callback= lambda t: pump.value(1))#***
            #             drip(watering_time_sm*sm_check)
        
    

        



def pipe_health_check(start, end):
    normal_start=11.20
    normal_end=10.20
    if start >=11.20 and  start<11.80:
        print("pipe entry is good")
    else:
        print("Drip is going to turn off","\n","check entry of pipe")
        
    if end >=10.20 and  end<11.05:
        print("exit pipe is good")
    else:
        print("Drip is going to turn off","\n","please check exit pipe")

#connect_wifi()
while True:
    sm1_percentage = read_soil_moisture(sm1)
    sm2_percentage = read_soil_moisture(sm2)
    print("Soil moisture of field1:", sm1_percentage, "%")
    print("Soil moisture of field2:", sm2_percentage, "%")
    
    wf1=wf.measure_flow(13)
    wf2=wf.measure_flow(14)
    
    
    print("Temperature: ",d.temperature())
    print("Humidity: ",d.humidity())


    
    watering(sm1_percentage,sm2_percentage)
    time.sleep(2)#2mins sleep
    
    #----------------------pipe health checking code------------------------
    
    pipe_health_check(wf1,wf2)
    #send_to_thingspeak(sm1_percentage, sm2_percentage, wf1, wf2)
    
    
    
    



