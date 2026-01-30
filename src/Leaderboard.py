import os
import json
import pygame
from typing import List, Tuple, Optional


class Leaderboard:
    """
    OOP leaderboard viewer.
    Usage:
        lb = Leaderboard(screen, clock, background=optional_surface)
        lb.run()  # blocks until user returns (ESC or click) and then returns
    It reads scores from data/score.json and ranks users by their best score.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        background: Optional[pygame.Surface] = None,
        data_path: Optional[str] = None,
        max_entries: int = 10,
    ):
        self.screen = screen
        self.clock = clock
        self.background = background
        self.max_entries = max_entries

        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_path = data_path or os.path.join(base_dir, "data", "score.json")

        # Prefer a static leaderboard image over a provided BackgroundVideo.
        # This ensures the leaderboard screen shows the intended static background
        # even if the caller passed a BackgroundVideo object.
        try:
            leaderboard_img = os.path.join(base_dir, "assets", "Background_leaderboard_image.png")
            if os.path.exists(leaderboard_img):
                surf = pygame.image.load(leaderboard_img)
                # convert with alpha if available
                try:
                    surf = surf.convert_alpha()
                except Exception:
                    surf = surf.convert()
                # scale to screen size
                surf = pygame.transform.smoothscale(surf, (self.screen.get_width(), self.screen.get_height()))
                self.background = surf
        except Exception:
            # ignore failures and keep the provided background (if any) or None
            pass

        # Visuals
        self.title_font = pygame.font.SysFont("verdana", 56, bold=True)
        self.entry_font = pygame.font.SysFont("verdana", 32)
        self.small_font = pygame.font.SysFont("verdana", 20)
        self.width, self.height = self.screen.get_size()

    def load_scores(self) -> List[Tuple[str, int]]:
        """Return a list of (name, best_score) sorted descending."""
        if not os.path.exists(self.data_path) or os.path.getsize(self.data_path) == 0:
            return []

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return []

        users = []
        try:
            solo = data.get("solo", {})
            utilisateurs = solo.get("utilisateurs", [])
            for u in utilisateurs:
                name = u.get("nom", "Unknown")
                scores = u.get("scores", [])
                best = max(scores) if scores else 0
                users.append((name, best))
        except Exception:
            return []

        # sort by score desc
        users.sort(key=lambda x: x[1], reverse=True)
        return users

    def draw(self, entries: List[Tuple[str, int]]):
        # draw background if available. Accept either a pygame.Surface or a
        # BackgroundVideo-like object (has get_frame_surface()).
        if self.background is not None:
            try:
                # If background provides a frame method (BackgroundVideo), use it.
                if hasattr(self.background, "get_frame_surface"):
                    frame = self.background.get_frame_surface()
                    self.screen.blit(frame, (0, 0))
                else:
                    # assume it's a pygame.Surface
                    self.screen.blit(self.background, (0, 0))
            except Exception:
                # fallback to solid fill if anything goes wrong
                self.screen.fill((10, 10, 10))
        else:
            self.screen.fill((10, 10, 10))

        # Title
        title_surf = self.title_font.render("Leaderboard", True, (230, 103, 177))
        title_rect = title_surf.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_surf, title_rect)

        # Column headers
        header_name = self.entry_font.render("Player", True, (255, 255, 255))
        header_score = self.entry_font.render("Score", True, (255, 255, 255))
        self.screen.blit(header_name, (self.width // 4 - header_name.get_width() // 2, 150))
        self.screen.blit(header_score, (3 * self.width // 4 - header_score.get_width() // 2, 150))

        # Entries
        start_y = 200
        gap = 40
        for idx, (name, score) in enumerate(entries[: self.max_entries], start=1):
            y = start_y + (idx - 1) * gap
            rank_surf = self.entry_font.render(f"{idx}.", True, (200, 200, 200))
            name_surf = self.entry_font.render(name, True, (255, 255, 255))
            score_surf = self.entry_font.render(str(score), True, (255, 255, 255))

            self.screen.blit(rank_surf, (self.width // 8 - rank_surf.get_width() // 2, y))
            self.screen.blit(name_surf, (self.width // 4 - name_surf.get_width() // 2, y))
            self.screen.blit(score_surf, (3 * self.width // 4 - score_surf.get_width() // 2, y))

        # Footer / instructions
        instr = self.small_font.render("Press ESC or click to return", True, (180, 180, 180))
        instr_rect = instr.get_rect(center=(self.width // 2, self.height - 40))
        self.screen.blit(instr, instr_rect)

    def run(self):
        """Main loop: shows the leaderboard until the user presses ESC or clicks."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    running = False

            entries = self.load_scores()
            self.draw(entries)
            pygame.display.flip()
            self.clock.tick(60)

        return None

