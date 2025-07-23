from pygame import Surface, Rect
import pygame

class TextureData:
    def __init__(self, texture: Surface):
        self.texture = texture
        self.rect: Rect = texture.get_rect()
    
    @classmethod
    def load(cls, filepath: str):
        return cls(pygame.image.load(filepath))