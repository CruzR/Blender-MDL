#!/usr/bin/python3

import string

# This is our abstract state machine
class StateMachine:

# @param handlers: Dictionary containing name => function pairs
# @param startState: The first state to call when starting
# @param endStates: State machine will end execution on these
	def __init__(self, handlers={}, startState=None, endStates=[]):
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
			self.handlers[name] = handler()
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

# @param cargo: Some kind of information to carry through the states
	def run(self, cargo={}):
		try:
			handler = self.handlers[self.startState]
		except:
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
	def run(self, cargo):
		cargo['prev_handler'] = self.__class__.__name__
		print("Prev: {}".format(cargo['prev_handler']))
		return ['SEARCH', cargo]
