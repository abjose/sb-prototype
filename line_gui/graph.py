import networkx as nx
import gfx


"""
TODO:
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
        if self.get_topic(t.title) == None:
            self.AG.add_node(t)
            self.HG.add_node(t)
            return True
        return False

    def can_expand(self, t):
        """ Only let topics expand if they have children. """
        #t = self.get_topic(title)
        return self.HG.successors(t) != []

    def unexpand_parents(self, t):
        for p in self.HG.predecessors(t):
            p.expanded = False

    def any_ancestors_visible(self, t):
        preds = self.HG.predecessors(t)
        return any([self.should_display(p) for p in preds]) or \
               any([self.any_ancestors_visible(p) for p in preds])

    def should_display(self, t):
        # TODO: THIS IS WRONG!!!
        """ Return true if should display given Topic. """
        # t should be an object
        #if not t in self.HG:
        #    return True # no ancestors - definitely display
        #    # buhhh...what if expanded??? 
        #else:
        preds = self.HG.predecessors(t)
        #return not t.expanded and not any([self.should_display(p)
        #                                   for p in preds])            
        return not t.expanded and not self.any_ancestors_visible(t)

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
            self.AG.add_edges_from([(p,tpc) for p in self.AG.predecessors(t)])
            self.AG.add_edges_from([(tpc,p) for p in self.AG.successors(t)])
    
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


