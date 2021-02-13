class GameStats:
	"""Sigue las estadisticas del juego"""

	def __init__(self,ai_game):
		"""Inicializa estadisticas"""
		self.settings = ai_game.settings
		self.reset_stats()

		#Inicia el juego en estado activo
		self.game_active = False

		#Marcador alto
		self.high_score = 0

	def reset_stats(self):
		"""Inicializa estadisticas que cambien en el juego"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1