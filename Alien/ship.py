import pygame
from pygame.sprite import Sprite 

class Ship(Sprite):
	"""Clase para manejar la nave"""

	def __init__(self,ai_game):
		"""Inicializa y declarar primera posicion"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		#Cargar la imagen de nave
		self.image = pygame.image.load('Imagenes/ship.bmp')
		self.rect = self.image.get_rect()

		#Empezar con la nave al centro
		self.rect.midbottom = self.screen_rect.midbottom

		#Guardar el valor decimal de la nave
		self.x = float(self.rect.x)

		#Movimiento de la nave
		self.moving_right = False 
		self.moving_left = False

	def update(self):
		"""Actualiza la nave dependiendo de la tecla"""
		#Actualiza los valores de la posicion
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		#Actualiza el rectangulo 
		self.rect.x = self.x

	def blitme(self):
		"""Dibujar nave en posicion"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Centra la nave"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)