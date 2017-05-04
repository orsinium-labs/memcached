#import socket
import socks

import re
rex_slab = re.compile(r'STAT items\:(\d+)\:number (\d+)')
rex_key = re.compile(r'ITEM (.+?) \[(\d+) b; \d+ s\]')
#ip = '92.53.97.80'


class Connection:
	port = 11211
	
	def __init__(self, ip):
		#self.sock = socket.socket()
		self.sock = socks.socksocket()
		self.sock.set_proxy(socks.SOCKS4, '127.0.0.1', 9050)
		self.ip = ip
		print('Connecting...')
		self.sock.connect((self.ip, self.port))
		print('Connected')
	
	def _query(self, data):
		if data[-1] != '\n':
			data = data + '\n'
		data = data.encode('utf-8')
		self.sock.send(data)
		return self.sock.recv(32768).decode('utf-8')
	
	def get_slabs(self):
		data = self._query('stats items')
		self.slabs = [(i, int(j)) for i,j in rex_slab.findall(data)]
		self.slabs.sort(key=lambda x: x[1], reverse=True)
		return self.slabs
	
	def get_keys(self, slab):
		self.keys = []
		slabs = [(slab, 0)] if (slab is not None) else self.slabs
		for slab, n in slabs:
			data = self._query('stats cachedump {} 100'.format(slab))
			self.keys.extend(rex_key.findall(data))
		self.keys = [(i, int(j)) for i,j in self.keys]
		self.keys = [(i, j) for i,j in self.keys if j > 20]
		self.keys.sort(key=lambda x: x[1], reverse=True)
		return self.keys
	
	def get_data(self, key):
		if type(key) is int or key.isdigit():
			key = self.keys[int(key) - 1]
		return self._query('get {}'.format(key))
	
	def set_data(self, key, data):
		key = self.keys[int(key) - 1]
		q = 'set {} 0 6000 {}\n{}'
		q = q.format(key, len(data), data)
		return self._query(q)
