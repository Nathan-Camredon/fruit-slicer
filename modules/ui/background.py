import pygame
from moviepy import VideoFileClip
from typing import Optional, Tuple


class BackgroundVideo:
    """
    Encapsulate a VideoFileClip and provide a persistent timer so
    the video does not restart when switching menus.
    """

    def __init__(self, filepath: str, size: Tuple[int, int] = (1280, 720)):
        self.filepath = filepath
        self.size = size
        self.clip: Optional[VideoFileClip] = None
        self.duration: float = 1.0
        self.start_ticks = 0
        self._load()

    def _load(self):
        # Must be called after pygame.init()
        self.clip = VideoFileClip(self.filepath).resized(self.size)
        self.duration = self.clip.duration
        self.start_ticks = pygame.time.get_ticks()

    def get_frame_surface(self) -> pygame.Surface:
        """Return a pygame.Surface for the current frame based on a persistent clock."""
        if self.clip is None:
            self._load()
        elapsed_sec = (pygame.time.get_ticks() - self.start_ticks) / 1000.0
        t = elapsed_sec % self.duration
        frame = self.clip.get_frame(t)
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        return surface

    def reset_offset(self, offset_seconds: float = 0.0):
        """Shift the internal clock so the video appears at a different offset."""
        self.start_ticks = pygame.time.get_ticks() - int(offset_seconds * 1000)

    def close(self):
        if self.clip is not None:
            try:
                self.clip.close()
            except Exception:
                pass
            self.clip = None

