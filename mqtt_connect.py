import machine
from umqtt.simple import MQTTClient
import ubinascii
import ssl
import time
import network
import ntptime

class MQTT:
    def __init__(self, config):
        broker = config['mqtt']['broker']
        key = config["mqtt"]["cert_key"]
        cert = config["mqtt"]["cert_pem"]
        ca = config["mqtt"]["cert_ca"]
        self.mqtt_temperature_topic = config["mqtt"]["topic"]
        self.client = self._get_mqtt_client(broker, key, cert, ca)
        # update the current time on the board using NTP
        ntptime.settime()

        self.client.connect()

    # function that reads PEM file and return byte array of data
    def _read_pem(self, file):
        print(f"Reading : {file}")
        with open(file, "r") as input:
            text = input.read().strip()
            split_text = text.split("\n")
            base64_text = "".join(split_text[1:-1])
            return ubinascii.a2b_base64(base64_text)


    def _get_mqtt_client(self, broker, key, cert, ca):
        # read the data in the private key, public certificate, and
        # root CA files
        key = self._read_pem(key)
        cert = self._read_pem(cert)
        ca = self._read_pem(ca)

        mqtt_client_id = ubinascii.hexlify(machine.unique_id())

        # create MQTT client that use TLS/SSL for a secure connection
        try:
            mqtt_client = MQTTClient(
                client_id=mqtt_client_id,
                server=broker,
                port=8883,
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
        except MQTTException as e:
            print(e)
        return mqtt_client


    def publish(self, message):
        self.client.publish(self.mqtt_temperature_topic, message)

    def disconnect(self):
        self.client.disconnect()
