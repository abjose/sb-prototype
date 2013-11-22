import pygame
#from sb_test import Graph, Topic
import graph


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
- change variable naming weirdness, comments...
- add a 'path' button - if two things are highlighted
-- OR could just do something like 'press m for menu' then that goes to command line and can enter normal commands...
- Add another button that allows you to print a nested list / hierarchy graph thing (also maybe another that prints adjacency graph)
- Have hierarchy viewing mode? (like press a button and can see hierarchy)
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
        #       and maybe auto-ellipsis if wayyyy too long
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
    # Graph stuff
    G = graph.Graph()

    # pygame stuff...
    screen  = pygame.display.set_mode((600,600))
    running = True

    # key press events
    menuRequest = False

    # stuff for double-click detection
    clickClock  = pygame.time.Clock()
    clickThresh = 225 # ms
    doubleClick = False

    MousePressed  = False # Pressed down THIS FRAME
    MouseReleased = False # Released THIS FRAME
    MouseDown     = False # mouse is held down
    Target = None # target of Drag/Drop
    #RenderList = [] # list of objects

    while running:
        screen.fill((0,0,0)) # clear screen
        pos=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                break # get out now
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                MousePressed=True 
                MouseDown=True 
                # should this be moved elsewhere to keep event handling code
                # minimal?
                clickClock.tick()
                doubleClick = clickClock.get_time() <= clickThresh
               
            if event.type == pygame.MOUSEBUTTONUP:
                MouseReleased=True
                MouseDown=False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #menuRequest = True
                    G.run_cmd()
                    # or could just call Graph's 'menu' stuff? or should 
                    # have elsewhere?
             
        if MousePressed==True:
            #for item in RenderList: # search all items
            for item in G.AG: # search all items
                if (item.textbox.in_bound(pos)):
                    Target=item # "pick up" item
                    break
            
            if Target is None and doubleClick: 
                Target = graph.Topic(raw_input('Topic title: '), pos)
                G.add_topic(Target)
                #RenderList.append(Target) # add to list of things to draw
            
            elif doubleClick:
                Target.textbox.highlight = not Target.textbox.highlight
        
        if MouseDown and Target is not None: # if we are dragging something
            Target.textbox.pos=pos # move the target with us
        
        if MouseReleased:
            Target=None # Drop item, if we have any
            
        #for item in RenderList:
        for item in G.AG:
            # render lines first
            # how to make directed? maybe don't worry about for now
            for successor in G.AG.successors(item):
                #pygame.draw.aaline(screen, (0,255,0), (20,20), (80,60))
                pygame.draw.aaline(screen, (0,255,0),
                                   item.textbox.rect.center,
                                   successor.textbox.rect.center)
            # then render text boxes
            item.textbox.render(screen) # Draw all items

        # TODO: draw lines from centers...

              
        MousePressed=False # Reset these to False
        MouseReleased=False # Ditto     
        menuRequest = False
        pygame.display.flip()
    return 
    
if __name__=='__main__':
    main() # Execute our main function
