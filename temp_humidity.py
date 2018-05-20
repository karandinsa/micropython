import dht
import machine
import usocket as socket
from machine import Timer

def http_get(url):
    _, _, host, path = url.split('/', 3)
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

def do_measure():
    time_value=http_get('http://karandin.kirov.ru.net/scripts/epoch2.pl')
    d = dht.DHT11(machine.Pin(4))
    d.measure()
    address = ("185.125.217.131", 2003)
    data_temperature = b'micropython_sk.temperature.home '+str(d.temperature())+' '+str(time_value)
    data_humidity = b'micropython_sk.humidity.home '+str(d.humidity())+' '+str(time_value)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data_temperature, address)
    sock.sendto(data_humidity, address)
    print('Температура',d.temperature())
    print('Влажность',d.humidity())
    print(time_value)

tim = Timer(-1)
tim.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:do_measure())
