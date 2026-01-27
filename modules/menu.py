import pygame
from moviepy import VideoFileClip
from modules.submenu import submenu
from modules.leaderboard import leaderboard

BACKGROUND = "./assets/Background_video.mp4"
EXIT_DOOR_IMG = "./assets/exit_door.png"
GAME_LOGO = "./assets/fruit_slicer_logo.png"


def menu():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Fruit Slicer")
    clock = pygame.time.Clock()

    # Fonts and UI settings
    font = pygame.font.SysFont("verdana", 30, bold=True)

    # Button rectangles (white buttons)
    # Play on the left, Leaderboard on the right
    btn_play = pygame.Rect(240, 400, 400, 95)
    btn_leaderboard = pygame.Rect(680, 400, 400, 95)

    # Game logo (top center)
    logo_surface = pygame.image.load(GAME_LOGO).convert_alpha()
    # Scale logo to fit nicely at top (max width 900px)
    max_logo_width = 600
    if logo_surface.get_width() > max_logo_width:
        scale_ratio = max_logo_width / logo_surface.get_width()
        new_size = (int(logo_surface.get_width() * scale_ratio),
                    int(logo_surface.get_height() * scale_ratio))
        logo_surface = pygame.transform.smoothscale(logo_surface, new_size)
    logo_rect = logo_surface.get_rect(midtop=(1280 // 2, 20))

    # Exit door (bottom-right) - click to quit
    exit_door_surface = pygame.image.load(EXIT_DOOR_IMG).convert_alpha()
    # Scale door to a reasonable size for 1280x720
    door_height = 180
    door_width = int(exit_door_surface.get_width() * (door_height / exit_door_surface.get_height()))
    exit_door_surface = pygame.transform.smoothscale(exit_door_surface, (door_width, door_height))
    exit_door_rect = exit_door_surface.get_rect(bottomright=(1280 + 12 , 720 - 10))
    # Precompute a "gray-ish" version for hover (multiply RGB, keep alpha)
    exit_door_hover_surface = exit_door_surface.copy()
    exit_door_hover_surface.fill((200, 200, 200, 255), special_flags=pygame.BLEND_RGBA_MULT)

    # Init video and load it in screen size
    clip = VideoFileClip(BACKGROUND).resized((1280, 720))
    duration = clip.duration

    running = True
    start_ticks = pygame.time.get_ticks()

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Handle button clicks
                if exit_door_rect.collidepoint(event.pos):
                    # Clicking the door exits the menu
                    running = False
                elif btn_play.collidepoint(event.pos):
                    submenu()
                    print("Play clicked")
                elif btn_leaderboard.collidepoint(event.pos):
                    leaderboard()
                    print("Leaderboard clicked")

        # Time in seconds of the video 
        elapsed_sec = (pygame.time.get_ticks() - start_ticks) / 1000.0
        t = elapsed_sec % duration

        # Get the frame and convert into Surface Pygame
        frame = clip.get_frame(t)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Display the frame
        screen.blit(frame_surface, (0, 0))

        # Draw white buttons on top of the video
        def draw_button(rect: pygame.Rect, label: str):
            # Simple hover effect (slightly gray)
            is_hovered = rect.collidepoint(mouse_pos)
            bg = (255, 235, 245) if is_hovered else (255, 255, 255)
            pink = (230, 103, 177)

            # Rounded rectangle + subtle border
            pygame.draw.rect(screen, bg, rect, border_radius=18)
            pygame.draw.rect(screen, pink, rect, width=3, border_radius=18)

            # Centered text
            text_surf = font.render(label, True, pink)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        draw_button(btn_play, "Play")
        draw_button(btn_leaderboard, "Leaderboard")

        # Draw logo at the top center
        screen.blit(logo_surface, logo_rect)

        # Draw exit door on top of the video (bottom-right)
        is_door_hovered = exit_door_rect.collidepoint(mouse_pos)
        # Hover effect: slightly gray door
        screen.blit(exit_door_hover_surface if is_door_hovered else exit_door_surface, exit_door_rect)

        pygame.display.flip()
        clock.tick(60)

    clip.close()
    pygame.quit()

