import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from random import shuffle

"""
TODO
- Weight votes by reputation
- Make minimal GUI with sliders and stuff...kinda cool if could slide over time
  but definitely not necessary
  to make sliders discrete: http://stackoverflow.com/questions/13656387/can-i-make-matplotlib-sliders-more-discrete
- ALSO NEED TO CHECK RELATION IS RIGHT
- NOTE: strange things seem to happen to voting when lying 
        abound - should make sure each agent can only upvote or downvote?
- use regression to figure out user characteristics?
- use regression or something? ASK
"""


class User:
    def __init__(self, ground_truth_graph, honesty, misbelief, participation):
        self.g = mutate_graph(ground_truth_graph, misbelief)
        # misbelief is the amount the passed graph will be mutated in [0,1]
        # honesty is proportion of truths told in [0,1]
        self.h = honesty
        self.p = participation

    def browse(self, graph):
        # "browse" the passed graph
        # add nodes that don't yet exist in graph
        new_nodes = [n for n in self.g.nodes() if n not in graph.nodes()]
        for n in new_nodes:
            if np.random.uniform() < self.p:
                if np.random.uniform() < self.h:
                    graph.add_node(n, upvotes=set([self]))
                else:
                    graph.add_node(np.random.randint(1000, 10000), 
                                   upvotes=set([self]))

        # add edges that don't yet exist in graph
        new_edges = [e for e in self.g.edges() if e not in graph.edges()]
        for i,j in new_edges:
            if np.random.uniform() < self.p:
                if np.random.uniform() < self.h:
                    graph.add_edge(i,j, upvotes=set([self]))
                else:
                    graph.add_edge(np.random.randint(1000,10000), 
                                   np.random.randint(1000,10000), 
                                   upvotes=set([self]))

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

        


class Site:
    def __init__(self, pop, graph_size, connect_prob):
        # honesty (h), misbelief (m), and participation (p) distro parameters
        h_mean, h_sd = 1., .0001
        m_mean, m_sd = .2, .0001
        p_mean, p_sd = 1., .0001
        # make a random graph to try to approximate
        self.true_graph = get_random_graph(graph_size, connect_prob)
        # graph meant to approximate true_graph
        self.graph = nx.DiGraph()
        # set of users with honesty values following passed distribution
        self.users = [User(self.true_graph, #1., 0., 1.)
                           clamp(np.random.normal(h_mean, h_sd),0.,1.),
                           clamp(np.random.normal(m_mean, m_sd),0.,1.),
                           clamp(np.random.normal(p_mean, p_sd),0.,1.),) 
                      for _ in range(pop)]
        # map from user to estimated 'reliablity' of user
        #self.trust = dict()

    def tick(self, ):
        shuffle(self.users)
        for u in self.users:
            pass
            u.browse(self.graph)

    def run_until_convergence(self, ):
        pass

    def show_difference(self, filt=False):
        # display
        plt.subplot(131)
        nx.draw(self.true_graph)
        plt.subplot(132)
        nx.draw(self.graph)
        plt.subplot(133)
        nx.draw(self.get_filtered_graph())
        plt.show()
        # calculate proportion difference?
        
    def get_filtered_graph(self, ):
        # only keep components with positive trust scores
        """
        g2 = self.graph.copy()
        for n in g2.nodes():
            #print len(get_upvotes(g2.node[n]))
            #print len(get_downvotes(g2.node[n]))
            if len(get_upvotes(g2.node[n])) < len(get_downvotes(g2.node[n])):
                g2.remove_node(n)
        for i,j in g2.edges():
            #print len(get_upvotes(g2.edge[i][j]))
            #print len(get_downvotes(g2.edge[i][j]))
            if len(get_upvotes(g2[i][j])) < len(get_downvotes(g2[i][j])):
                g2.remove_edge(i,j)
        return g2
        """
        T = self.get_trust_scores()
        g2 = self.graph.copy()
        for n in g2.nodes():
            #print len(get_upvotes(g2.node[n]))
            #print len(get_downvotes(g2.node[n]))
            if T[n] <= 0: g2.remove_node(n)
        for i,j in g2.edges():
            #print len(get_upvotes(g2.edge[i][j]))
            #print len(get_downvotes(g2.edge[i][j]))
            if T[(i,j)] <= 0: g2.remove_edge(i,j)
        return g2
        #"""

    def get_user_reputation(self, user):
        """ Calculate fraction of nodes in which user's votes agree 
            with the majority. """
        total = 0
        majority = 0
        for n in self.graph.nodes():
            total += 1
            uv = get_upvotes(self.graph.node[n])
            dv = get_downvotes(self.graph.node[n])
            if n in max(uv, dv, key=len):
                majority += 1
        return float(majority) / total

    def get_trust_scores(self, ):
        """ Get overall trust scores for graph components using user rep. """
        # get user reputation scores
        user_scores = {}
        for u in self.users:
            user_scores[u] = self.get_user_reputation(u)

        # find score for each graph component
        component_scores = {}
        for i,j in self.graph.edges():
            uv = [user_scores[u] for u in get_upvotes(self.graph.edge[i][j])]
            dv = [user_scores[u] for u in get_downvotes(self.graph.edge[i][j])]
            component_scores[(i,j)] = uv - dv
        for n in self.graph.nodes():
            uv = [user_scores[u] for u in get_upvotes(self.graph.node[n])]
            dv = [user_scores[u] for u in get_downvotes(self.graph.node[n])]
            component_scores[n] = uv - dv

        return component_scores


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

def get_upvotes(d):
    return d.get('upvotes', set())
def get_downvotes(d):
    return d.get('downvotes', set())


if __name__=='__main__':

    #g = get_random_graph(20, 0.1)
    #plt.subplot(211)
    #nx.draw(g)
    #g = mutate_graph(g, .1)
    #plt.subplot(212)
    #nx.draw(g)
    #plt.show()

    pop = 10
    size = 5
    connect_prob = 0.2
    s = Site(pop, size, connect_prob)
    for _ in range(100): s.tick()
    s.show_difference()
