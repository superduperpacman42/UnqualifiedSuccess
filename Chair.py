import pygame
from Constants import *
from Person import Person

class Chair:
	def __init__(self, pos, person=None, neighbor=None):
		self.pos = pos
		self.person = person
		self.neighbors = []
		if self.pos[0] == 1:
			self.direction = "RS"
		elif self.pos[0] == 12:
			self.direction = "LS"
		else:
			self.direction = "BS"
		if neighbor:
			self.addNeighbor(neighbor)
			neighbor.addNeighbor(self)
		if self.person and self.person != "table":
			self.person.setPos(self.pos[0]-1, self.pos[1]-1)
			self.person.setDirection(self.direction)

	def addNeighbor(self, neighbor):
		self.neighbors.append(neighbor)

	def toChair(self, neighbor):
		return (neighbor.pos[0]-self.pos[0],neighbor.pos[1]-self.pos[1])