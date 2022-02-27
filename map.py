import pygame, pyscroll, pytmx
from dataclasses import dataclass
from Player import NPC
from quete import QueteManager
from AppConfig import *

@dataclass
class Portal:
    from_world :str
    originPoint:str
    targetWorld:str
    teleportPoint:str
    

@dataclass
class Map:
    nom:str
    walls:list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals:list[Portal]
    npcs: list[NPC]
    pass

class MapManager:
    def __init__(self,screen,player) -> None:
        self.maps = dict() # house -> Map("house",walls,group)
        self.current_map = MAP_DEBUT
        self.screen = screen
        self.player = player
        self.npcs = []
        
        self.register_map("world",portals=[
            Portal(from_world="world", originPoint="enter_house1",targetWorld="house1",teleportPoint="spawn_point1"),
            Portal(from_world="world", originPoint="enter_house2",targetWorld="house2",teleportPoint="spawn_point2"),
            Portal(from_world="world", originPoint="enter_donjon1",targetWorld="donjon1",teleportPoint="spawn_donjon1"),
            Portal(from_world="world", originPoint="enter_house3",targetWorld="house3",teleportPoint="spawn_point3")

        ],npcs = [NPC("paul",nb_points=4,dialog=self.loadTextsNpc("paul")),NPC("robin",nb_points=2,dialog=self.loadTextsNpc("robin"))])
        self.register_map("house1",portals=[
            Portal(from_world="house1",originPoint="exit_house1",targetWorld="world",teleportPoint="enter_house_exit1")
        ])
        
        self.register_map("house2",portals=[
           Portal(from_world="house2",originPoint="exit_house2",targetWorld="world",teleportPoint="enter_house_exit2")
        ])
        self.register_map("house3",portals=[
           Portal(from_world="house3",originPoint="exit_house3",targetWorld="world",teleportPoint="enter_house_exit3")
        ])
        self.register_map("house5", portals=[
           Portal(from_world="house5",originPoint="exit_house5",targetWorld="magic",teleportPoint="enter_house_exit5")
        ])
        self.register_map("house6", portals=[
            Portal(from_world="house6", originPoint="exit_house6", targetWorld="magic",
                   teleportPoint="enter_house_exit6")
        ])
        self.register_map("donjon1",portals=[
            Portal(from_world="donjon1",originPoint="exit_donjon1",targetWorld="world",teleportPoint="enter_donjon_exit1"),
            Portal(from_world="donjon1",originPoint="enter_magic",targetWorld="magic",teleportPoint="spawn_magic")
        ],npcs=[NPC("boss",nb_points=2,dialog=self.loadTextsNpc("boss"))])

        self.register_map("magic", portals=[
            Portal(from_world="magic",originPoint="exit_magic",targetWorld="donjon1",teleportPoint="enter_exit_magic"),
            Portal(from_world="magic", originPoint="enter_house5", targetWorld="house5", teleportPoint="spawn_point5"),
            Portal(from_world="magic", originPoint="enter_house5", targetWorld="house6", teleportPoint="spawn_point6")
        ])

        self.teleport_player("player")
        self.teleport_npcs()
    def loadTextsNpc(self,npc:str):
        q = QueteManager()
        return q.getText(npc)

    def enterPortail(self):
        #portail
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.originPoint)
                rect = pygame.Rect(point.x,point.y,point.width,point.height)
                
                if self.player.feet.colliderect(rect):
                    copyPortal = portal
                    self.current_map = portal.targetWorld
                    self.teleport_player(copyPortal.teleportPoint)

    def check_npc_collisions(self, dialogBox):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialogBox.execute(sprite.dialog)

    def check_collisions(self):
        self.enterPortail()
        for sprite in self.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1
            
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
        pass

    def teleport_player(self,name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[],npcs=[]):
        # Charger la carte clasique
        if "house" in name:
            tmx_data = pytmx.load_pygame(f"assets/house/{name}.tmx")
        else:
            tmx_data = pytmx.load_pygame(f"assets/{name}/{name}.tmx")


        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = ZOOM
        # Les collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)
        
        # recuperer les npcs pour les ajouter au grp
        for npc in npcs:
            group.add(npc)
        
        # creer un obj map
        self.maps[name] = Map(name,walls, group,tmx_data, portals,npcs)
        
    def get_map(self): 
        return self.maps[self.current_map]
    
    def get_group(self): 
        return self.get_map().group
    
    def get_walls(self): 
        return self.get_map().walls
    
    def get_object(self,name): 
        return self.get_map().tmx_data.get_object_by_name(name)
    
    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
            
            for npc in npcs:
                if type(npc) is NPC:
                    npc.load_points(map_data.tmx_data)
                    npc.teleport_Spawn()

        pass
    
    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)


    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            if type(npc) is NPC:
                npc.move()
