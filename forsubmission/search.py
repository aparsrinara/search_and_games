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
import sys
import copy
import itertools

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

    def goalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getResult(self, state, action):
        """
        Given a state and an action, returns resulting state.
        """
        util.raiseNotDefined()

    def getCost(self, state, action):
        """
        Given a state and an action, returns step cost, which is the incremental cost 
        of moving to that successor.
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

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"
    current_state = problem.getStartState()
    frontier = util.Queue()
    d = {}
    explored = set()
    frontier.push(current_state)
    d[current_state] = []
    while frontier.isEmpty() == False:
        if problem.goalTest(current_state):
            return d[current_state]
        current_state = frontier.pop()
        for action in problem.getActions(current_state):
            child = problem.getResult(current_state, action)
            if child not in explored:
                d[child] = d[current_state] + [action]
                frontier.push(child)
        explored.add(current_state)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def iterativeDLS(problem, limit):
    current_state = problem.getStartState()
    s, d = util.Stack(), {}
    explored = set()
    s.push(current_state)
    d[current_state] = []

    if problem.goalTest(current_state):
        return d[current_state]
    while s.isEmpty() == False:
        current_state = s.pop()
        explored.add(current_state)
        if len(d[current_state]) < limit:
            for action in problem.getActions(current_state):
                child = problem.getResult(current_state, action)
                if problem.goalTest(child):
                    return d[current_state] + [action]
                if child not in d:
                    d[child] = d[current_state] + [action] #previous state and action it took to get to child state
                    s.push(child)
    return []


def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.
    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    result = []
    prevNum = 0
    for i in itertools.count(1, 1):
        result = iterativeDLS(problem, i)
        if len(result) != 0:
            return result

    util.raiseNotDefined()

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    initial = problem.getStartState()
    actions = []
    def gN(state,problem,heuristic,actions):
        return heuristic(state,problem) + problem.getCostOfActions(actions)
    poppedFromPQ = []
    frontier = util.PriorityQueue()
    frontier.push(initial, gN(initial,problem,heuristic,actions))
    d = {}
    node = frontier.pop()
    poppedFromPQ.append(node)
    d[node] = actions
    print(node)
    while True: 
        if problem.goalTest(node):
            return d[node]
        else:
          for action in problem.getActions(node):
            child = problem.getResult(node, action)
            if child not in d or gN(child, problem, heuristic, d[node] + [action]) < gN(child, problem, heuristic, d[child]):
                d[child] = d[node] + [action]
                frontier.push(child, gN(child,problem,heuristic,d[child]))
        if frontier.isEmpty() == False:
            node = frontier.pop()
            while node in poppedFromPQ and frontier.isEmpty() == False:
                node = frontier.pop()
            poppedFromPQ.append(node)
        else:
            return []

# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
