import sys
from time import sleep

import pygame 

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien 
from game_stats import GameStats 
from button import Button
from scoreboard import Scoreboard 

class AlienInvasion:
	"""Clase para organizar comportamientos"""

	def __init__(self):
		"""Inicializa el juego y crea recursos"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		#Crear instancia de GameStats
		self.stats = GameStats(self)
		#Crea el marcador
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		#Crear el boton
		self.play_button = Button(self,"Play")

	def run_game(self):
		"""Empieza el while para el juego"""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()

	def _check_events(self):
		"""Responde a teclas y mouse"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self,mouse_pos):
		"""Empieza el juego cuando das click"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#Resetea las configuraciones del juego
			self.settings.initialize_dynamic_settings()

			#Resetea las estadisticas del juego
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#Deshacerse de las balas y aliens
			self.aliens.empty()
			self.bullets.empty()

			#Crear una nueva flota y centrar la nave
			self._create_fleet()
			self.ship.center_ship()

			#Esconder el mouse
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Crear una bala y añadirla al grupo"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Actualiza la posicion de las balas"""
		#Actualiza las posiciones
		self.bullets.update()

		#Deshacernos de las balas
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_colisions()

	def _check_bullet_alien_colisions(self):
		"""Responde a los choques"""
		#Revisar las balas que chocaron a los aliens
		#Si pasó, deshacerse de los 2
		collisions = pygame.sprite.groupcollide(
				self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			#Destruye balas viejas y hace mas alies
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#Incrementa nivel
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		"""Checar si la flota esta en el borde, y luego actualizar los camnios"""
		self._check_fleet_edges()
		self.aliens.update()

		#Checar por colisiones con la nave
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		#Checa los aliens en el fondo
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""Responde a los choques"""
		if self.stats.ships_left > 0:
			#Decrementa la vida de las naves
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			#Deshacerse de los aliens y las balas
			self.aliens.empty()
			self.bullets.empty()

			#Crear una nueva flota y nave al centro
			self._create_fleet()
			self.ship.center_ship()

			#Pausa
			sleep(0.5)
		else:
			self.stats.game_active = False 
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""Revisa si los aliens tocan el fondo"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Como si chocara con la nave
				self._ship_hit()
				break

	def _create_fleet(self):
		"""Crea la flota de aliens"""
		#Calcular cuantos aliens caben en una fila
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		#Determina el numero de filas de aliens
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
								(3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		#Crear la flota
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):
		#Crear un alien y proyectarlo
			alien = Alien(self)
			alien_width, alien_height = alien.rect.size
			alien.x = alien_width + 2 * alien_width * alien_number
			alien.rect.x = alien.x
			alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
			self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Responde si llegaron al borde"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Cambiar la direccion de la flota"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self):
		"""Actualiza la pantalla"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		#Dibuja el marcador
		self.sb.show_score()

		#Dibuja el boton si esta inactivo
		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()


if __name__ == '__main__':
	#Correr el juego y hacer una instancia
	ai = AlienInvasion()
	ai.run_game()