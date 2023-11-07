import bme680
from machine import I2C, Pin, Timer
from wifi import connect_wifi
import time
import ujson
import mqtt_connect
import sys

try:
    f = open('config.json', 'r')
except OSError as e:
    print ('error reading file')
    sys.exit(5)
    
config = ujson.loads(f.read())
led = Pin("LED", Pin.OUT)
led.on()
time.sleep(2)
led.off()

wifi_ssid = config["mqtt"]["wifi_ssid"]
wifi_password = config["mqtt"]["wifi_password"]
connect_wifi(wifi_ssid, wifi_password)
led.on()
time.sleep(2)
led.off()

i2c = I2C(id=0, scl=Pin(17), sda=Pin(16), freq=200000)
print('Scan i2c bus...')
devices = i2c.scan()
led.on()
time.sleep(2)
led.off()

bme = bme680.BME680_I2C(i2c=i2c, address=118)
print('Connected to sensor')
while True:
    led.on()
    mc = mqtt_connect.MQTT(config)
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
    mc.publish(temperatureStr)
    print("published")
    mc.disconnect()
    led.off()
    # Sleeping deep for 30 seconds
    time.sleep_ms(30000)
    


    
