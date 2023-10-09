import pygame
import sys
import tiles

#screen config constants
WIN_WIDTH = 1920 #HD 16:9
WIN_HEIGHT = 1080 #HD 16:9
#colour config constants
WHITE = (255,255,255)
#other graphical constants
FPS = 60

#class to store the whole application
class Application:
    #initialise the application
    def __init__(self):
        pygame.init() #activate pygame
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) #create the screen
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
        self.tiles = pygame.sprite.LayeredUpdates()
    
    #update the application
    def update(self):
        self.all_sprites.update()

    #draw the application
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
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

def main():
    a = Application()
    a.intro_screen()
    a.new()
    while a.running:
        a.main()
        a.end_application()
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()