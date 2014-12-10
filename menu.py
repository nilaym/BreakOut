import pygame, sys, os
from pygame.locals import *
from text import Text

global SCREEN_SIZE
SCREEN_SIZE = (640,640)
FPS = 60

class Image(pygame.sprite.DirtySprite):
    def __init__(self, image, pos):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
    

def mainScreen(screen):
    background = pygame.image.load(os.path.join("images", "menu_background.jpg")).convert_alpha()

    breakOutText = Text("BreakOut Clone v1!!!",(160,90), font_family = "Comic Sans MS")
    playText = Text("Play Game", (245,260))
    howToPlayText = Text("How To Play", (240,310))
    aboutText = Text("About", (267,360))
    quitText = Text("Quit", (277,403))
    soundText = Text("Sound FX: On", (495,15), font_size = 25)
    main_options = [playText, howToPlayText, aboutText, quitText, soundText]
    main_images = [breakOutText]

    createdByText1 = Text("This is a very simple BreakOut or Arkanoid clone", (15,75))
    createdByText2 = Text("created by me in a few days of boredom over", (30,110))
    createdByText3 = Text("my summer", (30, 140))
    backText = Text("Back", (SCREEN_SIZE[0]-100, SCREEN_SIZE[1]-40))
    about_options = [backText]
    about_images = [createdByText1, createdByText2, createdByText3]

    howToPlay1_img = pygame.image.load(os.path.join("images", "howToPlay1.png")).convert_alpha()
    howToPlay2_img = pygame.image.load(os.path.join("images", "howToPlay2.png")).convert_alpha()
    howToPlay1 = Image(howToPlay1_img, (100,100))
    howToPlay2 = Image(howToPlay2_img, (400,100))
    theGoalText = Text("The Goal: Destroy all the bricks", (0, 230), font_size = 25)
    howToDestroyText = Text("How: Bounce the ball off the bricks and rebound it off your paddle", (0, 280), font_size = 25)
    controlsText = Text("Controls: Move mouse to move paddle.", (0, 330), font_size = 25)
    controls2Text = Text("Press the left mouse button to launch ball", (90, 365), font_size = 25)
    howToPlay_options = [backText]
    howToPlay_images = [howToPlay1, howToPlay2, theGoalText, howToDestroyText, controlsText, controls2Text]

    current_page = 'main'
    current_options = pygame.sprite.RenderUpdates()
    current_images = pygame.sprite.RenderUpdates()
    current_options.add(main_options)
    current_images.add(main_images)

    music = pygame.mixer.music.load(os.path.join("sounds", "menu.wav"))
    pygame.mixer.music.play(-1)

    #Blit background image once.
    screen.blit(background, (0,0))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if current_page == 'main':
                        if playText.rect.collidepoint(event.pos):
                            return

                        elif howToPlayText.rect.collidepoint(event.pos):
                            current_options.empty()
                            current_images.empty()
                            current_options.add(howToPlay_options)
                            current_images.add(howToPlay_images)
                            current_page = 'howToPlay'
                            
                          
                        elif aboutText.rect.collidepoint(event.pos):
                            current_options.empty()
                            current_images.empty()
                            current_options.add(about_options)
                            current_images.add(about_images)
                            current_page = 'about'

                        elif quitText.rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

                        elif soundText.rect.collidepoint(event.pos):
                            if soundText.message == "Sound FX: On":
                                soundText.changeMessage("Sound FX: Off")
                                pygame.mixer.music.pause()
                            else:
                                soundText.changeMessage("Sound FX: On")
                                pygame.mixer.music.unpause()
                                

                    elif current_page == 'howToPlay':
                        if backText.rect.collidepoint(event.pos):
                            current_options.empty()
                            current_images.empty()
                            current_options.add(main_options)
                            current_images.add(main_images)
                            current_page = 'main'

                    elif current_page == 'about':
                        if backText.rect.collidepoint(event.pos):
                            current_options.empty()
                            current_images.empty()
                            current_options.add(main_options)
                            current_images.add(main_images)
                            current_page = 'main'


        for text in current_options:
            text.update() #Highlight text if mouse if over text

        current_options.clear(screen, background)
        current_images.clear(screen, background)
        dirty_rects = current_options.draw(screen)
        dirty_rects.extend(current_images.draw(screen))
        
        pygame.display.update(dirty_rects)

if __name__ == '__main__':
    screen = pygame.display.set_mode((640,640))
    pygame.init()
    mainScreen(screen)

