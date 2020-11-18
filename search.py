# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    nodes = util.Stack()
    visited = []
    #la primera coordenada será la posicion y la segunda los movimientos hechos
    nodes.push((problem.getStartState(), []))
    #mientras todavía queden nodos que mirar
    while not nodes.isEmpty():
        #vamos sacando nodos
        node = nodes.pop()
        state = node[0]
        movements = node[1]

        #si el state es el nodo final terminamos
        if problem.isGoalState(state):
            return movements

        #si todavía no lo hemos visitado, lo expandimos
        if state not in visited:
            visited.append(state)
            #cogemos los sucesores del nodo
            successors = problem.getSuccessors(state)
            for child in successors:
                child_state = child[0]
                child_moves = child[1]
                if child_state not in visited:
                    #si los hijos del nodo no estaban en la lista, los ponemos
                    #con la lista de movimientos actualizada
                    child_moves = movements + [child_moves]
                    nodes.push((child_state, child_moves))


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    """El procedimiento y la justificación del problema es el mismo
    que en DFS, la única diferencia es el tipo de estructura utilizado
    para guardar y sacar los nodos. En el caso del BFS para que se cumpla
    el algoritmo debemos utilizar una Cola dónde el primero que entra es 
    el último que sale"""
    nodes = util.Queue()
    visited = []
    nodes.push((problem.getStartState(), []))

    while not nodes.isEmpty():
        node = nodes.pop()
        state = node[0]
        movements = node[1]

        if problem.isGoalState(state):
            return movements

        if state not in visited:
            visited.append(state)
            successors = problem.getSuccessors(state)
            for child in successors:
                child_state = child[0]
                child_moves = child[1]
                if child_state not in visited:
                    child_moves = movements + [child_moves]
                    nodes.push((child_state, child_moves))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    """Para el algoritmo de coste uniforme debemos utilizar una cola
    de prioridad dónde la prioridad es el último argumento, que corresponde
    al coste de ir de un nodo a otro"""
    nodes = util.PriorityQueue()
    visited =[]
    nodes.push((problem.getStartState(), []), 1)

    while not nodes.isEmpty():
        node = nodes.pop()
        state = node[0]
        movements = node[1]

        if problem.isGoalState(state):
            return movements

        if state not in visited:
            visited.append(state)
            successors = problem.getSuccessors(state)
            for child in successors:
                child_state = child[0]
                child_moves = child[1]
                if child_state not in visited:
                    child_moves = movements + [child_moves]
                    nodes.push((child_state, child_moves), 1)
                    nodes.update(nodes, 1)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #inicializamos nodes como una priority queue
    nodes = util.PriorityQueue()
    #también inicializamos una lista para guardar los nodos visitados
    visited = []
    """introducimos el nodo de inicio en la priority queue, que será de la forma:
    (estado, movimientos), heuristica y el problema general"""
    nodes.update((problem.getStartState(), []),  heuristic(problem.getStartState(), problem))

    """El resto del problema corresponde a un algoritmo similar al
    BFS y DFS con la diferencia que debemos actualizar la cola cada
    vez que ponemos un nodo nuevo en esta"""
    while not nodes.isEmpty():
        node = nodes.pop()
        state = node[0]
        movements = node[1]

        if problem.isGoalState(state):
            return movements

        if state not in visited:
            visited.append(state)
            successors = problem.getSuccessors(state)
            for child in successors:
                child_state = child[0]
                child_moves = child[1]
                if child_state not in visited:
                    child_moves = movements + [child_moves]
                    cost = problem.getCostOfActions(child_moves)
                    nodes.update((child_state, child_moves), cost + heuristic(child_state, problem))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
