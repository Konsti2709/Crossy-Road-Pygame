class Spieler:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.breite = 40
		self.hoehe = 40

	def bewegen(self, x, y, max_breite, max_hoehe):
		neue_x = self.x + x
		neue_y = self.y + y

		if 0 <= neue_x <= max_breite - self.breite:
			self.x = neue_x

		if 0 <= neue_y <= max_hoehe - self.hoehe:
			self.y = neue_y
	
