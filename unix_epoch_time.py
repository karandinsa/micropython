import usocket as socket

def prints():
    print('nested proc')
    return 10
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
http_get('http://karandin.kirov.ru.net/scripts/epoch2.pl')
