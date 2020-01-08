import pygame
from Enemies import *
from Player import *
from configuration import *


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.hero_group = pygame.sprite.Group()
        self.hero = Player(self, RIGHT, 50, 250)
        self.hero_group.add(self.hero)
        self.clock = pygame.time.Clock()
        self.game_cycle()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.USEREVENT:
                if not self.hero.dead:
                    self.hero.tick()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.hero.up = True
                if event.key == pygame.K_RIGHT:
                    self.hero.right = True
                    self.hero.direction = RIGHT
                if event.key == pygame.K_LEFT:
                    self.hero.left = True
                    self.hero.direction = LEFT

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.hero.up = False
                if event.key == pygame.K_RIGHT:
                    self.hero.right = False
                if event.key == pygame.K_LEFT:
                    self.hero.left = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.hero.stunned:
                    if event.button == pygame.BUTTON_LEFT and not self.hero.is_default_attack and \
                            not self.hero.is_range_attack and self.hero.stamina >= HERO_DA_COST:
                        self.hero.stamina -= HERO_DA_COST
                        self.hero.is_default_attack = True
                    elif event.button == pygame.BUTTON_RIGHT and not self.hero.is_range_attack and \
                            not self.hero.is_default_attack and self.hero.stamina >= HERO_RA_COST:
                        self.hero.stamina -= HERO_RA_COST
                        self.hero.is_range_attack = True

    def update(self):
        if not self.hero.dead:
            self.hero.update()
        self.hero.hero_melee_attacks.update()
        self.hero.hero_range_attacks.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.hero_group.draw(self.screen)
        self.hero.hero_melee_attacks.draw(self.screen)
        self.hero.hero_range_attacks.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

    def game_cycle(self):
        pygame.time.set_timer(pygame.USEREVENT, 1000)  # изменение состояния персонажа(здоровье и прочее)
        while self.running:
            self.events()
            self.update()
            self.render()
        pygame.quit()


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game = Main(screen)
