import pygame

from Inventory import Inventory
from dialog import DialogBox

from map import *
from quete import QueteManager
from Player import Player

from AppConfig import *

class Game:

    def __init__(self):
        # Démarrage
        self.running = True
        self.map = MAP_DEBUT

        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode(ECRAN)
        pygame.display.set_caption(TITRE)

        # Générer le joeur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.quete_manager = QueteManager()
        self.dialogBox = DialogBox()

        # generer la barre d'inventaire
        self.inventory = Inventory()


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False
        elif pressed[pygame.K_UP] or pressed[pygame.K_z]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.player.move_down()
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.player.move_right()
        elif pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.player.move_left()

    def checkQuete(self ,map,npc,qutename)-> bool:
        if not self.quete_manager.getStateQuete(npc, qutename):
            point = self.map_manager.maps[map].tmx_data.get_object_by_name(self.quete_manager.getPoint(npc, qutename))
            rect = pygame.Rect(point.x, point.y, point.width, point.height)

            if self.player.feet.colliderect(rect):
                self.quete_manager.changeStateQuete(npc, qutename)
                self.quete_manager.save()
                return True
            return False

    def checkQuetes(self):
        from dialog import DialogBox
        d = DialogBox()
        # check toutes les quetes
        if self.checkQuete("world", "robin", "queteR1"):
            pass
        if self.checkQuete("donjon1", "paul", "queteP1"):

            pass
        if self.checkQuete("world", "boss", "queteB1"):
            pass
        pass

    def update(self):
        self.map_manager.update()
        self.checkQuetes()

    def run(self):

        clock = pygame.time.Clock()

        # Clock
        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialogBox.render(self.screen)
            self.inventory.render(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialogBox)

            clock.tick(FPS)

        pygame.quit()
