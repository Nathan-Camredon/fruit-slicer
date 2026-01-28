from .Fruit import Fruit
import pygame


class Bomb(Fruit):
    def __init__(self, letter):
        super().__init__(letter, type="Bomb")

    def draw(self, screen):
        police = pygame.font.SysFont(None, 50)
        # Red for Bomb
        lettre_image = police.render(self.letter, True, (255, 0, 0)) 
        zone_lettre = lettre_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(lettre_image, zone_lettre)