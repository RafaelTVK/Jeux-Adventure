import pygame
from animation import AnimateSprite

class Player(AnimateSprite):
    def __init__(self,x,y) -> None:
        super().__init__("player",(32,32))
        self.position = [x,y]
        self.speed = 3
        self.feet = pygame.Rect(0,0,self.rect.width * 0.5,12)
        self.oldPosition = self.position.copy()
        
    def save_location(self):
        self.oldPosition = self.position.copy()
        
    def change_animation(self,name):
        self.animate(name)
        pass    
    def move_right(self): self.position[0] += self.speed
    def move_left(self):  self.position[0] -= self.speed
    
    def move_up(self): self.position[1] -= self.speed
    def move_down(self): self.position[1] += self.speed
    
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom 
        pass
    def move_back(self):
        self.position = self.oldPosition
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom 
        pass
    # def get_image(self,x,y):
    #     image = pygame.Surface([32,32])
    #     image.blit(self.sprite_sheet, (0,0), (x,y,32,32))
    #     return image
        