import pygame
#from sb_test import Graph, Topic
import graph


"""
TODO:
- figure out best way to make lines directed
- add clock to limit frame rate?
- Add another button that allows you to print a nested list / hierarchy graph thing (also maybe another that prints adjacency graph)
- Have hierarchy viewing mode? (like press a button and can see hierarchy rather than adjacency connections)
- remove highlighting code if not going to use? then could use double-click for expanding merged nodes, and maybe double-right click for contracting?
- add code for hierarchy visibility - if top is visible, don't go down further (even if sub-nodes are marked as visible), but if not can keep iterating down...?
- only allow to be expanded if has children?

So, to do this, if double-clicking on something and it has children, should set its visibility to False (print something if no children). Then should auto-display children
Then when double right-click should set all parent's visibility to True
Perhaps should change 'visibility' to 'is_expanded' or something
"""

class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, pos, color=(255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        self.pad   = 5
        self.text  = text
        self.pos   = pos
        self.color = color
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
    clickThresh = 300 # ms
    doubleClick = False
    doubleRightClick = False

    # mouse press events
    mousePressed  = False # Pressed down THIS FRAME
    mouseReleased = False # Released THIS FRAME
    mouseDown     = False # mouse is held down
    target = None # target of Drag/Drop

    while running:
        screen.fill((0,0,0))
        pos=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break # exit
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True 
                mouseDown = True 
                # should this be moved elsewhere to keep event handling code
                # minimal?
                clickClock.tick()
                # assumes same button pressed...
                if event.button == 1: # left mouse button
                    doubleClick = clickClock.get_time() <= clickThresh
                if event.button == 3: # right mouse button
                    doubleRightClick = clickClock.get_time() <= clickThresh
               
            if event.type == pygame.MOUSEBUTTONUP:
                mouseReleased = True
                mouseDown = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #menuRequest = True
                    G.run_cmd()
                    # or could just call Graph's 'menu' stuff? or should 
                    # have elsewhere?
             
        if mousePressed == True:
            for item in G.AG:
                if (item.textbox.in_bound(pos)):
                    target = item # "pick up" item
                    break
            
            if target is None and doubleClick: 
                target = graph.Topic(raw_input('Topic title: '), pos)
                G.add_topic(target)
            
            elif doubleClick:
                #target.textbox.highlight = not target.textbox.highlight
                target.expanded = G.can_expand(target)
        
        if mouseDown and target is not None: # if dragging
            target.textbox.pos=pos # move target 
        
        if mouseReleased:
            target=None # drop target
            
        for item in G.AG:
            # don't render anything if shouldn't display
            if not G.should_display(item):
                continue
            # render lines first
            for successor in G.AG.successors(item):
                if G.should_display(successor):
                    pygame.draw.aaline(screen, (0,255,0),
                                       item.textbox.rect.center,
                                       successor.textbox.rect.center)
            # then render text boxes
            item.textbox.render(screen)
              
        mousePressed  = False
        mouseReleased = False 
        menuRequest   = False
        pygame.display.flip()
    return 
    
if __name__=='__main__':
    main() # Execute our main function
