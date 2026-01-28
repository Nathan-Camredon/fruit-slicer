import pygame
import os
import sys
from typing import Optional


class GameDisplay:
    """
    Simple class to show a background image in a pygame window.
    Use GameDisplay.run() to start the display loop.
    """

    def __init__(self, width: int = 1280, height: int = 720, background_filename: str = "Background_image.png"):
        self.width = width
        self.height = height
        self.background_filename = background_filename

        # Compute assets path relative to this module
        self.assets_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets"))
        self.bg_path = os.path.join(self.assets_dir, self.background_filename)

        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.bg: Optional[pygame.Surface] = None

    def load(self) -> bool:
        """
        Initialize pygame, create the window and load the background image.
        Returns True on success, False on failure.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fruit Slicer - Background")
        self.clock = pygame.time.Clock()

        if not os.path.exists(self.bg_path):
            # Background image not found
            print(f"Background image not found: {self.bg_path}", file=sys.stderr)
            return False

        try:
            self.bg = pygame.image.load(self.bg_path).convert()
        except Exception as e:
            print(f"Error loading background image: {e}", file=sys.stderr)
            return False

        # Scale the image to the window size with smooth scaling
        self.bg = pygame.transform.smoothscale(self.bg, (self.width, self.height))
        return True

    def run(self):
        """
        Run the main loop: display the background until the user quits or presses ESC.
        """
        if not self.load():
            pygame.quit()
            return

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # Blit background and update display
            assert self.screen is not None and self.bg is not None
            self.screen.blit(self.bg, (0, 0))
            pygame.display.flip()
            assert self.clock is not None
            self.clock.tick(60)

        pygame.quit()


def main():
    GameDisplay().run()


if __name__ == "__main__":
    main()

