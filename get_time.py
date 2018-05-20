import usocket as socket
lcRequest=b'GET / HTTP/1.1\r\nHost: karandin.kirov.ru.net/scripts/epoch2.pl\r\n\r\n'
lcRequest2=b'GET /scripts/epoch2.pl HTTP/1.1'
addr = socket.getaddrinfo('karandin.kirov.ru.net', 80)[0][-1]
s = socket.socket()
s.connect(addr)
s.send(lcRequest2)
data = s.recv(4096)
s.close()
