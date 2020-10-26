from Game import Game
from Snake import Snake

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


    def onGameOver(self, score):
        print(score)

    def convert_path_to_direction(self, step, game):
        snake_head_x = game.snake.head[0]
        snake_head_y = game.snake.head[1]

        if snake_head_x == step[0] and snake_head_y > step[1]:
            return 9

        elif snake_head_x == step[0] and snake_head_y < step[1]:
            return 1

        elif snake_head_x < step[0] and snake_head_y == step[1]:
            return 3

        elif snake_head_x > step[0] and snake_head_y == step[1]:
            return 2

        else:
            return "ERROR"

    def generatePrediction(self, game):

        map = self.game_to_map(game)

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
                return self.convert_path_to_direction(path[::-1][0], game)
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
        return None

    # Check if a neighbor should be added to open list
    def add_to_open(self, open, neighbor):
        for node in open:
            if (neighbor == node and neighbor.f >= node.f):
                return False
        return True

    def game_to_map(self, game):
        pixels_x = game.frame_size_x // game.pixelSize
        pixels_y = game.frame_size_y // game.pixelSize

        map = {}
        food_x = game.food.x // game.pixelSize
        food_y = game.food.y // game.pixelSize

        snake_head_x = game.snake.head[0] // game.pixelSize
        snake_head_y = game.snake.head[1] // game.pixelSize

        snake_body = [(int(body[0] // game.pixelSize), int(body[1] // game.pixelSize)) for body in game.snake.body]

        for y in range(0, pixels_y):
            line = ""
            for x in range(0, pixels_x):

                #food
                if x == food_x and y == food_y:
                    char = "$"


                #snake
                elif x == snake_head_x and y == snake_head_y:
                    char = "@"

                elif any(body[0] == x and body[1] == y for body in snake_body):
                    char ="~"

                #wall - not implemented
                else:
                    char = "."

                map[x * game.pixelSize, y * game.pixelSize] = char
                line += char

        return map


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

aStar = AStarModel()

while True:
    snake = Snake(100, 50, [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]], [100, 50])
    currentGame = Game(frame_size_x, frame_size_y, difficulty, snake)

    while currentGame.snake.alive:
        currentGame.step(aStar, "ASTAR")