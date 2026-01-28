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
        # Create and run the game using the initialized screen, clock and background
        try:
            # import here to avoid circular imports at module import time
            from src.game import Game
        except Exception:
            # fallback to relative import if package import fails
            from game import Game

        assert self.screen is not None and self.clock is not None
        # pass background surface to Game so it can blit it each frame
        game = Game(self.screen, self.clock)
        game.background = self.bg
        result = game.run()
        # when the game loop finishes, quit pygame
        pygame.quit()
        return result


def main():
    GameDisplay().run()


if __name__ == "__main__":
    main()

