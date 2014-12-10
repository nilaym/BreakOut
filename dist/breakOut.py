import pygame, sys, os, math, random
from pygame.locals import *
from text import Text
from menu import mainScreen

global SCREEN_SIZE, FPS, BLOCK_START, BLOCK_WIDTH, BLOCK_HEIGHT, PLAYER_START, CORNER_WIDTH
SCREEN_SIZE = (640,640)
FPS = 60
BLOCK_START = (70,110)
BLOCK_WIDTH = 50 #Should match up with width of block image!
BLOCK_HEIGHT = 20 #Should match up with height of block image!
PLAYER_START = (290,620)
CORNER_WIDTH = 10

#Power up vars
global POWERUP_BALL, POWERUP_LIGHTNING, POWERUP_PADDLE, POWERUP_LASER, POWERUP_PROB, POWERUP_EXTRA_SPEED
#The different powerups marked by numbers signifying the index of the images list within PowerUp
POWERUP_BALL = 0
POWERUP_LIGHTNING = 1
POWERUP_PADDLE = 2
POWERUP_LASER = 3
#Variables related to the powerups, like probability of powerup spawn, or effects of certain powerups (e.g. extra speed)
POWERUP_PROB = [False, True, False, False] #Simulate probability of getting a powerup.
POWERUP_EXTRA_SPEED = 2 #Extra speed the lightning powerup gives to the balls


class Block(pygame.sprite.DirtySprite):
    def __init__(self, pos, level=1):
        pygame.sprite.DirtySprite.__init__(self)
        self.level = level #level of block 1-4, 5 is a fire block, 6 is an unbreakable block. 0 is dead block
        self.image = pygame.image.load(os.path.join("images", "block%d.png" % self.level)).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

    def levelDown(self):
        self.level -= 1
        self.image = pygame.image.load(os.path.join("images", "block%d.png" % self.level)).convert_alpha()
        self.dirty = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("images", "paddle.gif")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.lives = 3
        self.score = 0
        self.speed = 3

        self.big = False #Has the player poweruped in size?
        self.timeAtPowerUp = 0 #When did the player power up.
        self.powerUpTime = 10 #How many seconds should the powerup last?

    def growBig(self):
        self.image = pygame.transform.scale2x(self.image)
        center = self.rect.center
        self.rect = self.image.get_rect(center = center)
        self.big = True
        self.timeAtPowerUp = pygame.time.get_ticks() / 1000

    def update(self):
        mousepos = pygame.mouse.get_pos()
        self.rect.left = mousepos[0]

        if self.rect.right >= SCREEN_SIZE[0]:
            self.rect.right = SCREEN_SIZE[0]

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.big == True:
            time = pygame.time.get_ticks() / 1000
            if time > self.timeAtPowerUp + self.powerUpTime: #check if powerup period is over
                self.big = False
                self.image = pygame.image.load(os.path.join("images", "paddle.gif")).convert_alpha()
                center = self.rect.center
                self.rect = self.image.get_rect(center = center)


class Ball(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load(os.path.join("images", "ball.gif")).convert_alpha()
        self.rect = self.image.get_rect()

        self.direction = 0
        self.speed = 5
        self.max_speed = 9

        self.clamped = False
        self.dirty = 2


    def clamp(self, anchor):
        self.rect.bottom = anchor.rect.top
        self.rect.centerx = anchor.rect.centerx
        self.clamped = True

    def launch(self):
        spin = random.choice([30, -30])
        self.direction = 90+ spin
        self.clamped = False

    def get_direction(self):
        radians = math.radians(self.direction)
        dx,dy = math.cos(radians)*self.speed, -math.sin(radians)*self.speed

        return (dx,dy)

    def update(self):
        radians = math.radians(self.direction)
        dx,dy = math.cos(radians)*self.speed, -math.sin(radians)*self.speed #Account for pygame cartesian coordinates, where -y means up rather than down

        self.rect.move_ip(dx,dy)

    def checkWallCollisions(self):
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 180 - self.direction

        elif self.rect.right >= SCREEN_SIZE[0]:
            self.rect.right = SCREEN_SIZE[0]
            self.direction = 180 - self.direction

        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction = -self.direction

    def bounce(self, diff=0):
        if diff == 0:
            self.direction = -self.direction

        elif diff == -1:
            #Reverse direction
            self.direction -= 180

        elif diff == 1:
            #bounce off vertical surface
            self.direction = 180 - self.direction

        else:
            self.direction += diff

    


class PowerUp(pygame.sprite.DirtySprite):
    def __init__(self, powerup_type):
        pygame.sprite.DirtySprite.__init__(self)
        self.type = powerup_type
        self.images = [pygame.image.load(os.path.join("images", "powerup_ball.png")).convert_alpha(),
                       pygame.image.load(os.path.join("images", "powerup_lightning.png")).convert_alpha(),
                       pygame.image.load(os.path.join("images","powerup_paddle.png")).convert_alpha(),
                       pygame.image.load(os.path.join("images", "powerup_laser.png")).convert_alpha()]
                       

        self.image = self.images[self.type]
        self.rect = self.image.get_rect()

        self.fall_speed = 3

    def update(self):
        self.rect.move_ip(0, self.fall_speed)


class Laser(pygame.sprite.DirtySprite):
    def __init__(self, start_pos):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load(os.path.join("images", "laser.gif")).convert_alpha()
        self.rect = self.image.get_rect(midbottom = start_pos)
        self.speed = 3
        self.dirty = 2

    def update(self):
        self.rect.move_ip(0,-self.speed)

class Blast(pygame.sprite.DirtySprite):
    def __init__(self, center):
        pygame.sprite.DirtySprite.__init__(self)
        self.image1 = pygame.image.load(os.path.join("images", "blast1.gif"))
        self.image2 = pygame.image.load(os.path.join("images", "blast2.gif"))
        self.image3 = pygame.image.load(os.path.join("images", "blast3.gif"))
        self.images = [self.image1, self.image2, self.image3]

        self.frame = 0
        self.image = self.images[int(self.frame)]
        self.rect = self.image.get_rect(center = center)

    def update(self):
        self.frame += .25
        if self.frame > 2:
            self.kill() #blast done

        self.image = self.images[int(self.frame)]
        oldcenter = self.rect.center
        self.rect = self.image.get_rect(center = oldcenter)

            
        
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.background = pygame.image.load(os.path.join("images", "background1.png")).convert_alpha()
        self.fps = FPS
        self.level = 1
        self.levels = 1
        #Find out how many levels in total
        while os.path.isfile(os.path.join("levels", "level%d.LEVEL" % self.levels)):
            self.levels += 1

        self.levels -= 1 #The while loop breaks out when there is no level file at self.levels...so subtract 1 to get number of levels. 

        self.blocks = pygame.sprite.RenderUpdates()
        self.powerups = pygame.sprite.RenderUpdates()
        self.effects = pygame.sprite.RenderUpdates()
        self.balls = pygame.sprite.RenderUpdates()
        self.player = pygame.sprite.RenderUpdates()
        self.texts = pygame.sprite.RenderUpdates()

        player = Player(PLAYER_START)
        self.player.add(player)

        ball = Ball()
        ball.clamp(self.player.sprites()[0])
        self.balls.add(ball)

        self.livesText = Text("Lives: %d" % player.lives, (0,0))
        self.levelText = Text("Level: %d" % self.level, (540, 0))
        self.texts.add(self.livesText, self.levelText)

        self.powerup_types = [POWERUP_BALL, POWERUP_LIGHTNING, POWERUP_PADDLE, POWERUP_LASER] #List of possible powerups to randomly choose from

        self.clock = pygame.time.Clock()

        self.loadLevel(self.level)

    def reset(self):
        self.blocks = pygame.sprite.RenderUpdates()
        self.powerups = pygame.sprite.RenderUpdates()
        self.effects = pygame.sprite.RenderUpdates()
        self.balls = pygame.sprite.RenderUpdates()
        self.player = pygame.sprite.RenderUpdates()
        self.texts = pygame.sprite.RenderUpdates()

        player = Player(PLAYER_START)
        self.player.add(player)

        ball = Ball()
        ball.clamp(self.player.sprites()[0])
        self.balls.add(ball)

        self.livesText = Text("Lives: %d" % player.lives, (0,0))
        self.levelText = Text("Level: %d" % self.level, (540, 0))
        self.texts.add(self.livesText, self.levelText)

        self.loadLevel(self.level)

    def run(self):
        self.screen.blit(self.background, (0,0))
        pygame.display.update() #update the whole screen once...after this only dirty portions of the screen are updated
        pygame.mouse.set_visible(False) #hide the mouse cursor
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.blocks.empty() #convenient way to switch between levels. Take it out in the full version!!!!!!
                            
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1: #launch ball
                        if self.balls.sprites()[0].clamped == True:
                            self.balls.sprites()[0].launch()

                        
            self.clock.tick(self.fps)

            #update player
            self.player.update()

            #update ball
            if self.balls.sprites()[0].clamped == True:
                self.balls.sprites()[0].clamp(self.player.sprites()[0])
            else:
                for ball in iter(self.balls):
                    ball.checkWallCollisions()
            
                    collision = pygame.sprite.spritecollideany(ball, self.blocks) #did the ball hit any blocks?
                    if collision != None: 
                        get_power_up = random.choice(POWERUP_PROB) #should a powerup spawn? 
                        if get_power_up == True:
                            powerup_type = random.choice(self.powerup_types)
                            powerup = PowerUp(powerup_type)
                            powerup.rect.midtop = collision.rect.midbottom
                            self.powerups.add(powerup)


                        #check if the ball bounced off a vertical side or horizontal side of the block
                        if ball.rect.x <= collision.rect.left:
                            ball.bounce(diff = 1)
                            ball.rect.left = collision.rect.left - 2
                        elif ball.rect.x >= collision.rect.right:
                            ball.bounce(diff = 1)

                        elif collision.rect.left <= ball.rect.x <= collision.rect.right:
                            ball.bounce()

                        #what to do for various different blocks
                        if 1 < collision.level < 5:
                            collision.levelDown()
                        elif collision.level == 5: #hit a blast block
                            blast = Blast(collision.rect.center)
                            self.effects.add(blast)
                            collision.kill()
                        elif collision.level == 6:
                            pass #hard block...can't break it
                        elif collision.level == 1:
                            collision.kill()
                        

                    #collision detection with player
                    collision = pygame.sprite.spritecollideany(ball, self.player)
                    player = self.player.sprites()[0]
                    if collision != None:
                        if (player.rect.right - CORNER_WIDTH <= ball.rect.centerx <= player.rect.right) and (ball.get_direction()[0] < 0):
                            ball.bounce(diff=-1) #bounce back 
                        elif player.rect.left <= ball.rect.centerx <= player.rect.left + CORNER_WIDTH and (ball.get_direction()[0] > 0):
                            ball.bounce(diff=-1) #bounce back
                        else:
                            ball.bounce() #bounce normally
                            
                    if ball.rect.top > SCREEN_SIZE[1]:
                        ball.kill()

                self.balls.update()
                if len(self.balls) == 0: #if no balls on screen, then create new ball and take away a player life
                    ball = Ball()
                    ball.clamp(self.player.sprites()[0])
                    self.balls.add(ball)
                    self.player.sprites()[0].lives -= 1
                    self.livesText.changeMessage("Lives: %d" % self.player.sprites()[0].lives)
                    if self.player.sprites()[0].lives < 0: #if player is out of lives then its game over
                        self.gameOver()
                        self.level = 1
                        self.loadLevel(self.level)
                        self.levelText.changeMessages("Level: %d" % self.level)


            #manage and update powerups
            self.powerups.update()
            powerup = pygame.sprite.spritecollideany(self.player.sprites()[0], self.powerups)
            if powerup != None:
                if powerup.type == POWERUP_BALL:
                    powerup.kill()
                    if self.balls.sprites()[0].clamped == False: #Don't spawn an extra ball if the player gets the powerup before launching his ball into play
                        extra_ball = Ball()
                        extra_ball.clamp(self.player.sprites()[0])
                        extra_ball.launch()
                        self.balls.add(extra_ball)

                elif powerup.type == POWERUP_LIGHTNING:
                    powerup.kill()
                    for ball in iter(self.balls):
                        if ball.speed < ball.max_speed:
                            ball.speed += POWERUP_EXTRA_SPEED

                elif powerup.type == POWERUP_PADDLE:
                   powerup.kill()
                   if self.player.sprites()[0].big == False: #player can't keep on upgrading size. You can only get bigger once.
                       self.player.sprites()[0].growBig()

                elif powerup.type == POWERUP_LASER:
                    powerup.kill()
                    laser = Laser(self.player.sprites()[0].rect.midtop)
                    self.effects.add(laser)

            #manage and update effects
            self.effects.update()
            for effect in iter(self.effects):
                if isinstance(effect, Laser):
                    collision =  pygame.sprite.spritecollideany(effect, self.blocks)
                    if collision != None:
                        if collision.level < 6:
                            collision.kill()
                    if effect.rect.bottom < 0:
                        effect.kill()

                elif isinstance(effect, Blast):
                    collision =  pygame.sprite.spritecollideany(effect, self.blocks)
                    if collision != None:
                        collision.kill()
                        

            #test to see if only unbreakable blocks remain, if so then move onto next level
            if (all(block.level == 6 for block in self.blocks)) or (len(self.blocks)==0):
                if self.level < self.levels:
                    self.level += 1
                    pygame.time.wait(1000)
                    self.loadLevel(self.level)
                    self.levelText.changeMessage("Level: %d" % self.level)

                else:
                    self.gameWon()

            
            self.player.clear(self.screen, self.background)
            self.balls.clear(self.screen, self.background)
            self.blocks.clear(self.screen, self.background)
            self.powerups.clear(self.screen, self.background)
            self.effects.clear(self.screen, self.background)
            self.texts.clear(self.screen, self.background)

            dirty_rects = []
            dirty_rects.extend(self.player.draw(self.screen))
            dirty_rects.extend(self.balls.draw(self.screen))
            dirty_rects.extend(self.blocks.draw(self.screen))
            dirty_rects.extend(self.powerups.draw(self.screen))
            dirty_rects.extend(self.effects.draw(self.screen))
            dirty_rects.extend(self.texts.draw(self.screen))

            pygame.display.update(dirty_rects)

    def loadLevel(self, level):
        self.blocks.empty() #pre-caution. empty blocks group
        #parse level file based on self.level
        level_file = open(os.path.join("levels", "level%d.LEVEL" % level))
        level_template = level_file.readlines()
        #strip away new line chars and all empty spaces
        for line in level_template:
            index = level_template.index(line)
            level_template[index] = line.strip()

        #using the level file template, create new block array
        x,y = BLOCK_START
        for line in level_template:
            for block_level in line:
                if int(block_level) > 0:
                    block = Block((x,y),int(block_level))
                    self.blocks.add(block)
                x += BLOCK_WIDTH

            x = BLOCK_START[0]
            y += BLOCK_HEIGHT

    def gameOver(self):
        self.screen.fill((255,255, 255))
        background = pygame.image.load(os.path.join("images", "menu_background.jpg"))
        self.screen.blit(background, (0,0))
        pygame.display.update()
        
        gameOverText = Text("Game Over", (215,150), font_family = "Comic Sans MS", font_size = 40)
        newGameText = Text("New Game", (100, 350), font_family = "Comic Sans MS")
        quitText = Text("Quit", (500, 350), font_family = "Comic Sans MS")

        texts = pygame.sprite.RenderUpdates()
        images = pygame.sprite.RenderUpdates()
        texts.add(newGameText, quitText)
        images.add(gameOverText)

        pygame.mouse.set_visible(True)
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    if newGameText.rect.collidepoint(event.pos):
                        self.reset()
                        self.run()
                    elif quitText.rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            texts.update()

            texts.clear(self.screen, background)
            images.clear(self.screen, background)

            dirty_rects = texts.draw(self.screen)
            dirty_rects.extend(images.draw(self.screen))
            pygame.display.update(dirty_rects)

    def gameWon(self):
        self.screen.fill((255,255, 255))
        background = pygame.image.load(os.path.join("images", "menu_background.jpg"))
        self.screen.blit(background, (0,0))
        pygame.display.update()

        gameWonText = Text("Congratulations! You won the game!", (100,100))

        self.screen.blit(gameWonText.image, gameWonText.rect)
        pygame.display.update()
            
        pygame.time.wait(1250)
        pygame.quit()
        sys.exit()

            
def main():
    pygame.init()
    game = Game()

    #Both functions have built in while loops and event handler loops. so just run both back to back - when mainScreen returns, game runs.
    mainScreen(game.screen)
    game.run()

if __name__ == '__main__':
    main()
