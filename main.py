import dht
import machine
import usocket as socket
import time

def reset_chip():
    time.sleep(20)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, 25000)
    machine.deepsleep()

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
            reset_chip()
    except OSError:
        print(OSError)
        reset_chip()
        
def do_measure():
    time_value=http_get('http://karandin.kirov.ru.net/scripts/epoch2.pl')
    d = dht.DHT11(machine.Pin(4))
    d.measure()
    adc = machine.ADC(0)
    address = ("0.0.0.0", 2003)
    data_temperature = b'micropython_sk.temperature.home '+str(d.temperature())+' '+str(time_value)
    data_humidity = b'micropython_sk.humidity.home '+str(d.humidity())+' '+str(time_value)
    data_light = b'micropython_sk.light.home '+str(1024-adc.read())+' '+str(time_value)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data_temperature, address)
    sock.sendto(data_humidity, address)
    sock.sendto(data_light, address)

do_measure()
reset_chip()

