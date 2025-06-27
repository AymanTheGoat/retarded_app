import os

import random

import msvcrt


WIDTH = 14
HEIGHT = 14

class Snake:
    def __init__(self):
        self.randomApple()
        self.head = (WIDTH // 2, HEIGHT // 2)
        self.direction = "up"
        self.body = []
        self.score = 0

    def randomApple(self):
        self.apple = (random.randint(0, WIDTH - 1), random.randint(0, WIDTH - 1))

    def trimTail(self):
        if len(self.body) > self.score:
            self.body.pop()


    def move(self):
        x, y = self.head

        if self.direction == "w":
            self.body.insert(0, self.head)
            y -= 1
        elif self.direction == "s":
            self.body.insert(0, self.head)
            y += 1
        elif self.direction == "a":
            self.body.insert(0, self.head)
            x -= 1
        elif self.direction == "d":
            self.body.insert(0, self.head)
            x += 1

        if (x, y) in self.body  or x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            print("You lose!")
            exit(0)
        if (x, y) == self.apple:
            self.score += 1
            self.randomApple()

        self.head = (x, y)


    def draw(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) == self.head:
                    print("🤡", end="")
                elif (x, y) == self.apple:
                    print("🍎", end="")
                elif (x, y) in self.body:
                    print("🟩", end="")      
                else:
                    print("⬜", end="")
            print()


def game_loop():
    snake = Snake()

    while True:
        msvcrt.kbhit()

        snake.direction = msvcrt.getch().decode("utf-8")
        snake.move()
        os.system("cls")
        snake.draw()
        snake.trimTail()


if __name__ == "__main__":
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit(0)