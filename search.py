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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    #initialize and push start state on stack
    stack = util.Stack()
    stack.push((problem.getStartState(), []))

    #Empty visited set initialized
    visited = set()

    try:
        while True:
            # Pop a node and action from the stack
            state, actions = stack.pop()

            #if goal state, return state
            if problem.isGoalState(state):
                return actions

            # Mark the state visited
            if state not in visited:
                visited.add(state)

                # iterate through successors of current state
                for successor, action, _ in problem.getSuccessors(state):
                    # Push successors and action
                    stack.push((successor, actions + [action]))
    except IndexError:
        util.raiseNotDefined()

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # The usual try: while true: statement didn't work due to out of bounds errors on the tuples. I use while not queue.isEmpty() instead.
    # Initialize queue with the start state
    queue = util.Queue()
    startState = problem.getStartState()
    queue.push(startState)

    # Initialize a dictionary to track paths
    paths = {startState: []}
    visited = set()

    while not queue.isEmpty():

        state = queue.pop()

        # If state is the goal state, return the path to it
        if problem.isGoalState(state):
            return paths[state]

        # If the current state has not been visited yet, mark as visited
        if state not in visited:
            visited.add(state)

            #iterate through the entire successors list
            # check that all successors have been visited
            # push all successors that have not been visited yet
            for successor, action, _ in problem.getSuccessors(state):
                if successor not in visited and successor not in paths:

                    # Record the path to the successor, it's always current path + next action
                    queue.push(successor)
                    paths[successor] = paths[state] + [action]

    # If no solution is found, return an empty list
    return []
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # Priority queue because the third parameter priority allows necessary functionality a queue won't
    # Functionally speaking, the algorithm works the same way as DFS, with the prioritization factor and queue
    queue = util.PriorityQueue()

    # initial priority is 0
    queue.push((problem.getStartState(), []), 0)
    visited = set()

    try:
        while True:
            state, actions = queue.pop()

            # if state is goal, return the actions (path)
            if problem.isGoalState(state):
                return actions

            # if state hasn't been visited yet, add it to visited list
            if state not in visited:
                visited.add(state)

                # Can use the third param stepCost in for loop now that it's relevant
                for successor, action, stepCost in problem.getSuccessors(state):

                    #update works the same as push, with the added priority as a third param
                    queue.update((successor, actions + [action]), problem.getCostOfActions(actions + [action]))

    except IndexError:
        util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # Same format as above search algo's
    queue = util.PriorityQueue()
    queue.push((problem.getStartState(), []), 0)
    visited = set()

    try:
        while True:

            state, actions = queue.pop()

            if problem.isGoalState(state):
                return actions

            if state not in visited:
                visited.add(state)

                for successor, action, stepCost in problem.getSuccessors(state):

                    # Difference between A* and other searches below.

                    heuristicCost = problem.getCostOfActions(actions + [action])
                    estimatedCost = heuristic(successor, problem)
                    queue.update((successor, actions + [action]), heuristicCost + estimatedCost)

    except IndexError:
        util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
