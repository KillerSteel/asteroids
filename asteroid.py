from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

import pygame
import random

class Asteroid(CircleShape):

	def __init__(self, x: float, y: float, radius: float) -> None:
		super().__init__(x, y, radius)

	def draw(self, screen: pygame.Surface) -> None:
		pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

	def update(self, dt: float) -> None:
		self.position += (self.velocity * dt)

	def split(self) -> None:
		self.kill()
		if (self.radius <= ASTEROID_MIN_RADIUS):
			return

		log_event("asteroid_split")
		angle = random.uniform(20,50) # angle to spawn the two new rocks at
		asteroid_one_velocity = self.velocity.rotate(angle)
		asteroid_two_velocity = self.velocity.rotate(angle * -1)

		new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS

		asteroid_one = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
		asteroid_one.velocity = asteroid_one_velocity * 1.2

		asteroid_two = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
		asteroid_two.velocity = asteroid_two_velocity * 1.2
