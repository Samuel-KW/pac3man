# multiAgents.py
# --------------
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


from pacman import GameState
from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"
        print("Action: ", legalMoves[chosenIndex],
              "\tScore: ", scores[chosenIndex])
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """

        "*** YOUR CODE HERE ***"

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        # Check if the action is to stop
        if action == "Stop":
          # Return smallest value if the action is to stop
          return -float("inf")

        # Return smallest value if any ghost is going to touch pacman
        for ghost in newGhostStates:
          ghost_pos = ghost.getPosition()
          current_pos = currentGameState.getPacmanPosition()

          touching_next = ghost_pos[0] == newPos[0] and ghost_pos[1] == newPos[1]
          touching_current = ghost_pos[0] == current_pos[0] and ghost_pos[1] == current_pos[1]

          if (touching_next or touching_current) and ghost.scaredTimer == 0:
            return -float("inf")

        # Get Pacman's position as list [x, y]
        pacman_position = list(successorGameState.getPacmanPosition())

        # Get all the food positions
        food_positions = currentGameState.getFood().asList()

        # Get the closest food to Pacman
        closest_food = min(
            food_positions, key=lambda pos: manhattanDistance(pacman_position, pos))
        closest_food_dist = manhattanDistance(pacman_position, closest_food)

        # Get the closest ghost to Pacman
        closest_ghost = min(newGhostStates, key=lambda ghost: manhattanDistance(
            pacman_position, ghost.getPosition()))
        closest_ghost_dist = manhattanDistance(
            pacman_position, closest_ghost.getPosition())

        # Collect powerup if both ghost and powerup are nearby
        closest_powerup = min(successorGameState.getCapsules(
        ), key=lambda pos: manhattanDistance(pacman_position, pos))
        closest_powerup_dist = manhattanDistance(
            pacman_position, closest_powerup)
        if closest_ghost.scaredTimer == 0 and closest_powerup_dist < 5 and closest_ghost_dist < 5:
          return -closest_powerup_dist

        # If the ghost is scared
        if closest_ghost.scaredTimer > 20:

          # Chase nearby ghosts
          if closest_ghost_dist < 3:
            return -100

          # Chase nearby foods
          return -100

        # Return the calculated score
        return -closest_food_dist


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def minimax(agent: int, depth: int, gameState):

          # Base case: End if we reached the end of the game
          if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

          # Get all legal actions for the agent
          actions = gameState.getLegalActions(agent)

          # Recursive case: Handle the current agent
          if agent == 0: # Handle first agent (pacman)

            # Get the maximum utility
            maximum = minimax(
                1, depth, gameState.generateSuccessor(agent, actions.pop()))
            for action in actions:
              utility = minimax(
                  1, depth, gameState.generateSuccessor(agent, action))
              if utility > maximum:
                maximum = utility

            return maximum

          else: # Handle ghost agents
            next_agent = agent + 1

            # Check if we reached the end of the agents
            if next_agent == gameState.getNumAgents():
              next_agent = 0
              depth += 1

            # Get the minimum utility
            minimum = minimax(
                next_agent, depth, gameState.generateSuccessor(agent, actions.pop()))
            for action in actions:
              utility = minimax(next_agent, depth,
                                gameState.generateSuccessor(agent, action))
              if utility < minimum:
                minimum = utility

            return minimum

        # Return the best action
        return max(gameState.getLegalActions(0), key=lambda agent_state: minimax(1, 0, gameState.generateSuccessor(0, agent_state)))


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning.
    """

    def maximize(self, state: GameState, agent: int, depth: int, alpha: float, beta: float):
      pass

    def minimize(self, state: GameState, agent: int, depth: int, alpha: float, beta: float):
      pass

    def getAction(self, gameState: GameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
          with alpha-beta pruning.
        """

        def minimax(agent: int, depth: int, state: GameState, alpha: float, beta: float):

            # Base case: End if we reached the end of the game or max depth
            if depth == self.depth or gameState.isLose() or state.isWin():
                return self.evaluationFunction(state)

            # Get all legal actions for the agent
            actions = state.getLegalActions(agent)

            # Recursive case: Handle the current agent
            if agent == 0: # Pacman (Maximizing player)

                max_value = float("-inf")
                for action in actions:
                    successor = state.generateSuccessor(agent, action)
                    max_value = max(max_value, minimax(1, depth, successor, alpha, beta))

                    if max_value > beta:
                        return max_value  # Prune

                    alpha = max(alpha, max_value)

                return max_value

            else: # Ghosts (Minimizing players)

                min_value = float("inf")
                next_agent = agent + 1

                # Check if we cycle back to Pacman
                if next_agent == state.getNumAgents():
                    next_agent = 0
                    depth += 1

                for action in actions:
                    successor = state.generateSuccessor(agent, action)
                    min_value = min(min_value, minimax(next_agent, depth, successor, alpha, beta))

                    if min_value < alpha:
                        return min_value  # Prune

                    beta = min(beta, min_value)

                return min_value

        # Initialize best value
        best_value = float("-inf")
        best_action = None

        # Initialize alpha and beta
        alpha, beta = float("-inf"), float("inf")

        # Get the best action
        for action in gameState.getLegalActions(0):
            value = minimax(1, 0, gameState.generateSuccessor(0, action), alpha, beta)

            if value > best_value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)

        return best_action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        # Maximize player action
        def maximize(state: GameState, depth: int):
          value = float("-inf")

          for action in state.getLegalActions(0):
            successor = state.generateSuccessor(0, action)
            prediction = predict(successor, 1, depth)
            if prediction > value:
                value = prediction
 
          return value
        
        # Predict expected ghost actions
        def predict(state: GameState, agent: int, depth: int):
          value = 0
          total = state.getNumAgents() - 1

          # Get all legal actions
          for action in state.getLegalActions(agent):
            successor = state.generateSuccessor(agent, action)
            value += select(successor, 0, depth + 1) if agent == total else select(successor, agent + 1, depth)

          # Return the expected cost
          return value / len(gameState.getLegalActions(agent))
        
        # Expectimax selection function
        def select(state: GameState, agent: int, depth: int):
          if depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

          # Handle the current agent
          return maximize(state, depth) if agent == 0 else predict(state, agent, depth)

        # Return the best action
        value = float("-inf")
        decision = Directions.STOP

        for action in gameState.getLegalActions(0):
          successor = gameState.generateSuccessor(0, action)
          prediction = select(successor, 1, 0)
          if prediction > value:
            value = prediction
            decision = action

        return decision


def betterEvaluationFunction(currentGameState: GameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Eat scared ghosts, avoid angry ghosts, eat nearby foods.
    """

    # Useful state variables
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()

    pos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()

    # Higher score for avoiding ghosts or eating ghosts
    for ghost in ghosts:
        
        # Get the distance to the ghost
        distance = manhattanDistance(pos, ghost.getPosition())

        if distance > 0:
            
            # Attempt to eat nearby scared ghosts
            if ghost.scaredTimer > 0 and distance < 10:
                score += 300 / distance

            # Attempt to avoid nearby angry ghosts
            elif distance < 3:  
                score += -1 / distance
        else:

          # Don't die
          return float("-inf")

    distances = [manhattanDistance(pos, food) for food in food]

    # Higher score for finding food areas
    # for distance in distances:
    #     score += 0.1 / distance
        
    # Higher score for getting closer to single foods
    if len(distances) > 0:
      score += 2 / min(distances)

    return score


# Abbreviation
better = betterEvaluationFunction
