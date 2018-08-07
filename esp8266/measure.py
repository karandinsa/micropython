import time
import ccs811
import bme280
import esp8266_i2c_lcd
from machine import I2C,Pin
time.sleep(3)
i2c = I2C(scl=Pin(2), sda=Pin(4), freq=100000)
bme=bme280.BME280(i2c=i2c)
ccs=ccs811.CCS811(i2c)
lcd=esp8266_i2c_lcd.I2cLcd(i2c,39,2,16)
delay_time=5

while True:
	time.sleep(delay_time)	
	lcd.clear()
	lcd.move_to(2,0)
	lcd.putstr('Temperature')
	lcd.move_to(4,1)
	lcd.putstr(bme.values[0])

	time.sleep(delay_time)
	lcd.clear()
	lcd.move_to(4,0)
	lcd.putstr('Humidity')
	lcd.move_to(5,1)
	lcd.putstr(bme.values[2])

	time.sleep(delay_time)
	lcd.clear()
	lcd.move_to(4,0)
	lcd.putstr('Pressure')
	lcd.move_to(3,1)
	lcd.putstr(bme.values[1])

	time.sleep(delay_time)
	ccs.data_ready()
	lcd.clear()
	lcd.move_to(1,0)
	lcd.putstr('Carbon dioxide')
	lcd.move_to(4,1)
	lcd.putstr(str(ccs.eCO2)+' ppm')

	time.sleep(delay_time)
	ccs.data_ready()
	lcd.clear()
	lcd.move_to(0,0)
	lcd.putstr('Volatile organic')
	lcd.move_to(4,1)
	lcd.putstr(str(ccs.tVOC)+' ppb')