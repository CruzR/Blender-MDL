#!/usr/bin/python3

import io
from mdl import Geoset
from statemachine import StateMachine, BaseHandler

infile = None
globalkeys = ['Version', 'Geoset']
geosetkeys = ['Vertices', 'Normals', 'TVertices']
geosets = []

class SEARCH(BaseHandler):
	def run(self, cargo):
		newState, cargo = BaseHandler.run(self, cargo)
		print('SEARCH')
		while True:
			cargo['last'] = current = infile.readline()
			if current == '' :
				newState = 'EOF'
				break
			elif current.strip().split()[0] in globalkeys:
				newState = current.strip().split()[0].upper()
				break
	
		print('GOTO {}'.format(newState))
		return [newState, cargo]

class VERSION(BaseHandler):
	def run(self, cargo):
		cargo = BaseHandler.run(self, cargo)[1]
		print('VERSION')
		if int(infile.readline().strip().strip(',').split()[1]) != 800:
			raise Exception("This MDL Version is not supported!")
		return ['SEARCH', cargo]

class GEOSET(BaseHandler):
	def run(self, cargo):
		print('GEOSET')
		if cargo['prev_handler'] == 'SEARCH':
			try:
				cargo['geoindex'] += 1
			except:
				cargo['geoindex'] = 0
			geosets.append(Geoset())
			cargo['p'] = 1
		
		newState, cargo = BaseHandler.run(self, cargo)
		
		while cargo['p'] > 0:
			cargo['last'] = current = infile.readline()
			current = current.strip()
			if '{' in current: cargo['p'] += 1
			if '}' in current: cargo['p'] -= 1
			if current.split()[0] in geosetkeys:
				newState = current.split()[0].upper()
				break
	
		return [newState, cargo]

class VERTICES(BaseHandler):
	def run(self, cargo):
		cargo = BaseHandler.run(self, cargo)[1]
		for i in range(int(cargo['last'].strip().split()[1])):
			current = infile.readline().strip().strip('{},;')
			li = [float(n) for n in current.split(', ')]
			geosets[cargo['geoindex']].vertices.append(li)
		return ['GEOSET', cargo]

class NORMALS(BaseHandler):
	def run(self, cargo):
		cargo = BaseHandler.run(self, cargo)[1]
		for i in range(int(cargo['last'].strip().split()[1])):
			current = infile.readline().strip().strip('{},;')
			li = [float(n) for n in current.split(', ')]
			geosets[cargo['geoindex']].normals.append(li)
		return ['GEOSET', cargo]

class TVERTICES(BaseHandler):
	def run(self, cargo):
		cargo = BaseHandler.run(self, cargo)[1]
		for i in range(int(cargo['last'].strip().split()[1])):
			current = infile.readline().strip().strip('{},:')
			li = [float(n) for n in current.split(', ')]
			geosets[cargo['geoindex']].tvertices.append(li)
		return ['GEOSET', cargo]

def run():
	global infile
	print('Please input the path to the file')
	filepath = input('--> ')
	infile = open(filepath, 'r')
	m = StateMachine()
	m.add('SEARCH', SEARCH, startState=True)
	m.add('VERSION', VERSION)
	m.add('GEOSET', GEOSET)
	m.add('VERTICES', VERTICES)
	m.add('NORMALS', NORMALS)
	m.add('TVERTICES', TVERTICES)
	m.add('EOF', None, endState=True)
	m.run()
	for geoset in geosets:
		print('Vertices: {}'.format(geoset.vertices))
		print('Normals: {}'.format(geoset.normals))
		print('TVertices: {}'.format(geoset.tvertices))
