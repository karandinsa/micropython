import usocket as socket
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
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("0.0.0.0", 2003)
delay_time=5

def http_get(url):
	_, _, host, path = url.split('/', 3)
	try:
		addr = socket.getaddrinfo(host, 80)[0][-1]
		s = socket.socket()
		s.connect(addr)
		s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
		while True:
			data = s.recv(200)
			if data:
				m = str(data, 'utf8')
				epoch_time = m.split('text/html',1)
			else:
				break
		s.close()
		try:
			if int(epoch_time[1])>1502649400:
				return int(epoch_time[1])
		except:
			return 0
	except:
        	return 0

while True:
	time.sleep(delay_time)	
	lcd.clear()
	lcd.move_to(2,0)
	lcd.putstr('Temperature')
	lcd.move_to(4,1)
	lctemp=bme.values[0]
	lcd.putstr(lctemp+' C')
	time_value=http_get('https://karandin.kirov.ru.net/scripts/epoch2.pl')
	if time_value>0:
		data_temperature = b'micropython_sk.temperature.home '+lctemp+' '+str(time_value)
		sock.sendto(data_temperature, address)

	time.sleep(delay_time)
	lcd.clear()
	lcd.move_to(4,0)
	lcd.putstr('Humidity')
	lcd.move_to(5,1)
	lcHumidity=bme.values[2]
	lcd.putstr(lcHumidity+' %')
	time_value=http_get('https://karandin.kirov.ru.net/scripts/epoch2.pl')
	if time_value>0:
		data_Humidity = b'micropython_sk.humidity.home '+lcHumidity+' '+str(time_value)
		sock.sendto(data_Humidity, address)


	time.sleep(delay_time)
	lcd.clear()
	lcd.move_to(4,0)
	lcd.putstr('Pressure')
	lcd.move_to(3,1)
	lcPressure =bme.values[1]
	lcd.putstr(lcPressure+' hPa')
	
	time_value=http_get('https://karandin.kirov.ru.net/scripts/epoch2.pl')
	if time_value>0:
		data_Pressure = b'micropython_sk.pressure.home '+lcPressure+' '+str(time_value)
		sock.sendto(data_Pressure, address)



	time.sleep(delay_time)
	ccs.data_ready()
	lcd.clear()
	lcd.move_to(1,0)
	lcd.putstr('Carbon dioxide')
	lcd.move_to(4,1)
	lceCO2= str(ccs.eCO2)
	lcd.putstr(lceCO2+' ppm')
	time_value=http_get('https://karandin.kirov.ru.net/scripts/epoch2.pl')
	if time_value>0:
		data_eCO2 = b'micropython_sk.eCO2.home '+lceCO2+' '+str(time_value)
		sock.sendto(data_eCO2, address)




	time.sleep(delay_time)
	ccs.data_ready()
	lcd.clear()
	lcd.move_to(0,0)
	lcd.putstr('Volatile organic')
	lcd.move_to(4,1)
	lctVOC=str(ccs.tVOC)
	lcd.putstr(lctVOC+' ppb')
	time_value=http_get('https://karandin.kirov.ru.net/scripts/epoch2.pl')
	if time_value>0:
		data_tVOC = b'micropython_sk.tVOC.home '+lctVOC+' '+str(time_value)
		sock.sendto(data_tVOC, address)


