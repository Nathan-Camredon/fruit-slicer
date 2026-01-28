import pygame
from moviepy import VideoFileClip
import json
import os
from modules.submenu import submenu
# from modules.leaderboard import leaderboard

BACKGROUND = "./assets/Background_video.mp4"
EXIT_DOOR_IMG = "./assets/exit_door.png"
GAME_LOGO = "./assets/fruit_slicer_logo.png"
FRANCE_ICON = "./assets/france_icon.png"
UK_ICON = "./assets/united-kingdom_icon.png"


class Menu:
    """Class menu with buttons and languages"""

    def __init__(self, screen_size=(1280, 720)):
        pygame.init()
        self.width, self.height = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Fruit Slicer")
        self.clock = pygame.time.Clock()

        self.language = "en"
        self.labels = self._load_translations()
        self.font = pygame.font.SysFont("verdana", 30, bold=True)

        # Buttons
        self.btn_play = pygame.Rect(240, 400, 400, 95)
        self.btn_leaderboard = pygame.Rect(680, 400, 400, 95)

        # Logo
        self.logo_surface, self.logo_rect = self._load_logo()

        # Exit door
        (self.exit_door_surface,
         self.exit_door_hover_surface,
         self.exit_door_rect) = self._load_exit_door()

        # Flags
        (self.france_surface,
         self.uk_surface,
         self.france_rect,
         self.uk_rect) = self._load_flags()

        # Video background
        self.clip = VideoFileClip(BACKGROUND).resized(screen_size)
        self.duration = self.clip.duration

        self.running = False
        self.start_ticks = 0

    def _load_translations(self):
        json_path = os.path.join(os.path.dirname(__file__), "text_by_language.json")
        try:
            with open(json_path, "r", encoding="utf-8") as jf:
                return json.load(jf)
        except Exception:
            return {
                "en": {"play": "Play", "leaderboard": "Leaderboard"},
                "fr": {"play": "Jouer", "leaderboard": "Classement"},
            }

    def _load_logo(self):
        logo = pygame.image.load(GAME_LOGO).convert_alpha()
        max_logo_width = 600
        if logo.get_width() > max_logo_width:
            scale_ratio = max_logo_width / logo.get_width()
            new_size = (int(logo.get_width() * scale_ratio),
                        int(logo.get_height() * scale_ratio))
            logo = pygame.transform.smoothscale(logo, new_size)
        rect = logo.get_rect(midtop=(self.width // 2, 20))
        return logo, rect

    def _load_exit_door(self):
        surf = pygame.image.load(EXIT_DOOR_IMG).convert_alpha()
        door_height = 146
        door_width = int(surf.get_width() * (door_height / surf.get_height()))
        surf = pygame.transform.smoothscale(surf, (door_width, door_height))
        rect = surf.get_rect(bottomright=(self.width + 10, self.height - 10))
        hover = surf.copy()
        hover.fill((200, 200, 200, 255), special_flags=pygame.BLEND_RGBA_MULT)
        return surf, hover, rect

    def _load_flags(self):
        france = pygame.image.load(FRANCE_ICON).convert_alpha()
        uk = pygame.image.load(UK_ICON).convert_alpha()
        flag_size = (64, 64)
        france = pygame.transform.smoothscale(france, flag_size)
        uk = pygame.transform.smoothscale(uk, flag_size)
        france_rect = france.get_rect(midtop=(self.btn_play.centerx + 170, self.btn_play.bottom + 50))
        uk_rect = uk.get_rect(midtop=(self.btn_leaderboard.centerx - 170, self.btn_leaderboard.bottom + 50))
        return france, uk, france_rect, uk_rect

    def run(self):
        self.running = True
        self.start_ticks = pygame.time.get_ticks()

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                self._handle_event(event)

            # Time in seconds of the video
            elapsed_sec = (pygame.time.get_ticks() - self.start_ticks) / 1000.0
            t = elapsed_sec % self.duration

            frame = self.clip.get_frame(t)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.screen.blit(frame_surface, (0, 0))

            # Draw UI
            self._draw_button(self.btn_play, self.labels.get(self.language, self.labels["en"])["play"], mouse_pos)
            self._draw_button(self.btn_leaderboard, self.labels.get(self.language, self.labels["en"])["leaderboard"], mouse_pos)

            # Flags
            self.screen.blit(self.france_surface, self.france_rect)
            self.screen.blit(self.uk_surface, self.uk_rect)

            # Flag borders / hover
            france_hovered = self.france_rect.collidepoint(mouse_pos)
            uk_hovered = self.uk_rect.collidepoint(mouse_pos)
            self._draw_flag_with_border(self.france_surface, self.france_rect, france_hovered)
            self._draw_flag_with_border(self.uk_surface, self.uk_rect, uk_hovered)

            # Logo
            self.screen.blit(self.logo_surface, self.logo_rect)

            # Exit door
            is_door_hovered = self.exit_door_rect.collidepoint(mouse_pos)
            self.screen.blit(self.exit_door_hover_surface if is_door_hovered else self.exit_door_surface, self.exit_door_rect)

            pygame.display.flip()
            self.clock.tick(60)

        self.clip.close()
        pygame.quit()

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.exit_door_rect.collidepoint(pos):
                self.running = False
            elif self.btn_play.collidepoint(pos):
                try:
                    submenu()
                except NameError:
                    print("Play clicked")
            elif self.btn_leaderboard.collidepoint(pos):
                try:
                    leaderboard()
                except NameError:
                    print("Leaderboard clicked")
            elif self.france_rect.collidepoint(pos):
                self.language = "fr"
            elif self.uk_rect.collidepoint(pos):
                self.language = "en"

    def _draw_button(self, rect: pygame.Rect, label: str, mouse_pos):
        is_hovered = rect.collidepoint(mouse_pos)
        bg = (255, 235, 245) if is_hovered else (255, 255, 255)
        pink = (230, 103, 177)
        pygame.draw.rect(self.screen, bg, rect, border_radius=18)
        pygame.draw.rect(self.screen, pink, rect, width=3, border_radius=18)
        text_surf = self.font.render(label, True, pink)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def _draw_flag_with_border(self, surface, rect, hovered):
        border_color = (255, 255, 255)
        hover_border_color = (255, 192, 203)
        inflate_amount = 16 if hovered else 10
        color = hover_border_color if hovered else border_color
        pygame.draw.ellipse(self.screen, color, rect.inflate(inflate_amount, inflate_amount), width=3)


def menu():
    m = Menu()
    m.run()

