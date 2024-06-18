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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        return successorGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        return self.max_value(gameState, 0, self.depth*gameState.getNumAgents())[0] # Returns the action with the highest value. Since we find the move for Pacman, the agent is 0 and we directly call the max_value function so we get the tuple returned correctly.

    def MiniMax_Search(self, gameState, agent, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose(): # The game is terminal if the depth is 0 or if the game is won or lost.
            return self.evaluationFunction(gameState) # The evaluation function is called to evaluate the state.
        if agent == 0: # If the agent is 0, then it is Pacman and the max_value function is called.
            return self.max_value(gameState, agent, depth)[1] # The max_value function returns a tuple (action, value) and the value is returned.
        else:
            return self.min_value(gameState, agent, depth)[1] # If the agent is not 0, then it is a ghost and the min_value function is called. The min_value function returns a tuple (action, value) and the value is returned.
        
    def max_value(self, gameState, agent, depth):
        v = ("action", -float("inf")) # A tuple (action, value) is created. The value is set to -infinity as described in the pseudocode.
        for action in gameState.getLegalActions(agent): # For each action in the legal actions of the agent.
            possibleAction = (action, self.MiniMax_Search(gameState.generateSuccessor(agent, action), (agent+1)%gameState.getNumAgents(), depth-1)) # The agent is changed to the next agent and the depth is decreased by 1. Uses the MinMax_Search function to find the value of the action since we dont know if the next agent is a ghost or Pacman. We could perform a check to se if it is a ghost or pacman, but better to just call the function.
            v = self.max(possibleAction, v) # The max function is called to evaluate wheter v or the new action has the highest value. The max function returns the tuple with the highest value.
        return v # The tuple with the highest value is returned.

    def min_value(self, gameState, agent, depth):
        v = ("action", float("inf")) # A tuple (action, value) is created. The value is set to infinity as described in the pseudocode.
        for action in gameState.getLegalActions(agent): # For each action in the legal actions of the agent.
            possibleAction = (action, self.MiniMax_Search(gameState.generateSuccessor(agent, action), (agent+1)%gameState.getNumAgents(), depth-1)) # The agent is changed to the next agent and the depth is decreased by 1. Uses the MinMax_Search function to find the value of the action since we dont know if the next agent is a ghost or Pacman. We could perform a check to se if it is a ghost or pacman, but better to just call the function.
            v = self.min(possibleAction, v) # The min function is called to evaluate wheter v or the new action has the lowest value. The min function returns the tuple with the lowest value.
        return v # The tuple with the lowest value is returned.
        
    min = lambda self, x, y: x if x[1] < y[1] else y # A min function for tuples (action, value). Returns the tuple with the lowest valu and which is what the min_value function returns.
    max = lambda self, x, y: x if x[1] > y[1] else y # A max function for tuples (action, value). Returns the tuple with the highest value and which is what the max_value function returns.

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Alpha is initialy set to -infinity and beta is initialy set to infinity.
        # This is done so that the first value we get is always higher than alpha and lower than beta.
        return self.max_value(gameState, 0, self.depth*gameState.getNumAgents(), -float("inf"), float("inf"))[0] # Returns the action with the highest value. Since we find the move for Pacman, the agent is 0 and we directly call the max_value function so we get the tuple returned correctly.

    def alphaBeta_Search(self, gameState, agent, depth, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose(): # The game is terminal if the depth is 0 or if the game is won or lost.
            return self.evaluationFunction(gameState) # The evaluation function is called to evaluate the state.
        if agent == 0: # If the agent is 0, then it is Pacman and the max_value function is called.
            return self.max_value(gameState, agent, depth, alpha, beta)[1] # The max_value function returns a tuple (action, value) and the value is returned.
        else: # If the agent is not 0, then it is a ghost and the min_value function is called. 
            return self.min_value(gameState, agent, depth, alpha, beta)[1] # The min_value function returns a tuple (action, value) and the value is returned.

    def max_value(self, gameState, agent, depth, alpha, beta):
        v = ("action", -float("inf")) # A tuple (action, value) is created. The value is set to -infinity as described in the pseudocode.
        for action in gameState.getLegalActions(agent): # For each action in the legal actions of the agent.
            possibleAction = (action, self.alphaBeta_Search(gameState.generateSuccessor(agent, action), (agent+1)%gameState.getNumAgents(), depth-1, alpha, beta)) # The agent is changed to the next agent and the depth is decreased by 1. Uses the alphaBeta_Search function to find the value of the action since we dont know if the next agent is a ghost or Pacman. We could perform a check to se if it is a ghost or pacman, but better to just call the function.
            if possibleAction[1] > v[1]: # If the value of the new action is higher than the value of v.
                v = possibleAction # The new action is set to v.
                alpha = max(alpha, v[1]) # The alpha value is set to the highest value between alpha and the value of v.
            if v[1] > beta: # If the value of v is higher than the value of beta.
                return v # We dont have to check the rest of the tree, so we prune the rest of the tree and return v
        return v # The tuple with the highest value is returned. We had to check the whole tree, so we return v.

    def min_value(self, gameState, agent, depth, alpha, beta):
        v = ("action", float("inf")) # A tuple (action, value) is created. The value is set to infinity as described in the pseudocode.
        for action in gameState.getLegalActions(agent): # For each action in the legal actions of the agent.
            possibleAction = (action, self.alphaBeta_Search(gameState.generateSuccessor(agent, action), (agent+1)%gameState.getNumAgents(), depth-1, alpha, beta)) # The agent is changed to the next agent and the depth is decreased by 1. Uses the alphaBeta_Search function to find the value of the action since we dont know if the next agent is a ghost or Pacman. We could perform a check to se if it is a ghost or pacman, but better to just call the function.
            if possibleAction[1] < v[1]: # If the value of the new action is lower than the value of v.
                v = possibleAction # The new action is set to v.
                beta = min(beta, v[1]) # The beta value is set to the lowest value between beta and the value of v.
            if v[1] < alpha: # If the value of v is lower than the value of alpha.
                return v # We dont have to check the rest of the tree, so we prune the rest of the tree and return v
        return v # The tuple with the lowest value is returned. We had to check the whole tree, so we return v.

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
