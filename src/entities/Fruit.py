import random
import pygame


class Fruit:
    def __init__(self, letter, type="Classic"):
        """Initializes a fruit with a random trajectory."""
        self.letter = letter
        self.type = type
        self.t = 0.0
        if self.type == "Classic":
            images = ["apple.png", "banana.png", "orange.png", "watermelon.png"]
        if self.type == "Bomb":
            images = ["bomb.png"]
        if self.type == "Ice":
            images = ["ice.png"]
            
        choice = random.choice(images)
        link = f"assets/elements/{choice}"

        fruit = pygame.image.load(link).convert_alpha()
        self.fruit = pygame.transform.scale(fruit, (100, 100))
        # Random X position
        start_x = random.randint(100, 1180)
        
        # Calculate X direction (to throw towards the center)
        if start_x < 640:
            vx = random.uniform(100, 180)
        else:
            vx = random.uniform(-180, -100)
            
        self.params = {
            "start_x": start_x,
            "start_y": 800,
            "vx": vx,
            "vy": random.uniform(-950, -1150)
        }
        self.y = self.params["start_y"]
        self.x = self.params["start_x"] # Init x to avoid crash if drawn before update        

    def update(self):
        """Updates the fruit's position based on physics."""
        self.t += 1/60  
        gravity = 900
        # X Movement: x0 + vx * t
        self.x = self.params["start_x"] + (self.params["vx"] * self.t)
        
        # Y Movement: y0 + vy * t + 0.5 * g * t^2  low of galilée 
        self.y = self.params["start_y"] + (self.params["vy"] * self.t) + (0.5 * gravity * (self.t * self.t))

    def draw(self, screen):
        """Draws the fruit on the screen."""
        rect_fruit = self.fruit.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.fruit, rect_fruit)
        police = pygame.font.SysFont(None, 50)
        lettre_image = police.render(self.letter , True, (255, 255, 255))
        
        zone_lettre = lettre_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(lettre_image, zone_lettre)
