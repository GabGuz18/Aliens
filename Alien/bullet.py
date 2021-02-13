import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""Clase para manejar las balas"""

	def __init__(self,ai_game):
		"""Crear un objeto de bala"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		#Crear una bala a (0,0) y corregirlo
		self.rect = pygame.Rect(0,0,self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		#Guardar posicion de la bala
		self.y = float(self.rect.y)

	def update(self):
		"""mueve la bala para arriba"""
		#modifica la posicion de la bala
		self.y -= self.settings.bullet_speed
		#modifica la posicion del rectangulo
		self.rect.y = self.y 

	def draw_bullet(self):
		"""Dibuja la bala"""
		pygame.draw.rect(self.screen, self.color, self.rect)