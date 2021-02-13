class Settings:
	"""Clase para almacenar las configuraciones"""

	def __init__(self):
		"""inicializa las configuraciones"""
		#Configuracion de pantalla
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)

		#Configuracion de nave
		self.ship_limit = 3

		#Configuracion de las balas
		self.bullet_width = 3.0 
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 5

		#Configuracion de alien 
		self.fleet_drop_speed = 10 #10

		#Velocidad del juego
		self.speedup_scale = 1.1

		#Puntuacion del alien mediante los niveles
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Inicializa las configuraciones para cambair el juego"""
		self.ship_speed = 1.5
		self.bullet_speed = 1.5
		self.alien_speed = 2.0

		#Direccion de flota 1 derecha, -1 izquierda
		self.fleet_direction = 1

		#Puntuacion
		self.alien_points = 50

	def increase_speed(self):
		"""Aumenta velocidad de configuraciones y puntuacion"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)