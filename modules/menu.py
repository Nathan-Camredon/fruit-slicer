import pygame
from moviepy import VideoFileClip

BACKGROUND = "./assets/Background_video.mp4"


def menu():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Fruit Slicer")
    clock = pygame.time.Clock()

    # Init video and load it in screen size
    clip = VideoFileClip(BACKGROUND).resized((1280, 720))
    duration = clip.duration

    running = True
    start_ticks = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Time in seconds of the video 
        elapsed_sec = (pygame.time.get_ticks() - start_ticks) / 1000.0
        t = elapsed_sec % duration

        # Get the frame and convert into Surface Pygame
        frame = clip.get_frame(t)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Display the frame
        screen.blit(frame_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    clip.close()
    pygame.quit()

