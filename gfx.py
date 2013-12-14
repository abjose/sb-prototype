import pygame
import graph
import math as m
import numpy as np


"""
TODO:
- figure out best way to make lines directed
- move the testing stuff into another file
- add clock to limit frame rate?
- Add another button that allows you to print a nested list / hierarchy graph thing (also maybe another that prints adjacency graph)
- Have hierarchy viewing mode? (like press a button and can see hierarchy rather than adjacency connections)
- add code for hierarchy visibility - if top is visible, don't go down further (even if sub-nodes are marked as visible), but if not can keep iterating down...?
"""

class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, pos, color=(255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        self.pad   = 5
        self.text  = text
        self.pos   = pos
        self.color = color
        self.initFont()
        self.initGroup()
        self.setBox()

    def initFont(self):
        pygame.font.init()
        self.font = pygame.font.Font(None,16)

    def initGroup(self):
        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

    def setBox(self):
        w,h = self.font.size(self.text)
        self.image = pygame.Surface((w+2*self.pad, h+2*self.pad))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def setText(self):
        # TODO: make auto-newline if text too long
        #       and maybe auto-ellipsis if wayyyy too long
        x = self.font.render(self.text,True,(255-self.color[0],
                                             255-self.color[1],
                                             255-self.color[2]))
        self.image.blit(x,(self.pad, self.pad))

    def in_bound(self, pos):
        return self.rect.collidepoint(pos)

    def render(self, screen):
        self.setBox()
        self.setText()
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

    # testing
    # should really move this into a separate file or something
    # make sure to have at least one non-sibling merge and one sibling merge
    
    # NOTE: this topic progression taken from a Hyper-Textbook on Optimization
    #       models and applications from a class at Berkeley:
    #       https://inst.eecs.berkeley.edu/~ee127a/book/login/index.html

    # highest-level topic for demo
    G.add_topic(graph.Topic('Linear Algebra', (285,290)))

     # subtopics of linear algebra
    G.add_topic(graph.Topic('Vectors', (50,120)))
    G.add_topic(graph.Topic('Matrices', (150,115)))
    G.add_topic(graph.Topic('Linear Equations', (280,115)))
    G.add_topic(graph.Topic('Least-Squares', (430,115)))
    G.add_topic(graph.Topic('Eigenvalues', (500,170)))
    G.add_topic(graph.Topic('Singular Values', (525,230)))

    # subtopics of vectors
    G.add_topic(graph.Topic('Vector basics', (60,165)))
    G.add_topic(graph.Topic('Scalar products, norms and angles', (120,220)))
    G.add_topic(graph.Topic('Projection on a line', (170,280)))
    G.add_topic(graph.Topic('Orthogonalization', (250,340)))
    G.add_topic(graph.Topic('Hyperplanes and half-spaces', (310,380)))
    G.add_topic(graph.Topic('Linear functions', (360,430)))
    G.add_topic(graph.Topic('Application: data visualization', (410,480)))
    G.add_topic(graph.Topic('Vector exercises', (465,535)))

    # add path and merge for vector stuff
    G.add_path('Vector basics', 'Scalar products, norms and angles', 
               'Projection on a line', 'Orthogonalization', 
               'Hyperplanes and half-spaces', 'Linear functions', 
               'Application: data visualization', 'Vector exercises')
    G.merge('Vectors', 
            'Vector basics', 'Scalar products, norms and angles', 
            'Projection on a line', 'Orthogonalization', 
            'Hyperplanes and half-spaces', 'Linear functions', 
            'Application: data visualization', 'Vector exercises')
    
    # add path and merge for linear algebra stuff
    G.add_path('Vectors','Matrices','Linear Equations', 'Least-Squares', 
               'Eigenvalues', 'Singular Values')
    G.merge('Linear Algebra', 
            'Vectors','Matrices','Linear Equations', 'Least-Squares', 
            'Eigenvalues', 'Singular Values')

    t = G.get_topic('Vector basics')

    """
    G.add_topic(graph.Topic('a', (10,30)))
    G.add_topic(graph.Topic('b1', (30,30)))
    G.add_topic(graph.Topic('b2', (50,30)))
    G.add_topic(graph.Topic('c', (70,30)))
    G.add_topic(graph.Topic('B', (40,50)))
    G.add_path('a','b1','c')
    G.add_path('a','b2','c')
    G.merge('B', 'b1','b2')
    """


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
                doubleClick = False
                doubleRightClick = False
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
                if (item.textbox.in_bound(pos)) and G.should_display(item):
                    target = item # "pick up" item
                    print 'picked up ' + target.title
                    break
            
            if target is not None and doubleClick:
                print 'trying to expand ' + target.title
                target.expanded = G.can_expand(target)
                
            if target is not None and doubleRightClick:
                print 'trying to collapse ' + target.title
                G.unexpand_parents(target)

            if target is None and doubleClick: 
                target = graph.Topic(raw_input('Topic title: '), pos)
                if not G.add_topic(target):
                    print 'That topic already exists.'
                    target = None
        
        if mouseDown and target is not None: # if dragging
            target.textbox.pos=pos # move target 
        
        if mouseReleased:
            target=None # drop target
            
        for item in G.AG:
            # render lines first
            if G.should_display(item):
                for successor in G.AG.successors(item):
                    if G.should_display(successor):
                        # NEW LINE CODE HERE
                        make_directed_line(screen, 
                                           item.textbox.rect.center,
                                           successor.textbox.rect.center)
                        #pygame.draw.aaline(screen, (0,255,0),
                        #                   item.textbox.rect.center,
                        #                   successor.textbox.rect.center)
        for item in G.AG:
            # then render text boxes
            if G.should_display(item):
                item.textbox.render(screen)
              
        mousePressed  = False
        mouseReleased = False 
        menuRequest   = False
        pygame.display.flip()
    return 
    
def make_directed_line(screen, start, end):
    # make a line composed of arrows
    # TODO: interpolate colors! ...maybe.
    scale     = 7.0
    step_size = 25.
    arrow = scale*np.matrix([[0.,1.],
                             [0.,-1.],
                             [1.,0.]])
    x0,y0 = start
    x1,y1 = end
    dx = float(x0) - x1
    dy = float(y0) - y1
    
    # find angles and rotation
    th = -m.atan2(dy,dx)
    R  = -np.matrix([[m.cos(th), -m.sin(th)],
                     [m.sin(th), m.cos(th)]])
    # then rotate arrow
    arrow = arrow*R

    # normalize vectors
    d = m.sqrt(dx*dx + dy*dy)
    dx = -dx/d if d!=0 else 0
    dy = -dy/d if d!=0 else 0

    # iterate down path
    for offset in np.arange(0,d,step_size):
        tx = x0 + offset*dx
        ty = y0 + offset*dy
        arrow_t = arrow + (tx,ty)
        arrow_t = [(pt[0,0], pt[0,1]) for pt in arrow_t]
        pygame.draw.polygon(screen, (0,255,0), arrow_t, 0)
    


if __name__=='__main__':
    # show help text
    print "This is a prototype for testing out graph contractions\n" + \
          "for building 'useful' hierarchies of 'Topics'.\n\n" + \
          "- Click and drag to move topics around.\n" + \
          "- Double click an empty space to create a new topic.\n" + \
          "- Double left-click to expand topics into their subtopics\n" + \
          "- Double right-click to collapse topics into their supertopics\n" + \
          "- Press enter to enter commands in the terminal. Examples:\n" + \
          "    'path('t1', 't2', ...) makes a (directed) path t1->t2->...\n" + \
          "    'merge('T', 't1', 't2', ...) merges t1, t2, ... into T\n" + \
          " For example, try double-clicking Linear Algebra to expand it,\n" + \
          " Then double-clicking 'Vectors' to expand that.\n" + \
          " Note that only the 'Vectors' topic has further subtopics right now."
    main() # Execute our main function
