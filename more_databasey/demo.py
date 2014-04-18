#import yaml
#import sys
#import pprint
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

"""

Read in a yaml network description, put it into NetworkX

use dotfiles?
could just use networkx graph layouts? just show evolution of connections
in series of plots/single plot? (cool if had dragger...)

TODO
- decide on what format to use
- make one or more test graphs
- read in to python as a networkx digraph
- make a 'foracle' class that takes a networkx digraph and truthiness
- give foracle 'suggest_node' and 'suggest_relation(n1,n2)' fns
- make a 'querier' class that takes or makes a (list of) foracle object(s)
- make querier query foracle about existence of and relations between nodesre
- if possible - display series of networkx graphs representations with
  a slider so you can slide through the graph over time
  consider also adding sliders for changing mean/SD of truthiness of foracles
  to make sliders discrete: http://stackoverflow.com/questions/13656387/can-i-make-matplotlib-sliders-more-discrete

DOESN'T EVEN HAVE TO BE AN ACTUAL GRAPH! JUST MAKE A RANDOM DIGRAPH? THEN
SHOW HOW CLOSE APPROXIMATION IS TO GROUND TRUTH

can maybe decrease convergence time by asking liars fewer questions

would be cool to allow clicking on nodes to highlight or something then
showing paths including all dependences between nodes...

"""


class Foracle:
    def __init__(self, ground_truth_graph, wrongness, honesty):
        self.g = mutate_garph(ground_truth_graph, wrongness)
        # wrongness is the amount the passed graph will be mutated in [0,1]
        # honesty is proportion of truths told in [0,1]
        self.h = honesty

    def suggest_nodes(self, ):
        pass

    def suggest_relation(self, n1, n2):
        # suggest relationship between nodes n1 and n2
        pass


class Querier:
    def __init__(self, pop, graph_size, connect_prob):
        # wrongness (w) and honesty (h) distribution parameters
        h_mean, h_sd = 0.7, 0.3
        w_mean, w_sd = 0.2, 0.5
        # make a random graph to try to approximate
        self.graph = get_random_graph(graph_size, connect_prob)
        # set of users with honesty values following passed distribution
        self.users = [Foracle(graph, 
                              clamp(np.random.normal(w_mean, w_sd),0.,1.), 
                              clamp(np.random.normal(h_mean, h_sd),0.,1.))
                      for _ in pop]
        # map from user to estimated 'reliablity' of user
        self.trust = dict()

    def get_trust_rankings(self, ):
        # return list of users from high to low trust values
        # might want to ask questions in proportion to trust instead of
        # asking, say, top 10?
        pass


def clamp(n, a, b):
    # assumes a <= n <= b
    return max(min(n, b), a)

def get_random_graph(n, p):
    # make random erdos-renyi graph with n nodes and connection probability p
    G = nx.DiGraph()
    # add nodes
    G.add_nodes_from(range(n))
    # add labeled edges
    for i in range(n):
        for j in range(n):
            if np.random.uniform() < p:
                # choose what kind of edge to make and add it to the graph
                G.add_edge(i, j, relation=get_random_relation())
    return G
        
def get_random_relation():
    # return a random type of relation as a string
    # these probabilities should sum to one
    p_type_of, p_part_of, p_prereq_of = 0.25, 0.25, 0.5
    r = np.random.uniform()
    if r < p_type_of:
        return 'type-of'
    if r < p_type_of+p_part_of:
        return 'part-of'
    if r < p_type_of+p_part_of+p_prereq_of:
        return 'prereq-of'

def mutate_graph(graph, wrongness):
    # mutate a graph according to wrongness value
    pass

if __name__=='__main__':
    
    # read yaml from stdin I guess
    #db = yaml.load(sys.stdin)
    # prettyprint it
    #pp = pprint.PrettyPrinter()
    #pp.pprint(db)
    #g = nx.DiGraph(db)
    #print g.edges()

    # test reading dot file
    r = nx.read_dot('test.dot')
    nx.draw(r)
    plt.show()

    # test writing dot file
    g = nx.DiGraph()
    g.add_nodes_from(['node1','node2','node3'])
    g.node['node1']['type'] = 'is-a'
    g.add_edges_from([('node1','node2'),
                      ('node2','node3')])
    nx.write_dot(g, 'test_write.dot')
    nx.draw(g)
    plt.show()

