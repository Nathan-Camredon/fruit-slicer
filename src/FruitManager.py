import random
import pygame
from .entities.Fruit import Fruit
from .entities.Bomb import Bomb
from .entities.Ice import Ice



class FruitManager:
    def __init__(self):
        self.fruits = []
        self.lives = 3
        self.unfreeze = 0
        self.score = 0
    def spawn_fruit(self):
        """Adds a new fruit to the game."""
        #Choose Type
        x = random.random()
        if x < 0.06:
            fruit_type = "Bomb"
        elif x < 0.1:
            fruit_type = "Ice"
        else:
            fruit_type = "Classic"

        #Determine Forbidden Letters
        forbidden = []
        if fruit_type in ["Bomb", "Ice"]:
            # Bombs/Ice unique key
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
        if pygame.time.get_ticks() > self.unfreeze:
            for fruit in self.fruits:
                fruit.update()
        
        # Count fruits that fell (missed)
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

    def press_key(self, key, score = 0):
        """Handles key presses."""
        hit_fruits = [f for f in self.fruits if f.letter == key]
        for f in hit_fruits:
            if f.type == "Bomb":
                self.lives -= 3 #Game over
                self.fruits = [fruit for fruit in self.fruits if fruit.letter != key]
                return -50
            elif f.type ==  "Ice":
                self.unfreeze = pygame.time.get_ticks() + 1500
                self.fruits = [fruit for fruit in self.fruits if fruit.letter != key]
            elif hit_fruits:
                if len(hit_fruits) >= 2:
                    self.score += 100
                    self.fruits = [fruit for fruit in self.fruits if fruit.letter != key]
                    return 100
                self.score += 20 #Editable
                self.fruits = [fruit for fruit in self.fruits if fruit.letter != key]
                return 20
        return 0