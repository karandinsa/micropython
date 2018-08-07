
>>> lc=ubinascii.hexlify(i2c.readfrom_mem(104,0x00,7))
>>> l=lc.decode()
>>> l[0:2]-seconds
