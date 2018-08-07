from machine import Pin, I2C
i2c = I2C(scl=Pin(2), sda=Pin(4), freq=100000)