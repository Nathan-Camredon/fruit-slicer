import pygame
from src.fruit_manager import FruitManager
import random
import time

class Game:
    def __init__(self, screen, clock):
        self.timer = 0
        self.tick = 0 
        self.counter = 0
        self.screen = screen
        self.clock = clock
        # optional background surface (blitted every frame before drawing manager)
        self.background = None
        self.manager = FruitManager()
        self.NEXT_SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.NEXT_SPAWN_EVENT, 3000)
    def run(self):
        running = True
        while running:
            result = self.handle_input()
            if result == "quit" or result == "game_over":
                return result
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == self.NEXT_SPAWN_EVENT:
                for _ in range(random.randint(1+self.counter, 2+self.counter)): 
                    self.manager.spawn_fruit()
            elif event.type == pygame.KEYDOWN:
                self.manager.press_key(event.unicode.upper())

        if self.manager.lives <= 0:
            return "game_over"
    def update(self):
        self.manager.update()

        self.tick += 1
        if self.tick % 500 == 0 and self.counter < 5:
            self.counter += 1
    def draw(self):
        # draw background if provided, otherwise clear screen
        if self.background is not None:
            self.screen.blit(self.background, (0, 0))
        else:
            # fill with black by default
            self.screen.fill((0, 0, 0))

        self.manager.draw(self.screen)

