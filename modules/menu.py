import pygame
import os
import json
from moviepy import VideoFileClip
from modules.ui.button import Button, ImageButton
from modules.submenu import SubMenu

# Paths configuration
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BACKGROUND = os.path.join(BASE_DIR, "assets/Background_video.mp4")
EXIT_DOOR_IMG = os.path.join(BASE_DIR, "assets/exit_door.png")
GAME_LOGO = os.path.join(BASE_DIR, "assets/fruit_slicer_logo.png")
FRANCE_ICON = os.path.join(BASE_DIR, "assets/france_icon.png")
UK_ICON = os.path.join(BASE_DIR, "assets/united-kingdom_icon.png")
JSON_PATH = os.path.join(BASE_DIR, "text_by_language.json")

class Menu:
    def __init__(self, screen_size=(1280, 720)):
        pygame.init()
        self.width, self.height = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Fruit Slicer")
        self.clock = pygame.time.Clock()

        self.language = "en"
        self.labels = self._load_translations()
        self.font = pygame.font.SysFont("verdana", 30, bold=True)

        # 1. Setup Main Buttons
        self.btn_play = Button(240, 400, 400, 95, self._get_text("play"), self.font)
        self.btn_leaderboard = Button(680, 400, 400, 95, self._get_text("leaderboard"), self.font)

        # 2. Setup Flags
        f_img = pygame.transform.smoothscale(pygame.image.load(FRANCE_ICON).convert_alpha(), (64, 64))
        u_img = pygame.transform.smoothscale(pygame.image.load(UK_ICON).convert_alpha(), (64, 64))
        self.flag_fr = ImageButton(self.btn_play.rect.centerx + 100, self.btn_play.rect.bottom + 40, f_img)
        self.flag_en = ImageButton(self.btn_leaderboard.rect.centerx - 170, self.btn_leaderboard.rect.bottom + 40, u_img)

        # 3. Logo & Exit Door
        self.logo_surf, self.logo_rect = self._load_logo()
        self.door_surf, self.door_hover, self.door_rect = self._load_exit_door()

        # 4. Background Video
        self.clip = VideoFileClip(BACKGROUND).resized(screen_size)
        self.duration = self.clip.duration
        self.running = False

    def _load_translations(self):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as jf:
                return json.load(jf)
        except Exception:
            return {"en": {"play": "Play", "leaderboard": "Leaderboard"}, "fr": {"play": "Jouer", "leaderboard": "Classement"}}

    def _get_text(self, key):
        return self.labels.get(self.language, self.labels["en"]).get(key, key)

    def _load_logo(self):
        img = pygame.image.load(GAME_LOGO).convert_alpha()
        img = pygame.transform.smoothscale(img, (600, int(img.get_height() * (600/img.get_width()))))
        return img, img.get_rect(midtop=(self.width // 2, 20))

    def _load_exit_door(self):
        surf = pygame.image.load(EXIT_DOOR_IMG).convert_alpha()
        surf = pygame.transform.smoothscale(surf, (120, 146))
        rect = surf.get_rect(bottomright=(self.width - 10, self.height - 10))
        hover = surf.copy()
        hover.fill((200, 200, 200, 255), special_flags=pygame.BLEND_RGBA_MULT)
        return surf, hover, rect

    def run(self):
        self.running = True
        start_ticks = pygame.time.get_ticks()

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                self._handle_events(event)

            # Video Background logic
            t = ((pygame.time.get_ticks() - start_ticks) / 1000.0) % self.duration
            frame = pygame.surfarray.make_surface(self.clip.get_frame(t).swapaxes(0, 1))
            self.screen.blit(frame, (0, 0))

            # Draw Everything
            self.btn_play.draw(self.screen, mouse_pos)
            self.btn_leaderboard.draw(self.screen, mouse_pos)
            self.flag_fr.draw(self.screen, mouse_pos)
            self.flag_en.draw(self.screen, mouse_pos)
            self.screen.blit(self.logo_surf, self.logo_rect)

            door_img = self.door_hover if self.door_rect.collidepoint(mouse_pos) else self.door_surf
            self.screen.blit(door_img, self.door_rect)

            pygame.display.flip()
            self.clock.tick(60)
        
        self.clip.close()
        pygame.quit()

    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_play.is_clicked(event.pos):
                SubMenu(self.labels, self.language, self.screen).run()
            elif self.flag_fr.is_clicked(event.pos):
                self.language = "fr"
                self._update_language()
            elif self.flag_en.is_clicked(event.pos):
                self.language = "en"
                self._update_language()
            elif self.door_rect.collidepoint(event.pos):
                self.running = False

    def _update_language(self):
        self.btn_play.update_text(self._get_text("play"))
        self.btn_leaderboard.update_text(self._get_text("leaderboard"))