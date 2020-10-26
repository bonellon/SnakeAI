import pygame, sys, time, random
import math
from Snake import Snake
from Food import Food

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
magenta = pygame.Color(255, 0, 255)

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake')

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


class Game:
    def __init__(self, x, y, difficulty, snake):
        self.frame_size_x = x
        self.frame_size_y = y
        self.pixelSize = 10
        self.score = 0
        self.difficulty = difficulty
        self.snake = snake
        self.food = Food(random.randrange(1, (self.frame_size_x // self.pixelSize)) * self.pixelSize,
                         random.randrange(1, (self.frame_size_y // self.pixelSize)) * self.pixelSize)

        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.frame_size_x / 10, 15)
        else:
            score_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 1.25)
        self.game_window.blit(score_surface, score_rect)

    def game_over(self):
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 4)
        self.game_window.fill(black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.show_score(0, red, 'times', 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def collision_food(self):
        return self.snake.head[0] == self.food.x and self.snake.head[1] == self.food.y

    def collision_boundaries(self, snake_head):
        if snake_head[0] < 0 or snake_head[0] > self.frame_size_x - self.pixelSize:
            return True
        if snake_head[1] < 0 or snake_head[1] > self.frame_size_y - self.pixelSize:
            return True
        return False

    def collision_snake(self, snake_head):
        for block in self.snake.body[1:]:
            if snake_head[0] == block[0] and snake_head[1] == block[1]:
                return True
        return False

    def get_wall_distances(self):
        distanceLeft = self.snake.head[0]
        distanceTop = self.snake.head[1]
        distanceRight = self.frame_size_x - self.pixelSize - self.snake.head[0]
        distanceBottom = self.frame_size_y - self.pixelSize - self.snake.head[1]
        return distanceLeft, distanceTop, distanceRight, distanceBottom

    def get_apple_position(self):
        relativeFoodPostion = [0, 0, 0, 0, 0, 0]

        if (self.food.x - self.snake.x) > 0:  # foodRight
            relativeFoodPostion[0] = 1
        if (self.food.x - self.snake.x) < 0:  # foodLeft
            relativeFoodPostion[1] = 1
        if self.food.x - self.snake.x == 0:  # foodXMiddle
            relativeFoodPostion[2] = 1

        if (self.food.y - self.snake.y) > 0:  # foodDown
            relativeFoodPostion[3] = 1
        if (self.food.y - self.snake.y) < 0:  # foodTop
            relativeFoodPostion[4] = 1
        if self.food.y - self.snake.y == 0:  # foodYMiddle
            relativeFoodPostion[5] = 1

        rFP = ""  # als String concatenated
        for x in relativeFoodPostion:
            rFP += str(x)
        return rFP

    def get_apple_distance(self):
        return abs(self.snake.head[0] - self.food.x) + abs(self.snake.head[1] - self.food.y)

    def get_apple_angle(self):
        return math.degrees(math.atan2(self.snake.y - self.food.y, self.snake.x - self.food.x))

    def get_blocked_directions(self):
        leftBlocked = self.collision_boundaries(
            [self.snake.head[0] - self.pixelSize, self.snake.head[1]]) or self.collision_snake(
            [self.snake.head[0] - self.pixelSize, self.snake.head[1]])
        topBlocked = self.collision_boundaries(
            [self.snake.head[0], self.snake.head[1] - self.pixelSize]) or self.collision_snake(
            [self.snake.head[0], self.snake.head[1] - self.pixelSize])
        rightBlocked = self.collision_boundaries(
            [self.snake.head[0] + self.pixelSize, self.snake.head[1]]) or self.collision_snake(
            [self.snake.head[0] + self.pixelSize, self.snake.head[1]])
        bottomBlocked = self.collision_boundaries(
            [self.snake.head[0], self.snake.head[1] + self.pixelSize]) or self.collision_snake(
            [self.snake.head[0], self.snake.head[1] + self.pixelSize])

        blockedPositions = int(leftBlocked is True), int(topBlocked is True), int(rightBlocked is True) \
            , int(bottomBlocked is True)

        sD = ""
        for x in blockedPositions:
            sD += str(x)
        return sD

    def get_distance_snake(self):
        leftDistance = 1
        for i in range(self.pixelSize, self.frame_size_x + self.pixelSize, self.pixelSize):
            leftBlocked = self.collision_snake([self.snake.head[0] - i, self.snake.head[1]])
            if leftBlocked:
                break
            leftDistance += 1
            if self.collision_boundaries([self.snake.head[0] - i, self.snake.head[1]]):
                leftDistance = 0
                break

        rightDistance = 1
        for i in range(self.pixelSize, self.frame_size_x + self.pixelSize, self.pixelSize):
            rightBlocked = self.collision_snake([self.snake.head[0] + i, self.snake.head[1]])
            if rightBlocked:
                break
            rightDistance += 1
            if self.collision_boundaries([self.snake.head[0] + i, self.snake.head[1]]):
                rightDistance = 0
                break

        topDistance = 1
        for i in range(self.pixelSize, self.frame_size_y + self.pixelSize, self.pixelSize):
            topBlocked = self.collision_snake([self.snake.head[0], self.snake.head[1] - i])
            if topBlocked:
                break
            topDistance += 1
            if self.collision_boundaries([self.snake.head[0], self.snake.head[1] - i]):
                topDistance = 0
                break

        bottomDistance = 1
        for i in range(self.pixelSize, self.frame_size_y + self.pixelSize, self.pixelSize):
            bottomBlocked = self.collision_snake([self.snake.head[0], self.snake.head[1] + i])
            if bottomBlocked:
                break
            bottomDistance += 1
            if self.collision_boundaries([self.snake.head[0], self.snake.head[1] + i]):
                bottomDistance = 0
                break

        return str(leftDistance) + '_' + str(rightDistance) + '_' + str(topDistance) + '_' + str(bottomDistance)

    def getObservations(self):

        wallDistance = self.get_wall_distances()
        appleDistance = self.get_apple_distance()
        appleAngle = self.get_apple_angle()
        blockedDirections = self.get_blocked_directions()

        return wallDistance[0], wallDistance[1], wallDistance[2], wallDistance[3], appleDistance, appleAngle, \
               blockedDirections[0], blockedDirections[1], blockedDirections[2], blockedDirections[3]

    def paramsToState(self):

        foodPosition = self.get_apple_position()
        blockedPositions = self.get_blocked_directions()

        direction = ""
        dx = self.snake.body[1][0] - self.snake.body[0][0]
        dy = self.snake.body[1][1] - self.snake.body[0][1]

        if dx == -self.pixelSize and dy == 0:
            # Moving right
            direction = "0"
        if dx == self.pixelSize and dy == 0:
            # Moving left
            direction = "1"
        if dx == 0 and dy == self.pixelSize:
            # Moving up
            direction = "2"
        if dx == 0 and dy == -self.pixelSize:
            # Moving down
            direction = "3"

        snakeDistance = self.get_distance_snake()
        '''
        state = xxxxxx_xxxx_x_x_x_x_x
        foodPosition: right left Xmiddle down up Ymiddle
        blockedPositions: left rop right bottom
        direction: 0 OR 1 OR 2 OR 3
        distanceToSnakeLeft
        distanceToSnakeRight
        distanceToSnakeTop
        distanceToSnakeBottom
        '''
        state = foodPosition + "_" + blockedPositions + "_" + direction  # + "_" + snakeDistance -> Determined to worsen QLearning performance
        return state

    def step(self, model, gameType):
        action = None
        if gameType == "MANUAL":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        action = 0
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        action = 1
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        action = 2
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        action = 3
                    # Esc -> Create event to quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

        elif gameType == "ASTAR":
            action = model.generatePrediction(self)
        else:
            action = model.generatePrediction(self.paramsToState())

        if action is not None:
            if action == 0 and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            if action == 1 and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'
            if action == 2 and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            if action == 3 and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'

        if self.snake.direction == 'UP':
            self.snake.y -= self.pixelSize
        if self.snake.direction == 'DOWN':
            self.snake.y += self.pixelSize
        if self.snake.direction == 'LEFT':
            self.snake.x -= self.pixelSize
        if self.snake.direction == 'RIGHT':
            self.snake.x += self.pixelSize
        # Snake body growing mechanism
        self.snake.body.insert(0, list([self.snake.x, self.snake.y]))
        if self.collision_food():
            self.score += 1
            self.food.spawned = False

            if model == "QLearning":
                model.onScore(self.paramsToState())
        else:
            self.snake.body.pop()
        self.snake.head = self.snake.body[0]

        if not self.food.spawned:
            self.food.x = random.randrange(1, (self.frame_size_x // self.pixelSize)) * self.pixelSize
            self.food.y = random.randrange(1, (self.frame_size_y // self.pixelSize)) * self.pixelSize

            while [self.food.x, self.food.y] in self.snake.body:
                self.food.x = random.randrange(1, (self.frame_size_x // self.pixelSize)) * self.pixelSize
                self.food.y = random.randrange(1, (self.frame_size_y // self.pixelSize)) * self.pixelSize

        self.food.spawned = True
        # GFX
        self.game_window.fill(black)
        body_part = 0
        for node in self.snake.body:
            if body_part == 0:
                pygame.draw.rect(self.game_window, magenta,
                                 pygame.Rect(node[0], node[1], self.pixelSize, self.pixelSize))
            else:
                pygame.draw.rect(self.game_window, green, pygame.Rect(node[0], node[1], self.pixelSize, self.pixelSize))
            body_part += 1

        # Snake food
        pygame.draw.rect(self.game_window, white, pygame.Rect(self.food.x, self.food.y, self.pixelSize, self.pixelSize))
        # Game Over conditions
        # Getting out of bounds
        if self.collision_boundaries(self.snake.head):
            if model is not None:
                model.onGameOver(self.score)
            self.snake.alive = False
            return self.paramsToState(), self.score, True

        # Touching the snake body
        if self.collision_snake(self.snake.head):
            if model is not None:
                model.onGameOver(self.score)
            self.snake.alive = False
            return self.paramsToState(), self.score, True

        else:
            self.score = self.score

        self.show_score(1, white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(self.difficulty)
        return self.paramsToState(), self.score, False


if __name__ == "__main__":
    difficulty = 50

    # Window size
    frame_size_x = 750
    frame_size_y = 500

    snake = Snake(100, 50, [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]], [100, 50])
    game = Game(frame_size_x, frame_size_y, difficulty, snake)

    while True:
        game.step(None, "MANUAL")
