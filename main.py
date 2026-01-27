import pygame
from modules.games_logic import FruitGame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Fruit Slicer")
    clock = pygame.time.Clock()
    
    # Instance du jeu (Gestionnaire de fruits)
    game = FruitGame()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Appuyer sur ESPACE pour lancer un nouveau fruit !
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                     game.spawn_fruit()
                else:
                    # On envoie la lettre tapée (en majuscule) au jeu
                    game.press_key(event.unicode.upper())

        # Update (Mise à jour de tous les fruits)
        game.update()
        # Draw (Dessin de tous les fruits)
        screen.fill((0, 0, 0)) 
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
