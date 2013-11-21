import pygame
from sb_test import Graph, Topic

"""
TODO:
- allow (directed...somehow) lines to be drawn (if you click on another node
  with one highlighted?) Should...just query networkx graph from other code?
  Or could store in nodes..
  Or...could not make through GUI at all, make in command line and just
  update display by looking at networkx graph...
  Or both - can add through GUI or command line...?
- Move networkx stuff here - 
- When making new node, query topic title in command line
- add clock to limit frame rate?
"""

class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, pos, color=(255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        self.pad   = 5
        self.text  = text
        self.pos   = pos
        self.color = color
        self.visible   = True
        self.highlight = False
        self.initFont()
        self.initGroup()


    def initFont(self):
        pygame.font.init()
        self.font = pygame.font.Font(None,16)

    def initGroup(self):
        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

    def setBox(self, color):
        w,h = self.font.size(self.text)
        self.image = pygame.Surface((w+2*self.pad, h+2*self.pad))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def setText(self, color):
        # TODO: make auto-newline if text too long
        #       and maybe auto-ellipse if wayyyy too long
        x = self.font.render(self.text,True,color)
        self.image.blit(x,(self.pad, self.pad))

    def in_bound(self, pos):
        return self.rect.collidepoint(pos)

    def render(self, screen):
        inverse = (255-self.color[0],255-self.color[1],255-self.color[2])
        if self.highlight:
            self.setBox(inverse)
            self.setText(self.color)
        else:
            self.setBox(self.color)
            self.setText(inverse)
        screen.blit(self.image, self.rect)


def main(): 
    screen  = pygame.display.set_mode((600,600))
    running = True

    clickClock  = pygame.time.Clock()
    clickThresh = 225 # ms
    doubleClick = False

    MousePressed  = False # Pressed down THIS FRAME
    MouseReleased = False # Released THIS FRAME
    MouseDown     = False # mouse is held down
    Target = None # target of Drag/Drop
    RenderList = [] # list of objects

    while running:
        screen.fill((0,0,0)) # clear screen
        pos=pygame.mouse.get_pos()
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                running=False
                break # get out now
            
            if Event.type == pygame.MOUSEBUTTONDOWN:
                MousePressed=True 
                MouseDown=True 
                clickClock.tick()
                doubleClick = clickClock.get_time() <= clickThresh
               
            if Event.type == pygame.MOUSEBUTTONUP:
                MouseReleased=True
                MouseDown=False
             
        if MousePressed==True:
            for item in RenderList: # search all items
                if (item.in_bound(pos)):
                    Target=item # "pick up" item
                    break
            
            if Target is None: # didn't find any?
                #Target=Node((0,0,255),pos,10) # create a new one
                Target=TextBox('meowasdf', pos) # create a new one
                RenderList.append(Target) # add to list of things to draw
            elif doubleClick:
                Target.highlight = not Target.highlight
        
        if MouseDown and Target is not None: # if we are dragging something
            Target.pos=pos # move the target with us
        
        if MouseReleased:
            Target=None # Drop item, if we have any
            
        for item in RenderList:
            item.render(screen) # Draw all items

        # TODO: draw lines from centers...
        pygame.draw.aaline(screen, (255,0,0), (20,20), (80,60))
              
        MousePressed=False # Reset these to False
        MouseReleased=False # Ditto        
        pygame.display.flip()
    return 
    
if __name__=='__main__':
    main() # Execute our main function
