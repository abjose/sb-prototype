import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from random import shuffle

"""
TODO
- ALSO NEED TO CHECK RELATION IS RIGHT
- use regression to figure out user characteristics?
- use regression or something? ASK
- print user rep vs. honesty, etc. to make sure makes sense
- maybe show nodes/edges colored based on how trusted they are?
- auto-delete graph components with very low scores? (not as filtering step)
"""


class User:
    def __init__(self, ground_truth_graph, honesty, misbelief, participation):
        self.g = mutate_graph(ground_truth_graph, misbelief)
        # misbelief is the amount the passed graph will be mutated in [0,1]
        # honesty is proportion of truths told in [0,1]
        self.h = honesty
        self.m = misbelief # just in case, don't actually need to store
        self.p = participation

    def browse(self, graph):
        """ 'Browse' the passed graph """
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
                # remove previous vote
                del_upvote(graph.node[n], self)
                del_downvote(graph.node[n], self)
                # add new vote
                if truth: add_upvote(graph.node[n], self)
                else:     add_downvote(graph.node[n], self)

        # vote on existing edges
        for i,j in graph.edges():
            if np.random.uniform() < self.p:
                truth = (i,j) in self.g.edges()
                if np.random.uniform() > self.h: truth = not truth
                # remove previous vote
                del_upvote(graph[i][j], self)
                del_downvote(graph[i][j], self)
                # add new vote
                if truth: add_upvote(graph.edge[i][j], self)
                else:     add_downvote(graph.edge[i][j], self)



class Site:
    def __init__(self, pop, graph_size, connect_prob):
        # honesty (h), misbelief (m), and participation (p) distro parameters
        h_mean, h_sd = .7, .2
        m_mean, m_sd = .2, .2
        p_mean, p_sd = .4, .2
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
        # calculate proportion difference
        print self.get_accuracy()

    def test_draw(self, ax1, ax2, ax3):
        # probably a better way to do this
        nx.draw_networkx(self.true_graph, ax=ax1)
        nx.draw_networkx(self.graph, ax=ax2)
        nx.draw_networkx(self.get_filtered_graph(), ax=ax3)
        ax1.axes.get_xaxis().set_ticks([])
        ax1.axes.get_yaxis().set_ticks([])
        ax2.axes.get_xaxis().set_ticks([])
        ax2.axes.get_yaxis().set_ticks([])
        ax3.axes.get_xaxis().set_ticks([])
        ax3.axes.get_yaxis().set_ticks([])
        print self.get_accuracy()
        
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
            print len(get_upvotes(g2.node[n]))
            print len(get_downvotes(g2.node[n]))
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
        majority = 0
        for n in self.graph.nodes():
            uv = get_upvotes(self.graph.node[n])
            dv = get_downvotes(self.graph.node[n])
            if user in max(uv, dv, key=len):
                majority += 1

        return float(majority) / len(self.graph)

    def get_trust_scores(self, ):
        """ Get overall trust scores for graph components using user rep. """
        # get user reputation scores
        user_scores = {}
        for u in self.users:
            user_scores[u] = self.get_user_reputation(u)

        sorted_users = sorted(self.users, key=lambda u: user_scores[u], 
                              reverse=True)
        # print out user stats to see if reputation is useful...
        #for u in sorted_users:
        #    print user_scores[u]
        #print 'reputation:\t', float(majority) / len(self.graph)
        #print 'honesty:\t',     user.h
        #print 'misbelief:\t',   user.m
        #print 'participatn:\t', user.p
        print 

        # find score for each graph component
        component_scores = {}
        for i,j in self.graph.edges():
            uv = [user_scores[u] for u in get_upvotes(self.graph.edge[i][j])]
            dv = [user_scores[u] for u in get_downvotes(self.graph.edge[i][j])]
            #print sum(uv)
            #print sum(dv)
            component_scores[(i,j)] = sum(uv) - sum(dv)
            #print component_scores[(i,j)]
        for n in self.graph.nodes():
            uv = [user_scores[u] for u in get_upvotes(self.graph.node[n])]
            dv = [user_scores[u] for u in get_downvotes(self.graph.node[n])]
            component_scores[n] = sum(uv) - sum(dv)

        return component_scores

    def get_accuracy(self, ):
        """ Determine the % accuracy of generated graph to ground truth. """
        # NEED TO ALSO GO IN REVERSE DIRECTION! Like count nodes in truth but
        # not in graph
        hits = 0
        total = 0
        g2 = self.get_filtered_graph().copy()
        # iterate over every node and edge in self.graph
        for n in self.true_graph.nodes():
            if n in g2.nodes(): hits += 1
            total += 1
        for e in self.true_graph.edges():
            if e in g2.edges(): hits += 1
            total += 1
        return float(hits) / total



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

def del_upvote(d, user):
    d['upvotes'] = d.get('upvotes', set()) - {user}
def del_downvote(d, user):
    d['downvotes'] = d.get('downvotes', set()) - {user}

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

    pop = 20
    size = 5
    connect_prob = 0.2
    s = Site(pop, size, connect_prob)
    for _ in range(5000): s.tick()
    s.show_difference()
