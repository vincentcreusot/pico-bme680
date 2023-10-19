# BME680 values publishing with MQTT
## Features
Sends values from the BME680 using MQTT simple client 
- temperature
- humidity
- pressure
- gas
- altitude
## Usage
Tested with a [RasperryPi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/) 
and a [BME680 Pimoroni](https://shop.pimoroni.com/products/bme680-breakout) Sensor.

To use the MQTT client:
1. flash your Pi
2. copy all files including
- the certificates needed, key, cert and CA in PEM format
- the `main.py`, `mqtt_connect.py`, `bme680.py` files
- the `config.json` file with the right values
- the `lib` folder

## Configuration
The configuration in the `config.json` file is as follows:
```json
{
    "mqtt": {
        "broker": "<broker address>",
        "topic": "<topic name>",
        "cert_key": "<path to cert key>",
        "cert_pem": "<path to certificate>",
        "cert_ca": "<path to CA cert>",
        "wifi_ssid": "<ssid of wifi to use>",
        "wifi_password": "<password of wifi to use>"
    }
}
```
## Dependencies
- Uses micropython implementation of bme680 https://github.com/robert-hh/BME680-Micropython
- Packages mqtt simple in the `lib` folder, that you can copy on your Pi Pico
