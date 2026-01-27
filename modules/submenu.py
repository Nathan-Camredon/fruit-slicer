import pygame
from moviepy import VideoFileClip

BACKGROUND = "./assets/Background_video.mp4"


def submenu(language, labels):
    """
    Simple submenu with two buttons (Solo, 1v1) matching main menu style.
    Uses the existing display surface if available.
    Returns the selected mode as a string ("solo" or "1v1") or None if exited.
    """
    screen = pygame.display.get_surface()
    if screen is None:
        screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("verdana", 28, bold=True)

    # Buttons: left = Solo, right = 1v1
    btn_solo = pygame.Rect(240, 320, 400, 95)
    btn_1v1 = pygame.Rect(680, 320, 400, 95)
    # Back button to return to main menu
    btn_back = pygame.Rect(540, 450, 200, 70)

    # Video background (same as main menu)
    clip = VideoFileClip(BACKGROUND).resized((1280, 720))
    duration = clip.duration

    running = True
    start_ticks = pygame.time.get_ticks()
    selected = None

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_solo.collidepoint(event.pos):
                    selected = "solo"
                    print("Solo selected")
                    running = False
                elif btn_1v1.collidepoint(event.pos):
                    selected = "1v1"
                    print("1v1 selected")
                    running = False
                elif btn_back.collidepoint(event.pos):
                    # Return to main menu without selecting a mode
                    selected = None
                    running = False

        # Video frame
        elapsed_sec = (pygame.time.get_ticks() - start_ticks) / 1000.0
        t = elapsed_sec % duration
        frame = clip.get_frame(t)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        # Draw buttons (same style)
        def draw_button(rect: pygame.Rect, label: str):
            is_hovered = rect.collidepoint(mouse_pos)
            bg = (255, 235, 245) if is_hovered else (255, 255, 255)
            pink = (230, 103, 177)
            pygame.draw.rect(screen, bg, rect, border_radius=18)
            pygame.draw.rect(screen, pink, rect, width=3, border_radius=18)
            text_surf = font.render(label, True, pink)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        draw_button(btn_solo, labels.get(language, labels["en"])["solo"])
        draw_button(btn_1v1, labels.get(language, labels["en"])["1vs1"])
        draw_button(btn_back, labels.get(language, labels["en"])["back"])

        pygame.display.flip()
        clock.tick(60)

    clip.close()
    return selected