class Spieler:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.breite = 40
		self.hoehe = 40

	def bewegen(self, x, y):
		self.x += x
		self.y += y
	
