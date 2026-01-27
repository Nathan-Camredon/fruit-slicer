import random
import pygame

class Fruit:
    def __init__(self, letter, type="classic"):
        """Initializes a fruit with a random trajectory."""
        self.letter = letter
        self.type = type
        self.t = 0.0
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
        

    def update(self):
        """Updates the fruit's position based on physics."""
        self.t += 1/60  
        gravity = 900
        # X Movement: x0 + vx * t
        self.x = self.params["start_x"] + (self.params["vx"] * self.t)
        
        # Y Movement: y0 + vy * t + 0.5 * g * t^2
        self.y = self.params["start_y"] + (self.params["vy"] * self.t) + (0.5 * gravity * (self.t * self.t))

    def draw(self, screen):
        """Draws the fruit on the screen."""
        
        police = pygame.font.SysFont(None, 50)
        lettre_image = police.render(self.letter , True, (255, 255, 255))
        zone_lettre = lettre_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(lettre_image, zone_lettre)

class Bomb(Fruit):
    def __init__(self, letter):
        super().__init__(letter, type="Bomb")

    def draw(self, screen):
        police = pygame.font.SysFont(None, 50)
        # Red for Bomb
        lettre_image = police.render(self.letter, True, (255, 0, 0)) 
        zone_lettre = lettre_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(lettre_image, zone_lettre)

class Ice(Fruit):
    def __init__(self, letter):
        super().__init__(letter, type="Ice")

    def draw(self, screen):
        police = pygame.font.SysFont(None, 50)
        # Blue for Ice
        lettre_image = police.render(self.letter, True, (0, 0, 255)) 
        zone_lettre = lettre_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(lettre_image, zone_lettre)

class FruitGame:
    def __init__(self):
        self.fruits = []
        self.lives = 3

    def spawn_fruit(self):
        """Adds a new fruit to the game."""
        #Choose Type
        x = random.random()
        if x < 0.03:
            fruit_type = "Bomb"
        elif x < 0.06:
            fruit_type = "Ice"
        else:
            fruit_type = "Classic"

        #Determine Forbidden Letters
        forbidden = []
        if fruit_type in ["Bomb", "Ice"]:
            # Bombs/Ice must be unique vs EVERYTHING
            forbidden = [f.letter for f in self.fruits]
        else:
            # Classic fruits only need to avoid Bombs/Ice
            forbidden = [f.letter for f in self.fruits if f.type in ["Bomb", "Ice"]]

        # Choose a Safe Letter
        possible_letters = "AZERUIOP"
        available = [L for L in possible_letters if L not in forbidden]
        
        if not available:
            return # Safety: No letters left, cancel spawn
            
        la_lettre = random.choice(available)

        # 4. Create Object
        if fruit_type == "Bomb":
            self.fruits.append(Bomb(la_lettre))
        elif fruit_type == "Ice":
            self.fruits.append(Ice(la_lettre))
        else:
            self.fruits.append(Fruit(la_lettre, type="Classic"))
        

    def update(self):
        """Updates all active fruits."""
        for fruit in self.fruits:
            fruit.update()
        
        # Count fruits that fell (missed)
        # On ne perd des vies que si c'est un Fruit Classique (pas une Bombe ou un Glaçon)
        missed_fruits = [f for f in self.fruits if f.y > 1000 and f.type == "Classic"]
        self.lives -= len(missed_fruits)
        
        # Keep only on-screen fruits
        self.fruits = [f for f in self.fruits if f.y <= 1000]

    def draw(self, screen):
        """Draws all active fruits and lives."""
        for fruit in self.fruits:
            fruit.draw(screen)
        
        # Draw lives
        font = pygame.font.SysFont(None, 36)
        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))

    def press_key(self, key):
        """Handles key presses."""
        self.fruits = [fruit for fruit in self.fruits 
                      if fruit.letter != key]