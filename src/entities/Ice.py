from .Fruit import Fruit
import pygame
import random

class Ice(Fruit):
    def __init__(self, letter):
        super().__init__(letter, type="Ice")

    def draw(self, screen):
        police = pygame.font.SysFont(None, 50)
        # Blue for Ice
        lettre_image = police.render(self.letter, True, (0, 0, 255)) 
        zone_lettre = lettre_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(lettre_image, zone_lettre)