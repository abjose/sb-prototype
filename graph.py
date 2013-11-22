import networkx as nx
#from dnd import TextBox
import gfx


"""
TODO:
- enforce uniqueness constraint on topic titles
- suggest likely merges automatically?
"""


class Topic(object):

    def __init__(self, title, pos=None):
        self.title    = title
        self.expanded = False
        self.textbox  = gfx.TextBox(title, pos)
    
    def __repr__(self):
        return self.title


class Graph(object):

    def __init__(self):
        self.AG = nx.DiGraph() # adjacency graph
        self.HG = nx.DiGraph() # hierarchy graph

    def get_topic(self, title):
        for t in self.AG.nodes():
            if t.title == title:
                return t
        return None

    def add_topic(self, t):
        self.AG.add_node(t)

    #def can_expand(self, title):
    def can_expand(self, t):
        """ Only let topics expand if they have children. """
        #t = self.get_topic(title)
        return self.HG.successors(t) != []

    def unexpand_parents(self, t):
        for p in self.HG.predecessors(t):
            p.expanded = False

    #def should_display(self, title, obj=None):
    def should_display(self, t):
        """ Return true if should display given Topic. """
        # t should be an object
        #t = self.get_topic(title) if obj==None else obj
        if not t in self.HG:
            return True # no ancestors - definitely display
        else:
            preds = self.HG.predecessors(t)
            return not t.expanded and not any([self.should_display(p) 
                                               for p in preds])            

    def add_path(self, *args):
        """ Make a path over the passed topics TITLES. """
        self.AG.add_path([self.get_topic(a) for a in args])

    def merge(self, tpc, *args):
        # tpc and *args should be topic TITLES!
        # should edges be inherited from existing resources, or "given"
        # at time of merge? (so will exist even if resources deleted)
        # Think they should be given and then removed if necessary?...
        # what if tpc appears in args? are self-edges allowed?
        tpc = self.get_topic(tpc)
        args = [self.get_topic(a) for a in args]
        for t in args:
            self.HG.add_edge(tpc, t)
            self.AG.add_edges_from([(tpc, p) for p in self.AG.predecessors(t)])
            self.AG.add_edges_from([(tpc, p) for p in self.AG.successors(t)])
    
    def split(self, tpc, *args):
        pass

    def run_cmd(self):
        # ideally would be a little CLI, just do input() for now
        try: exec('self.'+raw_input('Enter command: ')) # DANGER DANGER
        except Exception as e: print 'Command failed:', e 
            
        
        

if __name__=='__main__':

    t1 = Topic('poop1')
    t2 = Topic('poop2')
    t3 = Topic('poop3')
    t4 = Topic('poop4')
    t5 = Topic('poop5')

    g = Graph()
    #g.add_path(t1,t2,t3,t4,t5)
    #g.merge(Topic('fecal matter'), t1, t2)

    g.text_cmd()

    print g.AG.edges()
    print g.HG.edges()

