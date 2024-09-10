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


def tinyMazeSearch(problem: SearchProblem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.
    """
    
    # Keep track of visited nodes
    visited = set()

    # Store states to explore
    stack = util.Stack()
    stack.push((problem.getStartState(), []))

    while stack:

        # Get the top state and action in the stack
        state, actions = stack.pop()

        # Return if we have reached the goal
        if problem.isGoalState(state):
            return actions

        # Check unvisited states
        if state not in visited:
            visited.add(state)

            # Add successors and actions to the stack
            for successor, action, _ in problem.getSuccessors(state):
                if successor not in visited:
                    new_actions = actions + [action]
                    stack.push((successor, new_actions))

    # No solution found
    return []

def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """

    # Keep track of visited nodes
    visited = set()
    
    # Store states to explore
    queue = util.Queue()
    queue.push((problem.getStartState(), []))

    while not queue.isEmpty():

        # Get the next state and path
        state, actions = queue.pop()

        # Skip if state has been visited
        if state in visited: continue  

        # Mark the state as visited
        visited.add(state)  

        # Return if we have reached the goal
        if problem.isGoalState(state):
            return actions  

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:

                # Push the successor and the updated path to the queue
                queue.push((successor, actions + [action]))

    # No solution found
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
