import pygame
from AppConfig import *
from InventorySlot import  InventorySlot

class Inventory:
    def __init__(self):
        self.slots = []

        self.image = pygame.image.load(IMAGE_INVENTORY)
        self.image = pygame.transform.scale(self.image, TAILLE_INVENTORY)
        self.rect = self.image.get_rect()
        self.rect.topleft = POS_INVENTORY

    def ajouteObjet(self,name, pos):
        self.slots.append(InventorySlot(name, pos)) # append un objet a  l inventaire

    def render(self, screen):
        screen.blit(self.image, self.rect)

        for slot in self.slots:
            slot.render(screen)

