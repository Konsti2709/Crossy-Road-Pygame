class Auto:
	breite = 40
	hoehe = 40

	def __init__(self, x, y, richtung):
		self.x = x
		self.y = y
		self.richtung = richtung


	def bewegen(self):
		self.x += self.richtung