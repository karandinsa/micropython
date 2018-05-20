# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import network
gc.enable()
sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()
sta_if.connect("TP-LINK_D34C", "*****")
sta_if.isconnected()  
