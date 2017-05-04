#!/usr/bin/python3

import readline
import inputer

import checker
import scaner

conn = None

def make_result(data):
	result = []
	for i, (d, n) in enumerate(data[:100], 1):
		result.append('{}. {:30} [{}]'.format(i, d[:30], n))
	return '\n'.join(result)

def main(query):
	global conn
	
	if query[0] == 'set_ip':
		conn = scaner.Connection(query[1])
		return 'Done!'
	
	if query[0] == 'get_slabs':
		slabs = conn.get_slabs()
		return make_result(slabs)
	
	if query[0] == 'get_keys':
		if len(query) > 1:
			slab = query[1]
		else:
			slab = None
		keys = conn.get_keys(slab)
		return make_result(keys)
	
	if query[0] == 'get':
		if len(query) == 1:
			return 'get <key>'
		data = conn.get_data(query[1])
		return data
	
	if query[0] == 'set':
		if len(query) < 3:
			return 'set <key> <file>'
		fname = ' '.join(query[2:])
		try:
			data = open(fname, 'rb').read()
			print("Can't open file! Use filename as data.")
		except:
			data = fname
		data = conn.set_data(query[1], data)
		return data
	
	print('Команда не найдена!')

if __name__ == '__main__':
	try:
		while 1:
			query = input('\x1B[32m> ')
			print('\x1B[0m', end='')
			if not query:
				continue
			readline.add_history(query)
			query = query.split()
			response = main(query)
			print(response)
	except (EOFError, KeyboardInterrupt):
		print('\x1B[0m\nExit...')
