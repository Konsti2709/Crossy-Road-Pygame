import pygame
import random
from autos import Auto

class Strasse:
	def __init__(self, zeile, QUADRAT_BREITE, QUADRAT_HOEHE):
		self.zeile = zeile
		self.richtung = random.choice([-1, 1])
		self.timer = random.randint(50, 200)
		self.intervall = self.timer
		self.autos = []

		self.QUADRAT_BREITE = QUADRAT_BREITE
		self.QUADRAT_HOEHE = QUADRAT_HOEHE


	def befüllen(self, SPIELFELD_BREITE):
		# Random Anzahl Autos
		anzahl_autos = random.randint(4, 6)

		# Autos setzen
		for auto in range(anzahl_autos):
			max_versuche = 20

			auto_y = self.zeile * self.QUADRAT_HOEHE + self.QUADRAT_HOEHE / 10

			for _ in range(max_versuche):
				auto_x = random.randint(0, SPIELFELD_BREITE) * self.QUADRAT_BREITE + self.QUADRAT_BREITE / 10
				neues_auto = Auto(auto_x, auto_y, self.richtung)

				neues_rechteck = pygame.Rect(neues_auto.x, neues_auto.y, neues_auto.breite, neues_auto.hoehe)

				kollidiert = False

				for anderes_auto in self.autos:
					anderes_rechteck = pygame.Rect(anderes_auto.x, anderes_auto.y, anderes_auto.breite, anderes_auto.hoehe)

					if neues_rechteck.colliderect(anderes_rechteck):
						kollidiert = True
						break
					
				if not kollidiert:
					self.autos.append(neues_auto)
					break
	

	def timer_runterzaehlen(self):
		# Jeden Frame Timer runterzählen
		self.timer -= 1

		if self.timer <= 0:
			# Neues Intervall festlegen
			self.timer = self.intervall
			self.intervall = random.randint(50, 200)
			
			return True

		return False


	def auto_spawnen(self, SPIELFELD_BREITE):
		if self.timer_runterzaehlen():
			auto = Auto(0, 0, self.richtung)

			# Auto an der Seite spawnen
			if self.richtung == 1:
				x = -auto.breite
			
			else:
				x = SPIELFELD_BREITE * self.QUADRAT_BREITE + auto.breite
			
			# Auto Y Position festlegen
			y = self.zeile * self.QUADRAT_HOEHE + self.QUADRAT_HOEHE / 10

			auto.x = x
			auto.y = y

			self.autos.append(auto)


	def auto_bewegen(self):
		for auto in self.autos:
			auto.bewegen()