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


from util import manhattanDistance
from game import Directions
import random, util

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
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if successorGameState.isWin():
            return float("inf")
        if successorGameState.isLose():
            return -float("inf")
        foodLst = newFood.asList()
        value = 0
        foodNear = []
        for food in foodLst:
          foodNear += [manhattanDistance(newPos, food)]
        ghostLoc= []
        for ghost in newGhostStates:
             ghostLoc = [manhattanDistance(ghost.getPosition(), newPos)]
        # if len(newFood.asList()) == 0:
        #     return float("inf")
        value += min(ghostLoc) + successorGameState.getScore()
        if len(currentGameState.getFood().asList()) > len(successorGameState.getFood().asList()):
            value += 10
        if currentGameState.getScore() > 0:
            value += 20
        value -= min(foodNear)
        return value

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
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 7)
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
        bestScore, bestMove=self.minimax(gameState, self.depth, self.index)
        
        return bestMove

  
    def minimax(self, gameState, depth, agent):
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState), ""
      allGameScores = []
      if agent == 0:
        for action in gameState.getLegalActions(agent):
          allGameScores.append(self.minimax(gameState.generateSuccessor(agent, action), depth, agent+1))
        value = max(allGameScores)
        index = 0
        for score in allGameScores:
          if score == value:
            break
          index = index + 1
        return value, gameState.getLegalActions(agent)[index]
      else:
        if agent < gameState.getNumAgents() - 1:
          for action in gameState.getLegalActions(agent):
            allGameScores.append(self.minimax(gameState.generateSuccessor(agent, action), depth, agent+1))
        else:
          for action in gameState.getLegalActions(agent):
            allGameScores.append(self.minimax(gameState.generateSuccessor(agent, action), depth-1, 0)[0])
        value = min(allGameScores)
        index = 0
        for score in allGameScores:
          if score == value:
            break
          index = index + 1
        return value, gameState.getLegalActions(agent)[index]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState, self.depth, self.index)[1]

    def expectimax(self, gameState, depth, agent):
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState), ""
      allGameScores = []
      if agent == 0:
        for action in gameState.getLegalActions(agent):
          allGameScores.append(self.expectimax(gameState.generateSuccessor(agent, action), depth, agent+1)[0])
        value = max(allGameScores)
        index = 0
        for score in allGameScores:
          if score == value:
            break
          index = index + 1
        return value, gameState.getLegalActions(agent)[index]
      else:
        value = 0
        if agent < gameState.getNumAgents() - 1:
          for action in gameState.getLegalActions(agent):
            allGameScores = self.expectimax(gameState.generateSuccessor(agent, action), depth, agent+1)[0]
            value = value + float(allGameScores) / float(len(gameState.getLegalActions(agent)))
            bestAction = action
        else:
          for action in gameState.getLegalActions(agent):
            allGameScores = self.expectimax(gameState.generateSuccessor(agent, action), depth-1, 0)[0]
            value = value + float(allGameScores) / float(len(gameState.getLegalActions(agent)))
            bestAction = action   
        return value, bestAction


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: <write something here so we know what you did>
      ghostDist: This pacman loses points for letting the ghosts get too close, I tried a
      numbers to see what gave the best results and 2 as a ghost distance limit worked best.

      I also subtracted the minimum distance of the closest food becuase as to incentivize
      it to go closer not farther away from food. 
      I also subtracted the length of the food list, so having fewer food dots left results
      in a better prioritization value of the state. 

      I increased value for having a higher score so it would prioritize those states more,
      since we are trying to achieve 1000+ average score. 

      If the current state is Win then I used max value to prioritize this state highly.
      If it was a lose state, I used min value to make it NOT prioritize this state. 

      There is also a penalty for not using the pellets in this game as well becuase you want 
      pacman to go and use the pellets and eat the ghost. 

      Other than that I used various linear combinations of these values to see what would
      return the optimal results for my goal
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return -float("inf")
    foodLst = newFood.asList()
    value = 0
    foodNear = []
    for food in foodLst:
      foodNear += [manhattanDistance(newPos, food)]
    ghostLoc= []
    ghostDist = 0
    for ghost in newGhostStates:
         ghostDist = manhattanDistance(ghost.getPosition(), newPos)
         ghostLoc.append(ghostDist)
         if ghostDist < 2:
          value += 1000000
    value -= 3*min(ghostLoc)
    if len(newFood.asList()) == 0:
        return float("inf")
    if len(newFood.asList()) > 0:
        value -= 4*(len(newFood.asList()))
    if currentGameState.getScore() > 0:
        value += 2*currentGameState.getScore()
    if currentGameState.getCapsules() > 0:
        value -= 3*len(currentGameState.getCapsules())
    value -= min(foodNear)
    return value

# Abbreviation
better = betterEvaluationFunction

