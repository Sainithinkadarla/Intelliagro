import machine
import time
import math
import network
import urequests


# replace with your own WiFi network details
WIFI_SSID = "moto g(60)_ssk"
WIFI_PASSWORD = "#Bsnloverload"

# replace with your own ThingSpeak API key and channel ID
THINGSPEAK_API_KEY = "ZBXQK4LPTM5QUQ2T"
THINGSPEAK_CHANNEL_ID = "1712553"

# pin connected to the soil moisture sensor
SOIL_MOISTURE_SENSOR_PIN = 32

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
    return True

Tdt = 30 -5 #assume that 30cm  of tank is present (Total distance of tank) 

def is_water_sufficient():
    #present= #distance calculated by ultrasonic sound sensor
    if (present-Tdt) <= (Tdt*0.50): #12.5
        #fill the tank to 20 cm
    else
        return True
    
watering_time_sm = 10

def soil_moisture_check(moist):
    if moist >= 75 or moist <100: #75 - 100
        return 0 
    else if moist >= 50 or moist <75:
        return 0.25
    else if moist >= 35 or moist <50:
        return 0.5
    else if moist >=0 or moist<35:
        return 1

def level2_watering:
    if bool(math.floor(sm_time)):
        #drip with in-built | takes argument sm_check
    else:
        # drip with caluculated duration

def drip(duration):
    if water_check:
        #turn on pump
    pass

def watering(sm):
        sm_check= soil_moisture_check(sm)
        rain_check= read_rain()
        water_check= is_water_sufficient()

        if rain_check:
            level2_watering(sm_check)
        else:
            level2_watering(sm_check)


while True:
    moisture_percentage = read_soil_moisture()
    print("Soil moisture:", moisture_percentage, "%")
    send_to_thingspeak(moisture_percentage)
    time.sleep(1)
    
    watering(moisture_percentage)    

    
    
    


