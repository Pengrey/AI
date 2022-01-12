# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  InteligÃªncia Artificial, 2014-2019

from abc import ABC, abstractmethod
from typing import Callable

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent,cost=0,heuristic=0,pre_action=None): 
        self.state = state
        self.parent = parent
        self.depth = 0 if parent is None else parent.depth+1
        self.cost = cost
        self.heuristic = heuristic
        self.pre_action = pre_action
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

    def in_parent(self, state, equals):
        if self.parent is None:
            return False
        return True if equals(self.parent.state, state) else self.parent.in_parent(state, equals)

    def pre_actions(self):
        return (self.parent.pre_actions() if self.parent else []) + ([self.pre_action] if self.pre_action else [])

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem,strategy='breadth',node_equal: Callable = lambda x,y: x==y): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 0
        self.non_terminals = 0
        self.avg_branching = 0
        self.highest_cost_nodes = [root]
        self.average_depth = 0
        self.plan = []
        self.node_equal = node_equal

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self, node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self, limit=None):
        all_depth = [0]
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                self.avg_branching = round((self.non_terminals + self.terminals - 1)/(self.non_terminals), 2)
                self.average_depth = sum(all_depth)/len(all_depth)
                self.plan = self.solution.pre_actions()
                return self.get_path(node)

            self.non_terminals = self.non_terminals + 1

            lnewnodes = []
            if limit is not None and node.depth >= limit:
                continue

            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if not node.in_parent(newstate, self.node_equal):
                    newnode = SearchNode(newstate,node,
                        node.cost+self.problem.domain.cost(node.state,a),
                        self.problem.domain.heuristic(newstate,self.problem.goal),
                        a)
                    lnewnodes.append(newnode)
                    # Highest cost nodes
                    if len(self.highest_cost_nodes)==0 or newnode.cost > self.highest_cost_nodes[0].cost:
                        self.highest_cost_nodes = [newnode]
                    elif newnode.cost == self.highest_cost_nodes[0].cost:
                        self.highest_cost_nodes.append(newnode)
                    # Average node depth
                    all_depth.append(newnode.depth)

            self.add_to_open(lnewnodes)
        return None

    # numero de transicoes desde o estado inicial ate o objetivo
    @property
    def length(self):
        return self.solution.depth if self.solution is not None else None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda x: x.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda x: x.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda x: x.cost + x.heuristic)

    @property
    def cost(self):
        return self.solution.cost