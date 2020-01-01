import pygame
from configuration import *
from Player import Player


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.hero_group = pygame.sprite.Group()
        self.hero = Player(50, 50, screen)
        self.hero_group.add(self.hero)
        self.solid_blocks = []
        self.clock = pygame.time.Clock()
        self.up = self.right = self.left = False
        self.direction = RIGHT
        self.game_cycle()

    def game_cycle(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.up = True
                    if event.key == pygame.K_RIGHT:
                        self.right = True
                        self.direction = RIGHT
                    if event.key == pygame.K_LEFT:
                        self.left = True
                        self.direction = LEFT

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.up = False
                    if event.key == pygame.K_RIGHT:
                        self.right = False
                    if event.key == pygame.K_LEFT:
                        self.left = False
            self.screen.fill((0, 0, 0))
            self.hero.update(self.direction, self.left, self.right, self.up, self.solid_blocks)
            self.hero_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game = Main(screen)
