import pygame

from src.VersusGame import VersusGame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Fruit Slicer")
    clock = pygame.time.Clock()
    
    game_instance = VersusGame(screen, clock)
    game_instance.run()
    pygame.quit()

if __name__ == "__main__":
    main()
