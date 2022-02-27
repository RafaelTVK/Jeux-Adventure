import pygame
import pytmx
import pyscroll
from Player import Player

class Game:
    def __init__(self) -> None:
       # creer la fenetre
        self.screen = pygame.display.set_mode((960,800))
        pygame.display.set_caption("Pygamon - Adventure")
    # charger la carte
        tmx_data = pytmx.load_pygame("assets/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 2
        # generer un joueur 
        player_position = tmx_data.get_object_by_name("player")
        self.player  = Player(player_position.x, player_position.y)
        
        # definir  une liste qui va stocker les rectangles de collision
        self.walls = []
        
        for obj in tmx_data.objects:
            if obj.type=="collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # dessiner le groupe de calques
        self.group =pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=6)
        self.group.add(self.player)
        # definir le rect de collision pour entrer dans la maison 
        enter_house1  = tmx_data.get_object_by_name("enter_house1")
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)
        tmx_data = pytmx.load_pygame(f"assets/house{1}.tmx")
        self.exit_house1 = tmx_data.get_object_by_name("exit_house1")
        self.exit_house1_rect = pygame.Rect(self.exit_house1.x, self.exit_house1.y, self.exit_house1.width, self.exit_house1.height)
        spawnPoint = tmx_data.get_object_by_name(f"spawn_point1")
        self.spawnPoint_rect = pygame.Rect(spawnPoint.x, spawnPoint.y, spawnPoint.width, spawnPoint.height)
        
        
    def switch_house(self,numHouse):
        # charger la carte
        tmx_data = pytmx.load_pygame(f"assets/house{numHouse}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 2
    
        # definir  une liste qui va stocker les rectangles de collision
        self.walls = []
        
        for obj in tmx_data.objects:
            if obj.type=="collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # dessiner le groupe de calques
        self.group =pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=4)
        self.group.add(self.player)
        #point de spawn dans la maison
        spawnPoint = tmx_data.get_object_by_name(f"spawn_point1")
        self.spawnPoint_rect = pygame.Rect(spawnPoint.x, spawnPoint.y, spawnPoint.width, spawnPoint.height)
        self.player.position[0] = spawnPoint.x
        self.player.position[1] = spawnPoint.y - 20
        
        self.exit_house1 = tmx_data.get_object_by_name("exit_house1")
        self.exit_house1_rect = pygame.Rect(self.exit_house1.x, self.exit_house1.y, self.exit_house1.width, self.exit_house1.height)
    
    def exitHouse(self,numHouse):
        tmx_data = pytmx.load_pygame(f"assets/house{numHouse}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 2
        #point de spawn hors de la maison
        tmx_data =  pytmx.load_pygame(f"assets/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 2
        self.walls = []
        
        for obj in tmx_data.objects:
            if obj.type=="collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # dessiner le groupe de calques
        self.group =pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=4)
        self.group.add(self.player)
        
        spawnPoint = tmx_data.get_object_by_name("enter_house_exit1")
        self.player.position[0] = spawnPoint.x
        self.player.position[1] = spawnPoint.y + 20
        
        
        pass   

    def update(self):
        self.group.update()
        
        # verifier l entree dans la maison
        if self.player.feet.colliderect(self.enter_house1_rect):
            self.switch_house(1)
        if self.player.feet.colliderect(self.exit_house1_rect):
            self.exitHouse(1)
            
        
        # verifiication des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls)> -1:
                sprite.move_back()
        pass
    def switch_world(self):
            # charger la carte
        tmx_data = pytmx.load_pygame("assets/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 2
        
        # definir  une liste qui va stocker les rectangles de collision
        self.walls = []
        
        for obj in tmx_data.objects:
            if obj.type=="collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=5)
        self.group.add(self.player)
        # definir le rect de collision pour entrer dans la maison 
        enter_house1  = tmx_data.get_object_by_name("enter_house")
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)


        pass
    def handle_input(self):
        pressed = pygame.key.get_pressed()  # recupere le touche enclenchées
        if pressed[pygame.K_z] or pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.start_animation()
            self.player.change_animation("up")
            
        elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.start_animation()
            self.player.change_animation("down")
        elif pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.start_animation()
            self.player.change_animation("left")
            self.player.move_left()
        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.start_animation()
            self.player.change_animation("right")
    def run(self):
        clock = pygame.time.Clock()
        FPS = 120
        # boucle du jeu
        running = True

        while running:
            
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect) # Centrer la camera sur le rectangle du personnage
            self.group.draw(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False      
            pass
            clock.tick(FPS)
        
        pygame.quit()