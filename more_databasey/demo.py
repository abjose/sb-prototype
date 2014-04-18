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
    def __init__(self, ground_truth_graph, honesty):
        # honesty is proportion of truths told in [0,1]
        self.g = ground_truth_graph
        self.h = honesty

    def suggest_nodes(self, ):
        pass

    def suggest_relation(self, n1, n2):
        # suggest relationship between nodes n1 and n2
        pass


class Querier:
    def __init__(self, pop, mean=0.7, sd=0.3):
        self.graph = get_random_graph()
        self.users = [Foracle(graph, clamp(np.random.normal(mean,sd),0.,1.)) 
                      for _ in pop]
        # map from user to estimated honesty value
        self.trust = dict()


def clamp(n, a, b):
    # assumes a <= n <= b
    return max(min(n, b), a)


def get_random_graph():
    # make random graph
    # should assign types to edges!
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

