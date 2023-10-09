import pygame
import config

#represents a tile in the world
class Tile(pygame.sprite.Sprite):
    #create the tile object
    def __init__(self,application,x,y,type):
        self.application = application
        self._layer = config.TILE_LAYER
        self.groups = self.application.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.type = type
        self.init_position(x,y)
        self.init_image()
        self.init_rect()

    #define the position of the tile
    def init_position(self,x,y):
        self.x = x*config.TILESIZE
        self.y = y*config.TILESIZE
        self.width = config.TILESIZE
        self.height = config.TILESIZE

    #create the image of the tile (based on whether it is ocean or land)
    def init_image(self):
        self.image = pygame.Surface([self.width,self.height])
        if(self.type=='Land'):
            self.image.fill(config.GREEN)
        elif(self.type=='Ocean'):
            self.image.fill(config.BLUE)
        else:
            print("WARNING : TILE TYPE ",self.type, " NOT A VALID TYPE")
    
    #create the rectangle of the tile (hitbox)
    def init_rect(self):
        self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y