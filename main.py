import pygame

from src.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Fruit Slicer")
    clock = pygame.time.Clock()
    
    game_instance = Game(screen, clock)
    game_instance.run()
    pygame.quit()

if __name__ == "__main__":
    main()
