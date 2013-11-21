import networkx as nx
#from dnd import TextBox
import gfx


"""
Potential initial code stuff:
- allow to make new topics
- allow to make edges from one topic to another
- allow to merge with sibling (suggest automatically?)
- allow to merge with neighbor
- merges create new topics containing a list of all immediate children
-- is this the best way to store hierarchy?
-- could instead create new graphs in the networkx graph?
-- and resources just have null subgraphs?
-- but how to figure out hierarchy for display purposes?
-- could just do the whole dual adjacency/hierarchy graph thing
- Add dnd TextBoxes to Topic objects
"""


class Topic(object):

    def __init__(self, title, pos=None):
        self.title   = title
        self.textbox = gfx.TextBox(title, pos)
    
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

    def add_path(self, *args):
        """ Make a path over the passed topics. """
        self.AG.add_path(args)

    def merge(self, tpc, *args):
        # should edges be inherited from existing resources, or "given"
        # at time of merge? (so will exist even if resources deleted)
        for t in args:
            self.HG.add_edge(tpc, t)
            self.AG.add_edges_from([(tpc, p) for p in self.AG.predecessors(t)])
            self.AG.add_edges_from([(tpc, p) for p in self.AG.successors(t)])
        
        
    def split(self, tpc, *args):
        pass

if __name__=='__main__':

    t1 = Topic('poop1')
    t2 = Topic('poop2')
    t3 = Topic('poop3')
    t4 = Topic('poop4')
    t5 = Topic('poop5')

    g = Graph()
    g.add_path(t1,t2,t3,t4,t5)
    g.merge(Topic('fecal matter'), t1, t2)

    print g.AG.edges()
    print g.HG.edges()
