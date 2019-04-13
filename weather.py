import threading 
from time import sleep 
from gpiozero import DigitalInputDevice
import math
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt
import json
def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("Connected OK")
    else:
        print("Bad connetion Retruned Code=",rc)
mqtt_c=mqtt.Client('weather')
mqtt_c.on_connect=on_connect
mqtt_c.username_pw_set("homeassistant",password=" ")
mqtt_c.connect("192.168.x.xx")
mqtt_c.loop_start()
dia_m = 0.18
bucket_count = 0
wind_count = 0
rain_cum = 0
interval = 20
ADJUSTMENT = 1.18*(interval/5)
BUCKET_SIZE = 0.2794
circ_m = dia_m * math.pi 
wind_speed_sensor = DigitalInputDevice(17, pull_up=True)
temp_sensor = W1ThermSensor()
rain_sensor = DigitalInputDevice(27, pull_up=True)
def wind (time_sec):
    global wind_count
    rotations = wind_count / 2.0 
    dist_m=circ_m * rotations
    m_per_sec = (dist_m / time_sec) * ADJUSTMENT
    wind_count = 0
    return m_per_sec 

def spin ():
    global wind_count
    wind_count = wind_count + 1
def rain():
    global rain_cum
    rain_cum = rain_cum + BUCKET_SIZE

def temperature():
	return temp_sensor.get_temperature()

windspeed = threading.Thread(name='wind', target=wind(interval))
raindata =  threading.Thread(name ='rain', target=rain)
windspeed.start()
raindata.start()
wind_speed_sensor.when_activated = spin
rain_sensor.when_activated = rain
speed = []
i=0
while True:
    sleep (interval)
    speed.append(wind(interval))  
    i += 1
    if i == 15:
        temper = temperature()
        speed_avg = sum(speed,0.00)/len(speed)
        payload=json.dumps({"rain":rain_cum,
            "temperature":temper,
            "windspeed":speed_avg})
        mqtt_c.publish('outside/weather/',payload)
        # print('Publish data: ' + payload)
        i=0
        speed.clear()
    else:
        pass
