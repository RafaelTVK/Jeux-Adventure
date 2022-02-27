import pygame
from AppConfig import *

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, name) -> None:
        super().__init__()
        self.image = pygame.image.load(f"sprites/{name}.png")
        self.animationIndex = 0
        self.images = {
            "down": self.get_images(0),
            "left": self.get_images(32),
            "right": self.get_images(64),
            "up": self.get_images(96)
        }
        self.speed = SPEED
        self.clock = 0
    def change_animation(self,name):

        self.image = self.images[name][self.animationIndex]
        self.image.set_colorkey(NOIR)
        self.clock += self.speed * 8
        if self.clock >= 100:
        
            self.animationIndex+=1

            if self.animationIndex >= len(self.images[name]):
                self.animationIndex=0
            self.clock = 0
            
    def get_images(self,y):
        images = []
        for i in range(0,3):
            x = i*TAILLE_ENTITY
            image = self.get_image(x,y)
            images.append(image)
        return images
            
    def get_image(self, x, y):
        image = pygame.Surface([TAILLE_ENTITY, TAILLE_ENTITY])
        image.blit(self.image, (0, 0), (x, y, TAILLE_ENTITY, TAILLE_ENTITY))
        return image
        