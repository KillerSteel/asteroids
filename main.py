import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
	pygame.init()
	print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
	print(f"Screen width: {SCREEN_WIDTH}")
	print(f"Screen height: {SCREEN_HEIGHT}")

	# Var initilization
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()

	Player.containers = (updatable, drawable)
	Shot.containers = (shots, updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable)

	asteroid_field = AsteroidField()
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	frametime_clock = pygame.time.Clock()
	dt = 0.0

	while True:
		keys = pygame.key.get_pressed()

		if keys[pygame.K_ESCAPE]:
			sys.exit()

		log_state()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		screen.fill("black")

		updatable.update(dt)

		for asteroid in asteroids:
			if len(shots) > 0:
				for shot in shots:
					if shot.collides_with(asteroid):
						log_event("asteroid_shot")
						asteroid.kill()

			if asteroid.collides_with(player):
				log_event("player_hit")
				print("Game over!")
				sys.exit()

		for obj in drawable:
			obj.draw(screen)

		pygame.display.flip()

		dt = frametime_clock.tick(60) / 1000

if __name__ == "__main__":
    main()
