host = ('ip.appspot.com', 80)
request = b'GET / HTTP/1.1\nHost: ip.appspot.com\n\n'

import socket
s = socket.socket()
s.connect(host)
s.sendall(request)
response = s.recv(4096)
ip = response.decode('utf-8').split('\n')[-1]
print(ip)

import socks
s = socks.socksocket()
s.set_proxy(socks.SOCKS4, '127.0.0.1', 9050)
s.connect(host)
s.sendall(request)
response = s.recv(4096)
ip = response.decode('utf-8').split('\n')[-1]
print(ip)
