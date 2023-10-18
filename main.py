import bme680
from machine import I2C, Pin, Timer

import time
import ntptime
import ujson
import mqtt_connect
import sys

try:
    f = open('config.json', 'r')
except OSError as e:
    print ('error reading file')
    sys.exit(5)
    
config = ujson.loads(f.read())
broker = config['mqtt']['broker']
key = config["mqtt"]["cert_key"]
cert = config["mqtt"]["cert_pem"]
ca = config["mqtt"]["cert_ca"]
wifi_ssid = config["mqtt"]["wifi_ssid"]
wifi_password = config["mqtt"]["wifi_password"]

mqtt_temperature_topic = config["mqtt"]["topic"]

mc = mqtt_connect.get_mqtt_client(broker, key, cert, ca)

def pingmc(t):
    mc.ping()
    
mqtt_connect.connect_wifi(wifi_ssid, wifi_password)

# update the current time on the board using NTP
ntptime.settime()

mc.connect()
# create timer for periodic MQTT ping messages for keep-alive
mqtt_ping_timer = Timer(
    mode=Timer.PERIODIC, period=mc.keepalive * 1000, callback=pingmc
)

i2c = I2C(id=0, scl=Pin(17), sda=Pin(16))
print('Scan i2c bus...')
devices = i2c.scan()

bme = bme680.BME680_I2C(i2c=i2c, address=118)
print('Connected to sensor')
while True:
    gas_value = str(bme.gas)
    temp_value = bme.temperature
    humid_value = bme.humidity
    press_value = bme.pressure
    alt_value = bme.altitude
    ltime = str(time.mktime(time.localtime()))
    temperatureStr = '''
{{
    "timestamp": "{T}",
    "temperature": "{t:.2f}",
    "humidity": "{h:.2f}",
    "pressure": "{p:.2f}",
    "gas": "{g}",
    "altitude": "{a:.2f}"
}}'''.format(t = temp_value, h = humid_value, p = press_value, g = gas_value, a = alt_value, T = ltime)
    print('sending {temperatureStr}', temperatureStr)
    mc.publish(mqtt_temperature_topic, temperatureStr)
    print("published")
    time.sleep(60)
    


    
