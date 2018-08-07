import gc
import network
import webrepl
webrepl.start()
gc.enable()
sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()
sta_if.connect("TP-LINK_D34C", "*******")
sta_if.isconnected()  
