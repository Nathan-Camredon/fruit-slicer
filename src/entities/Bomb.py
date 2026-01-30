from .Fruit import Fruit
import pygame


class Bomb(Fruit):
    def __init__(self, letter):
        super().__init__(letter, type="Bomb")

