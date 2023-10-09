import pygame
import sys
import config
import tiles
import water
import numpy as np



#class to store the whole application
class Application:
    #initialise the application
    def __init__(self):
        pygame.init() #activate pygame
        self.screen = pygame.display.set_mode((config.WIN_WIDTH,config.WIN_HEIGHT)) #create the screen
        self.clock = pygame.time.Clock()
        self.running = True #the application is running
    
    #see which events have happened
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #quit the game
                self.playing = False
                self.running = False
        
    #a new application instance starts
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.tiles = pygame.sprite.Group()
    
    #update the application
    def update(self):
        self.all_sprites.update()

    #draw the application
    def draw(self):
        self.screen.fill(config.WHITE)
        self.all_sprites.draw(self.screen)
        self.clock.tick(config.FPS)
        pygame.display.update()

    #main loop
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
    
    def end_application(self):
        pass

    def intro_screen(self):
        pass

    #create the main map
    def create_map(self):
        map = water.water_landscape
        self.create_tiles_from_elevation(map)
        


    def create_tiles_from_elevation(self,map):
        for x,row in enumerate(map):
            for y,cell in enumerate(row):
                if cell>0:
                    type = 'Land'
                else:
                    type = 'Ocean'
                tile = tiles.Tile(self,x,y,type)
                self.tiles.add(tile)

def main():
    a = Application()
    a.intro_screen()
    a.new()
    a.create_map()
    while a.running:
        a.main()
        a.end_application()
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()