import math
import sys
from enum import Enum

import pygame
import random

vec3 = pygame.math.Vector3
vec2 = pygame.math.Vector2

WINDOW_SIZE = vec2(500, 500)

WHITE = vec3(255)
BLACK = vec3(0)


class GameStates(Enum):
    SPLASH = 0,
    RUNNING = 1,
    GAME_OVER = 2


class Game:
    def __init__(self):
        self.clock = None
        self.surface = None
        self.state = None

        self.sliders = None
        self.ball = None

        self.splash = None
        self.end = None
        self.divider = None

        self.font = None

        self.scores = None

    def run(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        self.surface.fill(BLACK)

        pygame.display.set_caption("Pong")
        pygame.display.update()

        try:
            self.font = pygame.font.Font("C:\\WINDOWS\\FONTS\\MONOCRAFT.OTF", 32)
        except FileNotFoundError:
            self.font = pygame.font.Font(pygame.font.get_default_font(), 32)

        self.scores = {
            'left': 0,
            'right': 0
        }

        self.splash = pygame.image.load("resources/splash-screen.png").convert()
        self.end = pygame.image.load("resources/end-screen.png").convert()
        self.divider = pygame.image.load("resources/divider.png").convert()

        self.sliders = pygame.sprite.Group()

        self.reset()

        self.state = GameStates.SPLASH

        while 1:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.state == GameStates.SPLASH:
                            self.reset()
                            self.state = GameStates.RUNNING

                        if self.state == GameStates.GAME_OVER:
                            self.state = GameStates.SPLASH

                    if event.key == pygame.K_q:
                        self.state = GameStates.GAME_OVER

            if self.state == GameStates.SPLASH:
                self.surface.blit(self.splash, self.splash.get_rect())

            if self.state == GameStates.RUNNING:
                self.update_game()

            if self.state == GameStates.GAME_OVER:
                self.surface.blit(self.end, self.end.get_rect())

            pygame.display.update()
            self.surface.fill(BLACK)

    def update_game(self):
        self.ball.update()
        self.surface.blit(self.ball.image, self.ball.rect)
        self.sliders.update(pygame.key.get_pressed())
        self.sliders.draw(self.surface)

        rect = self.divider.get_rect()
        rect.center = (WINDOW_SIZE // 2)
        self.surface.blit(self.divider, rect)

        scores = self.font.render(f"{self.scores.get('left')}  {self.scores.get('right')}", True, WHITE)
        rect = scores.get_rect()
        rect.center = (WINDOW_SIZE.x // 2, 30)
        self.surface.blit(scores, rect)

        if pygame.sprite.collide_rect(self.ball, self.sliders.sprites()[1]) \
                or pygame.sprite.collide_rect(self.ball,  self.sliders.sprites()[0]):
            self.ball.reflect(random.random() * 90)

    def set_state(self, state):
        self.state = state

    def soft_reset(self):
        self.ball = Ball(vec2(WINDOW_SIZE // 2), self)
        self.sliders.empty()
        self.sliders.add(Slider(vec2(20, WINDOW_SIZE.x // 2), self))
        self.sliders.add(Slider(vec2(WINDOW_SIZE.x - 20, WINDOW_SIZE.x // 2), self))

    def reset(self):
        self.ball = Ball(vec2(WINDOW_SIZE // 2), self)
        self.sliders.empty()
        self.sliders.add(Slider(vec2(20, WINDOW_SIZE.x // 2), self))
        self.sliders.add(Slider(vec2(WINDOW_SIZE.x - 20, WINDOW_SIZE.x // 2), self))
        self.scores['left'] = 0
        self.scores['right'] = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self, start_pos, game):
        super().__init__()
        self.pos = vec2(start_pos)

        direction = random.randint(0, 1)
        if direction == 0:
            direction = -1

        self.vel = vec2(4 * direction, 0)

        self.image = pygame.image.load("resources/ball.png").convert()
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

        self.game = game

    def update(self):
        if self.pos.y < 0:
            self.vel = self.vel.reflect(vec2(0, 1))

        elif self.pos.y > WINDOW_SIZE.y:
            self.vel = self.vel.reflect(vec2(0, -1))

        elif self.pos.x < 0:
            self.game.soft_reset()
            self.game.scores['left'] += 1

        elif self.pos.x > WINDOW_SIZE.x:
            self.game.soft_reset()
            self.game.scores['right'] += 1

        self.pos += self.vel
        self.rect.center = self.pos

    def reflect(self, angle=None):
        if angle is not None:
            # Calculate the new velocity based on the angle of reflection
            self.vel.rotate_ip(math.degrees(2 * angle))
        else:
            # Default behavior: reflect along the current velocity vector
            self.vel.reflect_ip(self.vel)


class Slider(pygame.sprite.Sprite):
    def __init__(self, start_pos, game):
        super().__init__()
        self.pos = vec2(start_pos)
        self.vel = vec2(0)

        self.image = pygame.image.load("resources/slider.png").convert()

        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

        self.game = game

    def update(self, keys):
        i = 0
        if keys[pygame.K_w]:
            i = -10
        elif keys[pygame.K_s]:
            i = 10

        if not self.pos.y + i >= 40:
            self.pos.y = 40
        elif not self.pos.y + i <= 460:
            self.pos.y = 460
        else:
            self.pos += vec2(0, i)

        self.rect.center = self.pos
