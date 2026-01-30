import pygame
import os
import sys
from typing import Optional
from src.Game import Game

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

    def run(self, mode: str = "solo"):
        """
        Run the main loop: display the background until the user quits or presses ESC.
        """
        if not self.load():
            pygame.quit()
            return
        # Create and run the game using the initialized screen, clock and background
        try:
            # import here to avoid circular imports at module import time
            from src.Game import Game
            from src.VersusGame import VersusGame
        except Exception:
            # fallback to relative import if package import fails
            from Game import Game
            from VersusGame import VersusGame

        assert self.screen is not None and self.clock is not None
        
        # pass background surface to Game so it can blit it each frame
        if mode == "1v1":
            game = VersusGame(self.screen, self.clock)
        else:
            game = Game(self.screen, self.clock)
            
        game.background = self.bg
        result = game.run()

        # If the game ended with a game over, show a brief "You lost" screen
        # and then return control to the caller (e.g., the menu).
        if result == "game_over":
            # Prepare message
            font = pygame.font.SysFont("verdana", 64, bold=True)
            
            message = "You lost"
            color = (255, 255, 255)
            
            # Check for 1v1 winner
            if mode == "1v1" and hasattr(game, "score_p1") and hasattr(game, "score_p2"):
                if game.score_p1 > game.score_p2:
                    message = "Player 1 Wins!"
                    color = (255, 100, 100) 
                elif game.score_p2 > game.score_p1:
                    message = "Player 2 Wins!"
                    color = (100, 255, 100) 
                else:
                    message = "Draw!"
            
            text_surf = font.render(message, True, color)
            text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2))

            end_time = pygame.time.get_ticks() + 3000  # show for 3 seconds
            while pygame.time.get_ticks() < end_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "quit"
                # draw background if available
                if self.bg is not None:
                    self.screen.blit(self.bg, (0, 0))
                else:
                    self.screen.fill((0, 0, 0))
                self.screen.blit(text_surf, text_rect)
                pygame.display.flip()
                # keep timing consistent with main loop
                if self.clock is not None:
                    self.clock.tick(60)

        # Leave pygame initialized; top-level code handles quitting.
        return result

