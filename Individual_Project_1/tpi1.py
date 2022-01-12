from tree_search import *
from cidades import *

class MyNode(SearchNode):
    def __init__(self,state,parent,cost=0,heuristic=0,arg5=None):
        super().__init__(state,parent)
        self.cost = cost
        self.heuristic = heuristic
        self.eval = None
        self.children = []

class MyTree(SearchTree):
    class solution_tree:
        def __init__(self):
            self.solution_tree.terminals = None
            self.solution_tree.non_terminals = None
            self.solution_tree.path = None
            self.solution_tree.solution = None
            self.solution_tree.cost = -1
            self.solution_tree.nodes = None
            self.used_shortcuts = []

    def __init__(self,problem, strategy='breadth',seed=0): 
        super().__init__(problem,strategy,seed)
        self.solution_tree.__init__(self)
        root = MyNode(self.problem.initial, None, 0, self.problem.domain.heuristic(self.problem.initial, self.problem.goal))
        root.eval = root.cost + root.heuristic
        self.all_nodes = [root]
        self.statesUsed = {}

    def astar_add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key = lambda nodeID: self.all_nodes[nodeID].cost + self.all_nodes[nodeID].heuristic)

    def propagate_eval_upwards(self,node):
        if len(node.children) == 1:
            node.eval = node.children[0].eval
        else:
            for child in node.children:
                if node.eval > child.eval:
                    node.eval = child.eval
        
        if node.parent == None:
            return
        else:
            self.propagate_eval_upwards(self.all_nodes[node.parent])

    def search2(self,atmostonce=False):
        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                self.cost = node.cost
                return self.get_path(node)
            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    newnode = MyNode(newstate, nodeID, node.cost + self.problem.domain.cost(node.state, a), self.problem.domain.heuristic(newstate, self.problem.goal))
                    newnode.eval = round(newnode.cost + newnode.heuristic)
                    if atmostonce and newstate in self.statesUsed:
                        if self.statesUsed[newstate] > newnode.cost:
                            self.all_nodes.append(newnode)
                            lnewnodes.append(len(self.all_nodes) - 1)

                            node.children += [newnode]
                            self.propagate_eval_upwards(node)
                            
                            self.statesUsed[newstate] = newnode.cost
                    else:
                        self.all_nodes.append(newnode)
                        lnewnodes.append(len(self.all_nodes) - 1)

                        node.children += [newnode]
                        self.propagate_eval_upwards(node)

                        self.statesUsed[newstate] = newnode.cost
            self.add_to_open(lnewnodes)
        return None
        

    def repeated_random_depth(self,numattempts=3,atmostonce=False):
        for a in range(numattempts):

            # Default values
            root = MyNode(self.problem.initial, None, 0, self.problem.domain.heuristic(self.problem.initial, self.problem.goal))
            self.all_nodes = [root]
            self.open_nodes = [0]
            self.solution = None
            self.non_terminals = 0

            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem.goal_test(node.state):
                    if self.solution_tree.cost > node.cost or self.solution_tree.cost == -1:
                        self.solution_tree.solution = node
                        self.terminals = len(self.open_nodes) + 1
                        self.solution_tree.terminals = self.terminals
                        self.solution_tree.non_terminals = self.non_terminals
                        self.solution_tree.path = self.get_path(node)
                        self.solution_tree.cost = node.cost
                        self.solution_tree.nodes = self.open_nodes
                    break

                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                    if newstate not in self.get_path(node):
                        newnode = MyNode(newstate, nodeID, node.cost + self.problem.domain.cost(node.state, a),self.problem.domain.heuristic(newstate, self.problem.goal))
                        self.all_nodes.append(newnode)
                        lnewnodes.append(len(self.all_nodes) - 1)
                self.add_to_open(lnewnodes)
        return self.solution_tree.path

    def make_shortcuts(self):
        nodesDict = {}
        solution = self.get_path(self.solution)
        # Save nodes in dict
        for node in self.all_nodes:
            if node != None and node.parent != None:
                child = str(node.state)
                parent = str(self.all_nodes[node.parent].state)
                #print(parent + " -> " + child)
                if parent not in nodesDict:
                    nodesDict[parent] = [child]
                else:
                    nodesDict[parent] += [child]

        # Iterate over the starts
        for s in range(len(solution)):
            # Iterate over the ends
            for e in range(len(solution) - 1,0,-1):
                # If we it the end of the search we stop
                if s >= len(solution):
                    return solution
                
                # If we find a shortcut we use it and we register it
                if solution[s] in nodesDict and solution[e] in nodesDict[solution[s]]:
                    if solution[e] != solution[s + 1]:
                        self.used_shortcuts += [(solution[s], solution[e])]
                    solution = solution[:s+1] + solution[e:]

class MyCities(Cidades):
    def maximum_tree_size(self,depth):   # assuming there is no loop prevention
        uniqueNodes = set()
        numberOfUniqueNodes = 0
        numberOfConnections = 0

        # Add unique nodes to set
        for con in self.connections:
            if con[0] not in uniqueNodes:
                uniqueNodes.add(con[0])
                numberOfUniqueNodes += 1
            if con[1] not in uniqueNodes:
                uniqueNodes.add(con[1])
                numberOfUniqueNodes += 1
            numberOfConnections += 2

        # Get average number of children nodes
        avgChildren = numberOfConnections/numberOfUniqueNodes

        # Return prediction of full tree
        return avgChildren**(depth + 1)/(avgChildren - 1)

        

