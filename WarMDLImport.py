# Copyright (c) 2011 Thomas Glamsch
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import bpy
import string
import io
import pdb
import time

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

dbg = False

bl_info = {
	"name": "Import WarCraft MDL (.mdl)",
	"description": "This addon allows you to import WarCraft MDL model files (.mdl).",
	"author": "Thomas 'CruzR' Glamsch",
	"version": (0, 1, 1),
	"blender": (2, 5, 7),
	#"api": ???,
	"location": "File > Import > WarCraft MDL (.mdl)",
	"warning": "Currently only the vertices and faces are imported, work in progress.",
	"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/Scripts/Import-Export/WarCraft_MDL",
	"tracker_url": "http://projects.blender.org/tracker/index.php?func=detail&aid=29552",
	"category": "Import-Export"}

# TODO: Add more comments

# This is our abstract state machine
class StateMachine:

# @param handlers: Dictionary containing name => function pairs
# @param startState: The first state to call when starting
# @param endStates: State machine will end execution on these
	def __init__(self, parent, handlers={}, startState=None, endStates=[]):
		self.parent = parent
		self.handlers = handlers
		self.startState = startState
		self.endStates = endStates

# @param name: The name of the state to add
# @param handler: A function to handle the state
# @param endState: Bool whether this should be added to endStates
# @param startState: Bool whether this should be set as startState
	def add(self, name, handler, endState=False, startState=False):
		name = name.upper()
		if handler:
			self.handlers[name] = handler(self.parent)
		if endState:
			self.endStates.append(name)
			print(self.endStates)
		if startState:
			self.startState = name

# @param name: Name of the state which shall be set as startState
	def set_start(self, name):
		name = name.upper()
		if name in self.handlers:
			self.startState = name
		else:
			raise Exception("Error: set_start(): Unknown state: {}".format(name))

# @param cargo: Some kind of information to carry through the states
	def run(self, cargo={}):
		handler = self.handlers.get(self.startState)
		if not handler:
			raise Exception("InitError: Set startState before calling StateMachine.run()")
		if not self.endStates:
			raise Exception("InitError: There must be at least one endstate")
		
		while True:
			newState, cargo = handler.run(cargo)
			if newState.upper() in self.endStates:
				break
			else:
				handler = self.handlers[newState.upper()]

# All Handlers should be derived from BaseHandler.
# They all have to override the .run() function
# They should always call newState, cargo = BaseHandler.run(cargo)
# before doing anything else.
class BaseHandler:
	def __init__(self, parent):
		self.parent = parent
	
	def run(self, cargo):
		cargo['prev_handler'] = self.__class__.__name__
		print(cargo['prev_handler'])
		return 'SEARCH', cargo

class GeosetManager:
	def __init__(self):
		self.vertices = [[]]
		self.normals = [[]]
		self.tvertices = [[]]
		self.faces = [[]]
		self.cnt = 0
		self.add_new = False
		
	def new_geoset(self):
		self.vertices.append([])
		self.normals.append([])
		self.tvertices.append([])
		self.faces.append([])
		self.cnt += 1
		self.add_new = False
	
	def append(self, li, cont):
		if cont == 'vertices':
			self.vertices[self.cnt].append(li)
		elif cont == 'normals':
			self.normals[self.cnt].append(li)
		elif cont == 'tvertices':
			self.tvertices[self.cnt].append(li)
		elif cont == 'faces':
			self.faces[self.cnt].append(li)
			self.add_new = True
	
	def extend(self, li, cont):
		if cont == 'vertices':
			self.vertices[self.cnt].extend(li)
		elif cont == 'normals':
			self.normals[self.cnt].extend(li)
		elif cont == 'tvertices':
			self.tvertices[self.cnt].extend(li)
		elif cont == 'faces':
			self.faces[self.cnt].extend(li)
			self.add_new = True

class SEARCH(BaseHandler):
	def run(self, cargo):
		newState, cargo = BaseHandler.run(self, cargo)
		#print('SEARCH')
		while True:
			cargo['last'] = current = self.parent.infile.readline()
			if current == '' :
				newState = 'EOF'
				break
			elif current.strip().startswith('//'):
				continue
			elif current.strip().split()[0] in self.parent.globalkeys:
				newState = current.strip().split()[0].upper()
				break
	
		#print('GOTO {}'.format(newState))
		return newState, cargo

class VERSION(BaseHandler):
	def run(self, cargo):
		cargo = BaseHandler.run(self, cargo)[1]
		#print('VERSION')
		if int(self.parent.infile.readline().strip().strip(',').split()[1]) != 800:
			raise Exception("This MDL Version is not supported!")
		return 'SEARCH', cargo

class GEOSET(BaseHandler):
	def run(self, cargo):
		#print('GEOSET')
		if dbg: pdb.set_trace()
		if cargo['prev_handler'] == 'SEARCH':
			if self.parent.mgr.add_new:
				self.parent.mgr.new_geoset()
			cargo['p'] = 1
		
		newState, cargo = BaseHandler.run(self, cargo)
		
		while cargo['p'] > 0:
			cargo['last'] = current = self.parent.infile.readline()
			current = current.strip()
			if '{' in current: cargo['p'] += 1
			if '}' in current: cargo['p'] -= 1
			if current.split()[0] in self.parent.geosetkeys:
				newState = current.split()[0].upper()
				break
	
		return newState, cargo

class VERTICES(BaseHandler):
	def run(self, cargo):
		cargo = BaseHandler.run(self, cargo)[1]
		for i in range(int(cargo['last'].strip().split()[1])):
			current = self.parent.infile.readline().strip().strip('{},;')
			li = [(float(n)/20) for n in current.split(', ')]
			self.parent.mgr.append(li, 'vertices')
		return 'GEOSET', cargo

class NORMALS(BaseHandler):
	def run(self, cargo):
		cargo = BaseHandler.run(self, cargo)[1]
		for i in range(int(cargo['last'].strip().split()[1])):
			current = self.parent.infile.readline().strip().strip('{},;')
			li = [float(n) for n in current.split(', ')]
			self.parent.mgr.append(li, 'normals')
		return 'GEOSET', cargo

class TVERTICES(BaseHandler):
	def run(self, cargo):
		cargo = BaseHandler.run(self, cargo)[1]
		for i in range(int(cargo['last'].strip().split()[1])):
			current = self.parent.infile.readline().strip().strip('{},:')
			li = [(float(n)/20.0) for n in current.split(', ')]
			self.parent.mgr.append(li, 'tvertices')
		return 'GEOSET', cargo

class FACES(BaseHandler):
	def run(self, cargo):
		cargo = BaseHandler.run(self, cargo)[1]
		grps, cnt = [int(n) for n in cargo['last'].strip().split()[1:3]]
		li = []
		while len(li) < cnt:
			cargo['last'] = current = self.parent.infile.readline()
			if current.strip().startswith('Triangles'):
				for i in range(grps):
					li += [int(n) for n in self.parent.infile.readline().strip().strip('{},;').split(', ')]
		if dbg: print(len(li))
		for i in range(cnt//3):
			self.parent.mgr.append([li[3*i], li[3*i+1], li[3*i+2]], 'faces')
		return 'GEOSET', cargo

class DataImporter:
	infile = None
	globalkeys = ['Version', 'Geoset']
	geosetkeys = ['Vertices', 'Normals', 'TVertices', 'Faces']
	mgr = GeosetManager()
	
	def run(self, filepath, context):
		start_time = time.time()
		print("Opening {}...".format(filepath))
		self.infile = open(filepath, 'r')
		m = StateMachine(parent=self)
		m.add('SEARCH', SEARCH, startState=True)
		m.add('VERSION', VERSION)
		m.add('GEOSET', GEOSET)
		m.add('VERTICES', VERTICES)
		m.add('NORMALS', NORMALS)
		m.add('TVERTICES', TVERTICES)
		m.add('FACES', FACES)
		m.add('EOF', None, endState=True)
		m.run()
		
		if dbg: pdb.set_trace()
		for i in range(self.mgr.cnt + 1):
			mesh = bpy.data.meshes.new("Geoset{}Mesh".format(i))
			obj = bpy.data.objects.new("Geoset{}".format(i), mesh)
			obj.location = (0.0, 0.0, 0.0)
			bpy.context.scene.objects.link(obj)
			mesh.from_pydata(self.mgr.vertices[i], [], self.mgr.faces[i])
			mesh.update()
			if dbg: pdb.set_trace()
			del mesh
			del obj
		
		print("Script finished after {} seconds".format(time.time() - start_time))
		return {'FINISHED'}

class ImportWarMDL(bpy.types.Operator, ImportHelper):
	'''Import from WarCraft MDL model format (.mdl).'''
	bl_idname = "import_mesh.warmdl"
	bl_label = "WarCraft MDL (.mdl)"
	
	filename_ext = ".mdl"
	
	filter_glob = StringProperty(
			default="*.mdl",
			options={'HIDDEN'}
			)
	
	@classmethod
	def poll(cls, context):
		return True
	
	def execute(self, context):
		di = DataImporter()
		return di.run(self.filepath, context)

def menu_func_export(self, context):
	self.layout.operator(ImportWarMDL.bl_idname, text="WarCraft MDL (.mdl)")

def register():
	bpy.utils.register_class(ImportWarMDL)
	bpy.types.INFO_MT_file_import.append(menu_func_export)

def unregister():
	bpy.utils.unregister_class(ImportWarMDL)
	bpy.types.INFO_MT_file_import.remove(menu_func_export)

if __name__ == "__main__":
	register()

	# test call
	bpy.ops.import_mesh.warmdl('INVOKE_DEFAULT')

