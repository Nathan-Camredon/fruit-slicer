import pygame
from modules.games_logic import FruitGame
import random
import time

def game(screen, clock):
       # Game instance (Fruit Manager)
    game = FruitGame()

    # Timer for fruit spawning
    NEXT_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(NEXT_SPAWN_EVENT, 3000) # Wave every 3 seconds (3000ms)
    t = 0
    c = 0
    running = True
    while running:
        t += 1
        if t % 500 == 0 and c < 5:
            c += 1


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == NEXT_SPAWN_EVENT:
                for _ in range(random.randint(1+c, 2+c)): 
                    game.spawn_fruit()
            elif event.type == pygame.KEYDOWN:
                game.press_key(event.unicode.upper())

        # Update position of all fruits
        game.update()
        
        # Check Game Over
        if game.lives <= 0:
            return "game_over"

        # Draw all fruits
        screen.fill((0, 0, 0)) 
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)