import pygame

class InventorySlot:
    def __init__(self, name, pos):
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def render(self,screen):
        screen.blit(self.image, self.rect)
