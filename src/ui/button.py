import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, 
                 base_color=(255, 255, 255), 
                 hover_color=(255, 235, 245), 
                 text_color=(230, 103, 177)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, screen, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos)
        bg = self.hover_color if is_hovered else self.base_color
        pygame.draw.rect(screen, bg, self.rect, border_radius=18)
        pygame.draw.rect(screen, self.text_color, self.rect, width=3, border_radius=18)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_text(self, new_text):
        self.text = new_text

class ImageButton:
    """Class for images with a circular border hover effect (like your flags)"""
    def __init__(self, x, y, image, hover_color=(255, 192, 203), base_color=(255, 255, 255)):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hover_color = hover_color
        self.base_color = base_color

    def draw(self, screen, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Draw the specific ellipse border logic you had
        inflate_amount = 16 if is_hovered else 10
        color = self.hover_color if is_hovered else self.base_color
        
        # Draw border
        pygame.draw.ellipse(screen, color, self.rect.inflate(inflate_amount, inflate_amount), width=3)
        # Draw flag
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)