from .Fruit import Fruit
import pygame
import random

class Ice(Fruit):
    def __init__(self, letter):
        super().__init__(letter, type="Ice")

