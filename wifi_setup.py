import network
ap_if=network.WLAN(network.AP_IF)
ap_if.config(essid="MicroPython-SK", authmode=network.AUTH_WPA_WPA2_PSK, password="MicroPythonSK")