class Snake:
    def __init__(self, x, y, body, head):
        self.x = x
        self.y = y
        self.size = len(body)
        self.body = body
        self.head = head
        self.direction = "RIGHT"
        self.alive = True



class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spawned = True