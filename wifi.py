import network
import time


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

    return wlan

