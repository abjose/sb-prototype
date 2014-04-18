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

need to keep track of everything every oracle says so can properly update
values when get better idea of how trustworthy oracles are? Would be nicer if
not...


Ok, to build approximation graph...
iterate over all users - can choose to ask or not
If choose to ask, find something you have low confidence in


For updating trust, could give a 'test' question that you're fairly confident
about and another you're not.

Consider changing options available to oracles? Maybe can't suggest a node
but can only suggest relations, and in doing so can suggest new nodes or 
claim that a node doesn't exist

Change design slightly:
Rather than proposing to centralize thing, users collectively post modifications
to the central graph based on their own versions. Then other users vote on
whether they agree with the modification or not. This leads to a reputation
score...easier to track user that proposed a change (and associate that change
with the user's current rep) than to go in the other direction.

So just have each graph component have two associated lists - upvoters
and downvoters. "Belief" in component as well as reputation depends on 
who votes on what.

Also have a 'participation rate'? Probabiltiy that will actually participate
in a given round...

TODO: ALSO NEED TO CHECK RELATION IS RIGHT

lolz, just change so doesn't care if upvotes or downvotes exist?
"""


class User: # 'faulty oracle'
    def __init__(self, ground_truth_graph, honesty, misbelief, participation):
        self.g = mutate_graph(ground_truth_graph, misbelief)
        # misbelief is the amount the passed graph will be mutated in [0,1]
        # honesty is proportion of truths told in [0,1]
        self.h = honesty
        self.p = participation

    def browse(self, graph):
        # "browse" the passed graph
        # vote on existing nodes
        for n in graph.nodes():
            if np.random.uniform() < self.p:
                truth = n in self.g.nodes()
                if np.random.uniform() > self.h: truth = not truth
                if truth: add_upvote(graph.node[n], self)
                else:     add_downvote(graph.node[n], self)

        # vote on existing edges
        for i,j in graph.edges():
            if np.random.uniform() < self.p:
                truth = (i,j) in self.g.edges()
                if np.random.uniform() > self.h: truth = not truth
                if truth: add_upvote(graph.edge[i][j], self)
                else:     add_downvote(graph.edge[i][j], self)

        # add nodes that don't yet exist in graph
        new_nodes = [n for n in self.g.nodes() if n not in graph.nodes()]
        for n in new_nodes:
            if np.random.uniform() < self.p:
                if np.random.uniform() > self.h:
                    graph.add_node(n, upvotes=set([self]))
                else:
                    graph.add_node(np.random.randint(1000, 10000), 
                                   upvotes=set([self]))

        # add edges that don't yet exist in graph
        new_edges = [e for e in self.g.edges() if e not in graph.edges()]
        for i,j in new_edges:
            if np.random.uniform() < self.p:
                if np.random.uniform() > self.h:
                    graph.add_edge(i,j, upvotes=set([self]))
                else:
                    graph.add_edge(np.random.randint(1000,10000), 
                                   np.random.randint(1000,10000), 
                                   upvotes=set([self]))

class Site:
    def __init__(self, pop, graph_size, connect_prob):
        # misbelief (m), honesty (h), and participation (p) distro parameters
        h_mean, h_sd = 0.9, 0.3
        m_mean, m_sd = 0.05, 0.1
        p_mean, p_sd = 0.25, 0.8
        # make a random graph to try to approximate
        self.true_graph = get_random_graph(graph_size, connect_prob)
        # graph meant to approximate true_graph
        self.graph = nx.DiGraph()
        # set of users with honesty values following passed distribution
        self.users = [User(self.true_graph, 
                           clamp(np.random.normal(h_mean, h_sd),0.,1.),
                           clamp(np.random.normal(m_mean, m_sd),0.,1.),
                           clamp(np.random.normal(p_mean, p_sd),0.,1.),) 
                      for _ in range(pop)]
        # map from user to estimated 'reliablity' of user
        #self.trust = dict()

    def tick(self, ):
        for u in self.users:
            # SHOULD PROBABLY SHUFFLE...
            u.browse(self.graph)

    def get_user_reputation(self, user):
        # iterate over graph, get idea for how right the user is...
        # could just have numerator of sum of people that seem to be right
        # and agree, denom opposite
        # so if upvotes and thing has lots of upvotes, numerator += len(upvotes)
        # and denom += len(downvotes)...can switch if downvotes look right..
        pass

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
    # add labeled nodes and edges
    for i in range(n):
        for j in range(n):
            if np.random.uniform() < p:
                # choose what kind of edge to make and add it to the graph
                G.add_edge(i, j, relation=get_random_relation())
    # return generated graph
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

def mutate_graph(original_graph, misbelief):
    # mutate a graph (add and remove nodes and edges) according to misbelief
    # might be...overkill.
    graph = original_graph.copy()
    size = len(graph)
    # remove nodes
    for n in range(size):
        if np.random.uniform() < misbelief:
            graph.remove_node(n)
    # add nodes - about as many as removed
    for n in range(size):
        if np.random.uniform() < misbelief:
            # make sure not to conflict with other nodes
            graph.add_node(size+n)
    # remove edges
    for e in graph.edges():
        if np.random.uniform() < misbelief:
            graph.remove_edge(*e)
    # add edges
    for i in graph.nodes():
        for j in graph.nodes():
            if np.random.uniform() < misbelief:
                graph.add_edge(i,j, relation=get_random_relation())
    # return results of mutation
    return graph

def add_upvote(d, user):
    d['upvotes'] = d.get('upvotes', set()) | {user}
def add_downvote(d, user):
    d['downvotes'] = d.get('downvotes', set()) | {user}


if __name__=='__main__':

    # test reading dot file
    #r = nx.read_dot('test.dot')
    #nx.draw(r)
    #plt.show()

    # test writing dot file
    #g = nx.DiGraph()
    #g.add_nodes_from(['node1','node2','node3'])
    #g.node['node1']['type'] = 'is-a'
    #g.add_edges_from([('node1','node2'),
    #                  ('node2','node3')])
    #nx.write_dot(g, 'test_write.dot')
    #nx.draw(g)
    #plt.show()
    

    #g = get_random_graph(20, 0.1)
    #plt.subplot(211)
    #nx.draw(g)
    #g = mutate_graph(g, .1)
    #plt.subplot(212)
    #nx.draw(g)
    #plt.show()

    pop = 10
    size = 20
    connect_prob = 0.3
    s = Site(pop, size, connect_prob)
    s.tick()
    
