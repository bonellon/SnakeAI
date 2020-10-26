import pygame

from Game import Game
from Snake import Snake

red = pygame.Color(255, 0, 0)

class Node:
    # Initialize the class
    def __init__(self, position:(), parent:()):
        self.position = position
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f

    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))


class AStarModel:
    def __init__(self):
        self.path = []
        self.game = None


    def onGameOver(self, score):
        print(score)
        self.game_to_map()

    def convert_path_to_direction(self, step):
        snake_head_x = self.game.snake.head[0]
        snake_head_y = self.game.snake.head[1]

        if snake_head_x == step[0] and snake_head_y > step[1]:
            print("UP")
            return 0

        elif snake_head_x == step[0] and snake_head_y < step[1]:
            print("DOWN")
            return 1

        elif snake_head_x < step[0] and snake_head_y == step[1]:
            print("RIGHT")
            return 3

        elif snake_head_x > step[0] and snake_head_y == step[1]:
            print("LEFT")
            return 2

        else:
            return "ERROR"

    def generatePredictionFromPath(self):
        step = self.path[0]
        self.path.pop(0)
        return self.convert_path_to_direction(step)

    def drawPath(self):
        for node in self.path:
            pygame.draw.rect(self.game.game_window, red,
                                 pygame.Rect(node[0], node[1], self.game.pixelSize, self.game.pixelSize))

        pygame.display.update()
        #pygame.time.wait(1000)

    def generatePrediction(self, game):

        self.game = game
        if self.path != []:
            return self.generatePredictionFromPath()

        map, visual_map = self.game_to_map()

        open = []
        closed = []

        start = Node(game.snake.head, None)
        goal = Node((game.food.x, game.food.y), None)

        open.append(start)

        while len(open) > 0:
            # Sort the open list to get the node with the lowest cost first
            open.sort()
            # Get the node with the lowest cost
            current_node = open.pop(0)
            # Add the current node to the closed list
            closed.append(current_node)

            # Check if we have reached the goal, return the path
            if current_node == goal:
                path = []
                while current_node != start:
                    path.append(current_node.position)
                    current_node = current_node.parent
                # path.append(start)
                # Return reversed path
                reverse_path = path[::-1]
                self.path = path[::-1]

                prediction = self.convert_path_to_direction(reverse_path[0])
                self.drawPath()
                self.path.pop(0)
                return prediction
            # Unzip the current node position
            (x, y) = current_node.position
            # Get neighbors
            neighbors = [(x - game.pixelSize, y), (x + game.pixelSize, y), (x, y - game.pixelSize), (x, y + game.pixelSize)]
            # Loop neighbors
            for next in neighbors:
                # Get value from map
                map_value = map.get(next)
                # Check if the node is a wall
                if (map_value == '~'):
                    continue
                # Create a neighbor node
                neighbor = Node(next, current_node)
                # Check if the neighbor is in the closed list
                if (neighbor in closed):
                    continue
                # Generate heuristics (Manhattan distance)
                neighbor.g = abs(neighbor.position[0] - start.position[0]) + abs(
                    neighbor.position[1] - start.position[1])
                neighbor.h = abs(neighbor.position[0] - goal.position[0]) + abs(
                    neighbor.position[1] - goal.position[1])
                neighbor.f = neighbor.g + neighbor.h
                # Check if neighbor is in open list and if it has a lower f value
                if (self.add_to_open(open, neighbor) == True):
                    # Everything is green, add neighbor to open list
                    open.append(neighbor)
            # Return None, no path is found
        print("CANNOT FIND PATH HELP!!!!")
        return None

    # Check if a neighbor should be added to open list
    def add_to_open(self, open, neighbor):
        for node in open:
            if (neighbor == node and neighbor.f >= node.f):
                return False
        return True

    def game_to_map(self):
        pixels_x = self.game.frame_size_x // self.game.pixelSize
        pixels_y = self.game.frame_size_y // self.game.pixelSize

        map = {}
        visual_map = {}
        food_x = self.game.food.x // self.game.pixelSize
        food_y = self.game.food.y // self.game.pixelSize

        snake_head_x = self.game.snake.head[0] // self.game.pixelSize
        snake_head_y = self.game.snake.head[1] // self.game.pixelSize

        snake_body = [(int(body[0] / self.game.pixelSize), int(body[1] / self.game.pixelSize)) for body in self.game.snake.body]

        for y in range(0, pixels_y):
            line = ""
            for x in range(0, pixels_x):

                #food
                if x == food_x and y == food_y:
                    char = "$"

                #snake
                elif snake_head_x == x and snake_head_y == y:
                    char = "@"

                elif any(body[0] == x and body[1] == y for body in snake_body):
                    char ="~"

                #wall - additional walls around the map. Not implemented yet.

                else:
                    char = "."

                map[x * self.game.pixelSize, y * self.game.pixelSize] = char
                line += char
            visual_map[x,y] = line

        return map, visual_map


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 100

# Window size
frame_size_x = 600
frame_size_y = 300
pixelSize = 10

aStar = AStarModel()
snakeStart = [200,50]

while True:
    print("iter")
    snake = Snake(snakeStart[0], snakeStart[1], [snakeStart, [snakeStart[0]-pixelSize, snakeStart[1]],
                                                 [snakeStart[0]-pixelSize*2, snakeStart[1]]], snakeStart)
    currentGame = Game(frame_size_x, frame_size_y, difficulty, snake, pixelSize)

    while currentGame.snake.alive:
        currentGame.step(aStar, "ASTAR")