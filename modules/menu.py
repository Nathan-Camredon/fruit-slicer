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


def menu():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Fruit Slicer")
    clock = pygame.time.Clock()

    language = "en"

    # Load translations from JSON file
    json_path = os.path.join(os.path.dirname(__file__), "text_by_language.json")
    try:
        with open(json_path, "r", encoding="utf-8") as jf:
            labels = json.load(jf)
    except Exception:
        # Fallback translations if JSON fails to load
        labels = {
            "en": {"play": "Play", "leaderboard": "Leaderboard"},
            "fr": {"play": "Jouer", "leaderboard": "Classement"},
        }

    # Fonts and UI settings
    font = pygame.font.SysFont("verdana", 30, bold=True)

    # Button rectangles (white buttons)
    # Play on the left, Leaderboard on the right
    btn_play = pygame.Rect(240, 400, 400, 95)
    btn_leaderboard = pygame.Rect(680, 400, 400, 95)

    # Game logo (top center)
    logo_surface = pygame.image.load(GAME_LOGO).convert_alpha()
    # Scale logo to fit 
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
    door_height = 146
    door_width = int(exit_door_surface.get_width() * (door_height / exit_door_surface.get_height()))
    exit_door_surface = pygame.transform.smoothscale(exit_door_surface, (door_width, door_height))
    exit_door_rect = exit_door_surface.get_rect(bottomright=(1280 + 10 , 720 - 10))
    # Precompute a "gray-ish" version for hover (multiply RGB, keep alpha)
    exit_door_hover_surface = exit_door_surface.copy()
    exit_door_hover_surface.fill((200, 200, 200, 255), special_flags=pygame.BLEND_RGBA_MULT)

    # Language flags (below buttons)
    france_surface = pygame.image.load(FRANCE_ICON).convert_alpha()
    uk_surface = pygame.image.load(UK_ICON).convert_alpha()
    # Scale flags to 64x64 (nice icon size)
    flag_size = (64, 64)
    france_surface = pygame.transform.smoothscale(france_surface, flag_size)
    uk_surface = pygame.transform.smoothscale(uk_surface, flag_size)
    # Position flags centered under each button
    france_rect = france_surface.get_rect(midtop=(btn_play.centerx + 170, btn_play.bottom + 50))
    uk_rect = uk_surface.get_rect(midtop=(btn_leaderboard.centerx - 170, btn_leaderboard.bottom + 50))

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
                    # Try to call submenu() if available, otherwise fallback to print
                    try:
                        submenu(language, labels)
                    except NameError:
                        print("Play clicked")
                elif btn_leaderboard.collidepoint(event.pos):
                    try:
                        leaderboard()
                    except NameError:
                        print("Leaderboard clicked")
                elif france_rect.collidepoint(event.pos):
                    language = "fr"

                elif uk_rect.collidepoint(event.pos):
                    # UK flag maps to English
                    language = "en"

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

        # Draw buttons using current language labels
        draw_button(btn_play, labels.get(language, labels["en"])["play"])
        draw_button(btn_leaderboard, labels.get(language, labels["en"])["leaderboard"])

        # Draw language flags under buttons (for future language selection)
        screen.blit(france_surface, france_rect)
        screen.blit(uk_surface, uk_rect)

        # Hover effect + white circular borders around flags
        border_color = (255, 255, 255)
        hover_border_color = (255, 192, 203)  # light pink when hovered

        france_hovered = france_rect.collidepoint(mouse_pos)
        uk_hovered = uk_rect.collidepoint(mouse_pos)

        # Slight scale up on hover
        def draw_flag_with_border(surface, rect, hovered):
            inflate_amount = 16 if hovered else 10
            color = hover_border_color if hovered else border_color
            pygame.draw.ellipse(screen, color, rect.inflate(inflate_amount, inflate_amount), width=3)

        draw_flag_with_border(france_surface, france_rect, france_hovered)
        draw_flag_with_border(uk_surface, uk_rect, uk_hovered)

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

