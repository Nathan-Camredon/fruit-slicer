import pygame
from src.game_display import GameDisplay
from src.ui.background import BackgroundVideo

BACKGROUND = "./assets/Background_video.mp4"


class SubMenu:
    """
    SubMenu implemented using OOP.
    Usage:
        sm = SubMenu(labels, language="en", screen=existing_screen)
        mode = sm.run()  # returns "solo", "1v1" or None
    """

    def __init__(self, labels: dict, language: str = "en", screen: pygame.Surface | None = None,
                 size: tuple[int, int] = (1280, 720), background: str = BACKGROUND, background_video: BackgroundVideo | None = None):
        self.labels = labels
        self.language = language
        self.size = size
        self.background = background
        # If a BackgroundVideo instance is provided, reuse it so the video doesn't restart.
        self.shared_background: BackgroundVideo | None = background_video
        self.owns_background = background_video is None

        self.screen = screen or pygame.display.get_surface() or pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("verdana", 28, bold=True)

        # Buttons
        self.btn_solo = pygame.Rect(240, 320, 400, 95)
        self.btn_1v1 = pygame.Rect(680, 320, 400, 95)
        self.btn_back = pygame.Rect(540, 450, 200, 70)

    def draw_button(self, rect: pygame.Rect, label: str, mouse_pos: tuple[int, int]) -> None:
        is_hovered = rect.collidepoint(mouse_pos)
        bg = (255, 235, 245) if is_hovered else (255, 255, 255)
        pink = (230, 103, 177)
        pygame.draw.rect(self.screen, bg, rect, border_radius=18)
        pygame.draw.rect(self.screen, pink, rect, width=3, border_radius=18)
        text_surf = self.font.render(label, True, pink)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def run(self) -> str | None:
        """Main submenu loop. Returns the selected mode or None."""
        # Use shared BackgroundVideo if provided, otherwise create our own.
        if self.shared_background is not None:
            bg = self.shared_background
            created_here = False
        else:
            bg = BackgroundVideo(self.background, self.size)
            created_here = True

        running = True
        start_ticks = pygame.time.get_ticks()
        selected = None
        try:
            while running:
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btn_solo.collidepoint(event.pos):
                            selected = "solo"
                            running = False
                        elif self.btn_1v1.collidepoint(event.pos):
                            selected = "1v1"
                            running = False
                        elif self.btn_back.collidepoint(event.pos):
                            selected = None
                            running = False

                # Video frame (from BackgroundVideo)
                frame_surface = bg.get_frame_surface()
                self.screen.blit(frame_surface, (0, 0))

                # Labels according to language (fallback to "en")
                labels_local = self.labels.get(self.language, self.labels.get("en", {}))

                # Draw buttons
                self.draw_button(self.btn_solo, labels_local.get("solo", "Solo"), mouse_pos)
                self.draw_button(self.btn_1v1, labels_local.get("1vs1", "1v1"), mouse_pos)
                self.draw_button(self.btn_back, labels_local.get("back", "Back"), mouse_pos)

                pygame.display.flip()
                self.clock.tick(60)
        finally:
            if created_here:
                try:
                    bg.close()
                except Exception:
                    pass

        # If a game mode was selected, launch the game display
        if selected in ("solo", "1v1"):
            try:
                GameDisplay().run()
            except Exception:
                # If launching the game fails, just return the selection
                pass

        return selected