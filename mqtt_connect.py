import machine
from umqtt.simple import MQTTClient
import ubinascii
import ssl
import time
import network


# function that reads PEM file and return byte array of data
def read_pem(file):
    print(f"Reading : {file}")
    with open(file, "r") as input:
        text = input.read().strip()
        split_text = text.split("\n")
        base64_text = "".join(split_text[1:-1])
        return ubinascii.a2b_base64(base64_text)
    
    
def get_mqtt_client(broker, key, cert, ca):
    # read the data in the private key, public certificate, and
    # root CA files
    key = read_pem(key)
    cert = read_pem(cert)
    ca = read_pem(ca)

    mqtt_client_id = ubinascii.hexlify(machine.unique_id())
    
    # create MQTT client that use TLS/SSL for a secure connection
    mqtt_client = MQTTClient(
        mqtt_client_id,
        broker,
        keepalive=60,
        ssl=True,
        ssl_params={
            "key": key,
            "cert": cert,
            "server_hostname": broker,
            "cert_reqs": ssl.CERT_REQUIRED,
            "cadata": ca,
        },
    )
    return mqtt_client

def connect_wifi(ssid, password):
    print(f"Connecting to Wi-Fi SSID: {ssid}")

    # initialize the Wi-Fi interface
    wlan = network.WLAN(network.STA_IF)

    # activate and connect to the Wi-Fi network:
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(0.5)

    print(f"Connected to Wi-Fi SSID: {ssid}")
