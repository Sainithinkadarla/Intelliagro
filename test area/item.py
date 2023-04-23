import machine
import time
import math
import network
import urequests
import WaterFlow as wf


timer = machine.Timer(0)
# replace with your own WiFi network details
WIFI_SSID = "moto g(60)_ssk"
WIFI_PASSWORD = "#Bsnloverload"

# replace with your own ThingSpeak API key and channel ID
THINGSPEAK_API_KEY = "ZBXQK4LPTM5QUQ2T"
THINGSPEAK_CHANNEL_ID = "1712553"

# pin connected to the soil moisture sensor
SOIL_MOISTURE_SENSOR_PIN = 32

#pins connected to water flow sensors
wf1_pin =32
wf2_pin =13

#pin connected to waterpump
pump=Pin(14, Pin.OUT)
# read the soil moisture sensor and convert the raw value to percentage
def read_soil_moisture():
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
def send_to_thingspeak(field1):
    url = "https://api.thingspeak.com/update"
    data = {"api_key": THINGSPEAK_API_KEY, "field1": field1}
    response = urequests.post(url, json=data)
    response.close()
    
    
#---------------------------------------------------------------------------------------------------
def read_rain():
    # define the pin number where the rain sensor is connected
    rain_sensor_pin = 13
    # create a pin object for the rain sensor pin
    rain_sensor = Pin(rain_sensor_pin, Pin.IN)
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
        return 0 
    else if moist >= 50 and moist <75:
        return 0.25
    else if moist >= 35 and moist <50:
        return 0.5
    else if moist >=0 and moist<35:
        return 1


# def drip(duration):
#     #is_water_sufficient()
#     #timer.init(period=watering_time_sm*sm_check , mode=machine.Timer.PERIODIC, callback= lambda t: pump.value(not pump.value()))
#     pass

def watering(sm):
        sm_check= soil_moisture_check(sm)
        #water_check= is_water_sufficient()

        if  read_rain():
            #is_water_sufficient() ***
            #timer.init(period=watering_time_sm*sm_check , mode=machine.Timer.PERIODIC, callback= lambda t: pump.value(not pump.value()))***
            #drip(watering_time_sm*sm_check)
        else:
            #is_water_sufficient()***
            #timer.init(period=watering_time_sm*sm_check , mode=machine.Timer.PERIODIC, callback= lambda t: pump.value(not pump.value()))***
            #drip(watering_time_sm*sm_check)

def pipe_health_check(start, end):
    normal_start=10
    normal_end=8
    if start >=(normal_start*0.75) and  start<normal_start:
        print("pipe entry is good")
    if start >=(normal_start*0.5) and  start<(normal_start*0.75):
        print("pipe entry is good")
    if start >=(normal_start*0.25) and  start<(normal_start*0.5):
        print("check ")
        
    if end >=(normal_end*0.75) and  end<normal_end:
        print("pipe end is good")
    if end >=(normal_end*0.5) and  end<(normal_end*0.75):
        print("pipe end is good")
    if end >=(normal_end*0.25) and  end<(normal_end*0.5):
        print("pipe end is good")

    
while True:
    moisture_percentage = read_soil_moisture()
    print("Soil moisture:", moisture_percentage, "%")
    send_to_thingspeak(moisture_percentage)
    
    
    watering(moisture_percentage)
    time.sleep(2*60)
    wf1=wf.measure_flow(wf1_pin)
    wf2=wf.measure_flow(wf2_pin)
    pipe_health_check(wf1[1], wf2[1])
    
    
    
    