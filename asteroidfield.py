import random
from collections.abc import Callable

import pygame
from asteroid import Asteroid
from constants import *

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
	containers: pygame.sprite.Group

	edges: list[Edge] = [
		(
			pygame.Vector2(1, 0),
			lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
		),
		(
			pygame.Vector2(-1, 0),
			lambda y: pygame.Vector2(
				SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
			),
		),
		(
			pygame.Vector2(0, 1),
			lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
		),
		(
			pygame.Vector2(0, -1),
			lambda x: pygame.Vector2(
				x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
			),
		),
	]

	def __init__(self) -> None:
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.spawn_timer = 0.0

	def spawn(
		self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
	) -> None:
		asteroid = Asteroid(position.x, position.y, radius)
		asteroid.velocity = velocity

	def update(self, dt: float) -> None:
		self.spawn_timer += dt
		if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
			self.spawn_timer = 0

			# spawn a new asteroid at a random edge
			edge = random.choice(self.edges) # pick an edge, returns a list
			speed = random.randint(40, 100) # set a random speed
			velocity = edge[0] * speed # first set velocity to that speed from the selected edge
			velocity = velocity.rotate(random.randint(-30, 30)) # add a rotation to that velocity
			position = edge[1](random.uniform(0, 1)) # picks a spot along the edge to start
			kind = random.randint(1, ASTEROID_KINDS) # sets the size of the asteroid
			self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity) # spawns the rock
