import pygame
import json
import os

class Leaderboard:
    """
    Class to handle the loading, saving, and displaying of high scores.
    """

    def __init__(self, screen):
        """Initialize paths, fonts, and load existing data."""
        self.screen = screen
        self.file_path = "scores.json"
        self.bg_path = "assets/img/leaderboard_background.png"
        
        # Initialize fonts
        self.font_title = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 30)
        
        # Load initial scores from the JSON file
        self.scores = self._load_data()

    def _load_data(self):
        """Private method to read scores from the JSON file."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def add_score(self, name, score):
        """Add a new score and save the top 10 to the file."""
        self.scores.append({"name": name, "score": score})
        
        # Sort scores in descending order based on points
        self.scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)[:10]
        
        # Write updated list to JSON
        with open(self.file_path, "w") as f:
            json.dump(self.scores, f, indent=4)

    def display(self):
        """Main loop for the leaderboard visual interface."""
        # Load and scale the background image
        try:
            bg = pygame.image.load(self.bg_path).convert()
            bg = pygame.transform.scale(bg, self.screen.get_size())
        except pygame.error:
            bg = pygame.Surface(self.screen.get_size())
            bg.fill((40, 40, 40))

        running = True
        while running:
            # 1. Draw Background
            self.screen.blit(bg, (0, 0))
            
            # 2. Draw a semi-transparent overlay for readability
            overlay = pygame.Surface((450, 520), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170)) # Black with alpha
            self.screen.blit(overlay, (self.screen.get_width()//2 - 225, 40))

            # 3. Render Header
            title_surf = self.font_title.render("TOP 10 NINJAS", True, (255, 255, 255))
            self.screen.blit(title_surf, (self.screen.get_width()//2 - title_surf.get_width()//2, 60))

            # 4. Render Score List
            for i, entry in enumerate(self.scores):
                # Format: 1. PlayerName - 150 pts
                rank_text = f"{i+1}. {entry['name']} - {entry['score']} pts"
                score_surf = self.font_text.render(rank_text, True, (230, 230, 230))
                self.screen.blit(score_surf, (self.screen.get_width()//2 - 180, 140 + i * 40))

            # 5. Exit Instruction
            exit_txt = self.font_text.render("Press ESC to return to Menu", True, (200, 200, 200))
            self.screen.blit(exit_txt, (self.screen.get_width()//2 - exit_txt.get_width()//2, 580))

            pygame.display.flip()

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False