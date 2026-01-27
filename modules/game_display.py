import pygame
import os
import sys


def show_background(width: int = 1280, height: int = 720):
    """
    Display a simple screen with the provided background image.
    When called directly, opens a Pygame window and closes it when the user quits.
    """
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Fruit Slicer - Background")
    clock = pygame.time.Clock()

    # Path to the image in ../assets/Background_image.png
    img_path = os.path.join(os.path.dirname(__file__), "..", "assets", "Background_image.png")
    img_path = os.path.normpath(img_path)

    if not os.path.exists(img_path):
        print(f"Image de fond introuvable : {img_path}", file=sys.stderr)
        pygame.quit()
        return

    try:
        bg = pygame.image.load(img_path).convert()
    except Exception as e:
        print(f"Erreur lors du chargement de l'image : {e}", file=sys.stderr)
        pygame.quit()
        return

    # Scale the image to fill the window while preserving quality
    bg = pygame.transform.smoothscale(bg, (width, height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(bg, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    show_background()

