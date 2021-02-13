import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""Clase para representar los aliens"""

	def __init__(self,ai_game):
		"""Inicializa el alien y su posicion"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		#Carga la imagen
		self.image = pygame.image.load('Imagenes/alien.bmp')
		self.rect = self.image.get_rect()

		#Empieza el alien en la esquina
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Guarda la posicion exacta
		self.x = float(self.rect.x)

	def check_edges(self):
		"""Regresa si el alien esta en el borde"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True 

	def update(self):
		"""Mover el alien a la derecha o izquierda"""
		self.x += (self.settings.alien_speed * 
						self.settings.fleet_direction)
		self.rect.x = self.x
