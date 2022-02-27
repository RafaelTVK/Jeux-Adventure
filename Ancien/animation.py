import pygame

# Classe qui va s'occuper des animations

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name, size=(200,200)) -> None:
        super().__init__()
        self.size = size
        self.image = pygame.image.load(f"assets/{name}/{name}down1.png")
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.current_image = 0
        self.images = animations
        self.animation = False

    # methode pour demarrer l animation
    def start_animation(self):
        self.animation = True

    # methode pour animer le sprite
    def animate(self,direction,loop =False):
        if self.animation:
            self.current_image+=1
            # verifier si l animation est a la fin
            if self.current_image>= len(self.images[f"player{direction}"]):
                # rermise a zero de l animation
                self.current_image = 0
                
                if loop is False:
                    self.animation = False

            # mdifier l image precedente par la suivante
            self.image = self.images[f"player{direction}"][self.current_image]
            self.image = pygame.transform.scale(self.image, self.size)
            
        pass

# definir une fonction pour charger les imagesd'un sprite
def loadAnimationImages(sprite_name:str,direction:str):
    # charger les 3 images de ce sprite
    images = []
    # recup du chemin pour ce sprite
    path = f"assets/{sprite_name.title()}/{sprite_name}{direction}"
    # boucler sur chaque image dans ce dossier
    for num in range(1,4):
        image_path = path + str(num) + ".png"
        print(image_path)
        images.append(pygame.image.load(image_path))

    return images

# definir un dictionnaire qui va contenir les images chargées de chaque sprite
# mummy -> [mummy1.png, mummy2.png, ...]

animations = {
    "playerup": loadAnimationImages("player","up"),
    "playerdown":loadAnimationImages("player","down"),
    "playerleft": loadAnimationImages("player","left"),
    "playerright": loadAnimationImages("player","right")
}