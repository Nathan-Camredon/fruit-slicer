import pygame
from typing import Optional


class AskUserName:
    """
    Simple modal to ask the player's name.
    Usage:
        name = AskUserName(screen, clock, background_video=optional_bg).run()
        returns string or None if cancelled
    """

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, background_video=None, prompt: str = "Enter your name:"):
        self.screen = screen
        self.clock = clock
        self.background_video = background_video
        self.prompt = prompt
        self.font = pygame.font.SysFont("verdana", 36)
        self.input_font = pygame.font.SysFont("verdana", 40, bold=True)
        self.width, self.height = self.screen.get_size()

    def draw(self, text: str):
        # draw background (video frame or dark fill)
        if self.background_video is not None and hasattr(self.background_video, "get_frame_surface"):
            try:
                frame = self.background_video.get_frame_surface()
                self.screen.blit(frame, (0, 0))
            except Exception:
                self.screen.fill((20, 20, 20))
        else:
            self.screen.fill((20, 20, 20))

        # overlay box
        box_w, box_h = 700, 120
        box_rect = pygame.Rect((self.width - box_w) // 2, (self.height - box_h) // 2, box_w, box_h)
        pygame.draw.rect(self.screen, (255, 255, 255, 200), box_rect, border_radius=12)
        pygame.draw.rect(self.screen, (230, 103, 177), box_rect, width=3, border_radius=12)

        # prompt
        prompt_surf = self.font.render(self.prompt, True, (60, 60, 60))
        prompt_rect = prompt_surf.get_rect(center=(self.width // 2, box_rect.top - 30))
        self.screen.blit(prompt_surf, prompt_rect)

        # input text
        input_surf = self.input_font.render(text or "_", True, (60, 60, 60))
        input_rect = input_surf.get_rect(center=box_rect.center)
        self.screen.blit(input_surf, input_rect)

        # instructions
        instr = pygame.font.SysFont("verdana", 18).render("Press Enter to confirm, Esc to cancel", True, (200, 200, 200))
        instr_rect = instr.get_rect(center=(self.width // 2, box_rect.bottom + 20))
        self.screen.blit(instr, instr_rect)

    def run(self, max_length: int = 16) -> Optional[str]:
        text = ""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        return text.strip() or None
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        ch = event.unicode
                        if ch and len(text) < max_length and ch.isprintable():
                            text += ch
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # clicking also confirms
                    return text.strip() or None

            self.draw(text)
            pygame.display.flip()
            self.clock.tick(60)

        return None

