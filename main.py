import pygame

from modules.game import game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Fruit Slicer")
    clock = pygame.time.Clock()
    
    game(screen, clock)
    pygame.quit()

if __name__ == "__main__":
    main()
