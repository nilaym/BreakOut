import pygame, sys, os
from pygame.locals import *

global SCREEN_SIZE, FPS, GRID_TOPLEFT, NUM_OF_ROWS, NUM_OF_COLUMNS, BLOCK_SIZE, MAX_LEVEL
SCREEN_SIZE = (640,640)
FPS = 60
GRID_TOPLEFT = (70,100)
NUM_OF_ROWS = 10
NUM_OF_COLUMNS = 10
BLOCK_SIZE = (50,20)
MAX_LEVEL = 6

class Block:
    def __init__(self, pos, level=1):
        self.level = level
        if self.level > 0:
            self.image = pygame.image.load(os.path.join("images", "block%d.png" % self.level)).convert_alpha()
            self.rect = self.image.get_rect(topleft = pos)

        else:
            self.rect = pygame.Rect(0,0,BLOCK_SIZE[0], BLOCK_SIZE[1])
            self.rect.topleft = pos

    def levelUp(self, value = -1):
        if value == -1:
            if self.level < MAX_LEVEL:
                self.level += 1
                self.image = pygame.image.load(os.path.join("images", "block%d.png" % self.level)).convert_alpha()

            else:
                self.level = 0

        else:
            self.level = value
            self.image = pygame.image.load(os.path.join("images", "block%d.png" % self.level)).convert_alpha()
            

    def levelDown(self):
        if self.level > 1:
            self.level -= 1
            self.image = pygame.image.load(os.path.join("images", "block%d.png" % self.level)).convert_alpha()

        else:
            self.level = 0
            
        
    def draw(self, surface):
        if self.level > 0:
            surface.blit(self.image, self.rect)

class Grid:
    def __init__(self):
        self.topleft = GRID_TOPLEFT
        self.data = []
        for r in xrange(NUM_OF_ROWS):
            self.data.append([])
        for row in self.data:
            for c in xrange(NUM_OF_COLUMNS):
                row.append(0)

        self.blocks = []
        x,y = self.topleft
        for row in self.data:
            for cell in row:
                block = Block((x,y),0)
                self.blocks.append(block)
                x += BLOCK_SIZE[0]

            x = self.topleft[0]
            y += BLOCK_SIZE[1]

    def saveLevel(self):
        count = 1
        filename = 'level%d.LEVEL' % count
        while os.path.isfile(os.path.join("levels", filename)):
            count += 1
            filename = 'level%d.LEVEL' % count


        f = open(os.path.join("levels",filename), 'w')
        block_count = 0
        for block in self.blocks:
            f.write('%d' % block.level)
            block_count += 1
            if block_count == NUM_OF_COLUMNS:
                block_count = 0
                f.write('\n')

        f.close()
        
        
    def draw(self, surface):
        x,y = self.topleft
        for r in xrange(NUM_OF_ROWS+1):
            pygame.draw.line(surface, (0,0,0), (x,y), (x+(NUM_OF_COLUMNS*BLOCK_SIZE[0]),y))
            y += BLOCK_SIZE[1]

        x,y = self.topleft
        for c in xrange(NUM_OF_COLUMNS+1):
            pygame.draw.line(surface, (0,0,0), (x,y), (x,(y+(NUM_OF_ROWS*BLOCK_SIZE[1]))))
            x += BLOCK_SIZE[0]

        for block in self.blocks:
            block.draw(surface)

        
        
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    clock = pygame.time.Clock()

    grid = Grid()

    value = -1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    grid.saveLevel()
                elif event.key == K_a:
                    value = input("Block level")
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for block in grid.blocks:
                        if block.rect.collidepoint(event.pos):
                            if block.level == 0:
                                block.levelUp(value)
                            else:
                                block.levelUp()

                elif event.button == 3:
                    for block in grid.blocks:
                        if block.rect.collidepoint(event.pos):
                            block.levelDown()
                            
            elif event.type == MOUSEBUTTONUP:
                pass

        clock.tick(FPS)

        screen.fill((255,255,255))

        grid.draw(screen)       

        pygame.display.update()



if __name__ == '__main__':
    main()
