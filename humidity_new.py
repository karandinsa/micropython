import dht
import machine
import usocket as socket
import time

def reset_chip():
    time.sleep(20)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, 10000)
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
        return int(epoch_time[1])
    except OSError:
        print(OSError)
        reset_chip()
        
def do_measure():
    time_value=http_get('http://karandin.kirov.ru.net/scripts/epoch2.pl')
    d = dht.DHT11(machine.Pin(4))
    d.measure()
    address = ("0.0.0.0", 2003)
    data_temperature = b'micropython_sk.temperature.home '+str(d.temperature())+' '+str(time_value)
    data_humidity = b'micropython_sk.humidity.home '+str(d.humidity())+' '+str(time_value)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data_temperature, address)
    sock.sendto(data_humidity, address)
    print('sended')

noerrors = True
while noerrors:
    try:
        do_measure()
        time.sleep(60)
        noerrors = True
    except:
        noerrors = False
        reset_chip()