import sys

from game import Game

import pygame

vec2 = pygame.math.Vector2
vec3 = pygame.math.Vector3

WINDOW_SIZE = vec2(500, 500)
BLACK = vec3(0, 0, 0)
WHITE = vec3(255, 255, 255)
RED = vec3(255, 0, 0)
BLUE = vec3(0, 0, 255)

if __name__ == '__main__':
    game = Game()
    game.run()

