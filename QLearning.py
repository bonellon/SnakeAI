import numpy as np
from collections import defaultdict
import pickle
from time import time

from Game import Game
from Snake import Snake


class QLearningModel:

    def __init__(self):
        self.rewardAlive = -1
        self.rewardKill = -10000
        self.rewardScore = 50000000

        # learningRate
        self.alpha = 0.00001
        # ZerfallsRate
        self.alphaD = 0.999

        # discount factor
        self.gamma = 0.9


        # randomness
        self.e = 0.5
        self.ed = 1.3
        self.emin = 0.0001

        try:
            with open("Q-distance.pickle", "rb") as file:
                self.Q = defaultdict(lambda: [0, 0, 0, 0], pickle.load(file))
        except:
            self.Q = defaultdict(lambda: [0, 0, 0, 0])
            # UP LEFT DOWN RIGHT
            print("NEW Q")

        self.lastMoves = ""

        self.oldState = None
        self.oldAction = None
        self.gameCounter = 0
        self.gameScores = []
        self.start = 0
        self.end = 0

    def generatePrediction(self, state):

        estReward = self.Q[state]
        prevReward = self.Q[self.oldState]

        index = 0
        if self.oldAction == 'U':
            index = 0
        if self.oldAction == 'L':
            index = 1
        if self.oldAction == 'D':
            index = 2
        if self.oldAction == 'R':
            index = 3

        reward = (-10) / 50
        prevReward[index] = (1 - self.alpha) * prevReward[index] + \
                            self.alpha * (reward + self.gamma * max(estReward))

        self.Q[self.oldState] = prevReward

        self.oldState = state
        basedOnQ = np.random.choice([True, False], p=[1 - self.e, self.e])

        if basedOnQ == False:
            choice = np.random.choice(['U', 'L', 'D', 'R'], p=[0.25, 0.25, 0.25, 0.25])
            self.oldAction = choice
            return choice
        else:
            if estReward[0] > estReward[1] and estReward[0] > estReward[2] and estReward[0] > estReward[3]:
                self.oldAction = 'U'
                return 0
            if estReward[1] > estReward[0] and estReward[1] > estReward[2] and estReward[1] > estReward[3]:
                self.oldAction = 'L'
                return 3
            if estReward[2] > estReward[0] and estReward[2] > estReward[1] and estReward[2] > estReward[3]:
                self.oldAction = 'D'
                return 2
            if estReward[3] > estReward[0] and estReward[3] > estReward[1] and estReward[3] > estReward[2]:
                self.oldAction = 'R'
                return 1
            else:
                choice = np.random.choice(['U', 'L', 'D', 'R'], p=[0.25, 0.25, 0.25, 0.25])
                self.oldAction = choice
                return choice

    def onGameOver(self, score):
        self.gameScores.append(score)

        # update Q of previous state (state which lead to gameOver)
        prevReward = self.Q[self.oldState]

        if self.oldAction is None:
            index = 0
        if self.oldAction == 'U':
            index = 0
        if self.oldAction == 'L':
            index = 1
        if self.oldAction == 'D':
            index = 2
        if self.oldAction == 'R':
            index = 3

        prevReward[index] = (1 - self.alpha) * prevReward[index] + self.alpha * self.rewardKill

        self.Q[self.oldState] = prevReward

        self.oldState = None
        self.oldAction = None

        # save Q as pickle
        if self.gameCounter % 200 == 0:
            with open("Q-distance.pickle", "wb") as file:
                pickle.dump(dict(self.Q), file)
            print("+++++++++ Pickle saved +++++++++")

        # show some stats
        if self.gameCounter % 100 == 1:
            self.end = time()
            timeD = self.end - self.start
            print(str(self.gameCounter) + " : " + "\t" + 'meanScore: ' + str(
                np.mean(self.gameScores[-100:])) + "| HighScore: " + str(
                np.max(self.gameScores)) + "| time for 10 games: " + str(round(timeD * 10) / 100))
            self.start = time()

        # print coeffients
        if self.gameCounter % 100 == 0:
            print("alpha:", self.alpha)
            print("e:", self.e)
            print("gamma:", self.gamma)

        # decrease alpha / e per 100 moves
        if self.gameCounter % 100 == 0:
            self.alpha = self.alpha * self.alphaD
            if self.e > self.emin:
                self.e = self.e / self.ed

        self.gameCounter += 1

    def onScore(self, state):
        estReward = self.Q[state]

        prevReward = self.Q[self.oldState]

        if self.oldAction == 'U':
            index = 0
        if self.oldAction == 'L':
            index = 1
        if self.oldAction == 'D':
            index = 2
        if self.oldAction == 'R':
            index = 3

        prevReward[index] = (1 - self.alpha) * prevReward[index] + \
                            self.alpha * (self.rewardScore + self.gamma * max(estReward))

        self.Q[self.oldState] = prevReward


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 50

# Window size
frame_size_x = 720
frame_size_y = 480

qLearn = QLearningModel()

while True:
    snake = Snake(100, 50, [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]], [100, 50])
    game = Game(frame_size_x, frame_size_y, difficulty, snake)
    while game.snake.alive:
        game.step(qLearn, "QLearning")
