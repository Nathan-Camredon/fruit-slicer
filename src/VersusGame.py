import pygame
import random
from .Game import Game

class VersusGame(Game):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.start_time = pygame.time.get_ticks()
        self.score_p1 = 0
        self.score_p2 = 0
    
    def handle_input(self):
        if pygame.time.get_ticks() - self.start_time > 60000: #1 minutes
            return "game_over"

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return "quit"
        
            elif event.type == self.NEXT_SPAWN_EVENT:
                for _ in range(random.randint(3+self.counter, 5+self.counter)): 
                    self.manager.spawn_fruit()
            elif event.type == pygame.KEYDOWN:
                key = event.unicode.upper()
                
                if key in "AZER":
                    # Player 1 (Left)
                    points = self.manager.press_key(key, self.score_p1)
                    if points:
                        self.score_p1 += points
                        points = 0
                elif key in "UIOP":
                    # Player 2 (Right)
                    points = self.manager.press_key(key, self.score_p2)
                    self.score_p2 += points
                    points = 0
    def draw(self):
        # draw background if provided, otherwise clear screen (reuse Game behavior)
        if self.background is not None:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        # Draw fruits (but NOT the default UI with lives)
        for fruit in self.manager.fruits:
            fruit.draw(self.screen)

        # Draw Versus Score UI
        font = pygame.font.SysFont(None, 50)
        
        # P1 Score (Left - Red/Blue?)
        text_p1 = font.render(f"P1: {self.score_p1}", True, (255, 100, 100))
        self.screen.blit(text_p1, (50, 50))

        # P2 Score (Right - Green?)
        text_p2 = font.render(f"P2: {self.score_p2}", True, (100, 255, 100))
        self.screen.blit(text_p2, (1000, 50))
        
        # Timer
        time_left = 60 - (pygame.time.get_ticks() - self.start_time) // 1000
        text_time = font.render(f"{time_left}", True, (255, 255, 255))
        self.screen.blit(text_time, (600, 50))