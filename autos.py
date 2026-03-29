import random

class Auto:

	def __init__(self, x, y, richtung):
		self.x = x
		self.y = y
		self.richtung = richtung
		self.breite = random.randint(40, 100)
		self.hoehe = 40


	def bewegen(self):
		self.x += self.richtung