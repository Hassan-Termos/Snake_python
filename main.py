import pygame
from pygame.locals import *
import time
import random
import sys

SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (45, 134, 51)
DARK_GREEN = (45, 134, 51)

class Blue_Box:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("python_project/resources/apple.png").convert_alpha()
        self.move()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 14) * SIZE
        self.y = random.randint(0, 14) * SIZE
        if (450 <= self.x <= 600 and 0 <= self.y <= 40):
            self.x = random.randint(0, 10) * SIZE
            self.y = random.randint(0, 10) * SIZE

class Red_Box:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("python_project/resources/Eaten_apple.png").convert_alpha()
        self.visible = False
        self.move()

    def draw(self):
        if self.visible:
            self.parent_screen.blit(self.image, (self.x, self.y))
            pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 10) * SIZE
        self.y = random.randint(0, 10) * SIZE
        if (450 <= self.x <= 600 and 0 <= self.y <= 40):
            self.x = random.randint(0, 10) * SIZE
            self.y = random.randint(0, 10) * SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.head_image = pygame.image.load("python_project/resources/head.png").convert_alpha()
        self.body_image = pygame.image.load("python_project/resources/body.png").convert_alpha()
        self.direction = 'right'
        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        self.draw()

    def draw(self):
        for i in range(self.length):
            if i == 0:
                image = self.head_image
                if self.direction == 'left':    
                    image = pygame.transform.rotate(self.head_image, 90)
                elif self.direction == 'right':
                    image = pygame.transform.rotate(self.head_image, -90)
                elif self.direction == 'up':
                    image = pygame.transform.rotate(self.head_image, 0)
                elif self.direction == 'down':
                    image = pygame.transform.rotate(self.head_image, 180)
            else:
                prev_x = self.x[i - 1]
                prev_y = self.y[i - 1]
                curr_x = self.x[i]
                curr_y = self.y[i]
                if prev_x == curr_x:
                    angle = 90 if prev_y < curr_y else -90
                else:
                    angle = 0 if prev_x < curr_x else 180
                image = pygame.transform.rotate(self.body_image, angle)
            self.parent_screen.blit(image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def decrease_length(self):
        if self.length > 1:
            self.length -= 1
            self.x.pop()
            self.y.pop()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple Game")
        self.surface = pygame.display.set_mode((600, 600))
        self.background_image = pygame.image.load("python_project/resources/BG.png").convert()
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.Blue_Box = Blue_Box(self.surface)
        self.Blue_Box.draw()
        self.Red_box = Red_Box(self.surface)
        self.Red_box.visible = False

    def reset(self):
        self.snake = Snake(self.surface)
        self.Blue_Box = Blue_Box(self.surface)
        self.Red_box = Red_Box(self.surface)
        self.Red_box.visible = False

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def border_collision(self):
        if self.snake.x[0] < 0 or self.snake.x[0] >= 600 or self.snake.y[0] < 0 or self.snake.y[0] >= 600 or (430 <= self.snake.x[0] <= 600 and 0 <= self.snake.y[0] <= 35):
            return True
        return False

    def play(self):
        self.surface.blit(self.background_image, (0, 0))
        self.snake.walk()
        self.Blue_Box.draw()
        self.display_score()
        pygame.display.flip()
        if self.snake.length >6:
            self.Red_box.visible = True
            self.Red_box.draw()
        else:
            self.Red_box.visible = False
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.Blue_Box.x, self.Blue_Box.y):
            self.snake.increase_length()
            self.Blue_Box.move()
        if self.Red_box.visible and self.is_collision(self.snake.x[0], self.snake.y[0], self.Red_box.x, self.Red_box.y):
            self.snake.decrease_length()
            self.Red_box.move()
        if self.border_collision():
            raise "Collision Occurred"
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occurred"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length-1}", True, (255, 255, 255))
        pygame.draw.rect(self.surface, (255, 255, 255), (445, 0, 160, 43), 3)
        self.surface.blit(score, (450, 10))

    def show_game_over(self):
        self.surface.fill(GREEN)
        bigger_font = pygame.font.SysFont('arial', 50)
        normal_font = pygame.font.SysFont('arial', 20)
        line0 = bigger_font.render(f"GAME OVER!!", True, (0,0,0))
        self.surface.blit(line0, (100, 200))
        line1 = normal_font.render(f"Your score is: {self.snake.length-1}", True, (0,0,0))
        self.surface.blit(line1, (100, 250))
        line2 = normal_font.render("To play again press Enter.", True, (0,0,0))
        self.surface.blit(line2, (400, 550))
        line3 = normal_font.render("To exit press Escape.", True, (0,0,0))
        self.surface.blit(line3, (400, 575))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            try:
                if not pause:
                    self.play()
                    if self.snake.length >= 5:
                        time.sleep(0)
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.5)

def main_page():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Snake And Apples Game")
    background_image = pygame.image.load("python_project/resources/main.png").convert()
    font = pygame.font.SysFont('arial', 30)
    small_font = pygame.font.SysFont('arial', 20)

    def draw_button(text, rect, color, text_color):
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def draw_title():
        title_font = pygame.font.SysFont('timesnewroman', 50)
        title_surface = title_font.render("Snake And Boxes Game", True, WHITE)
        title_rect = title_surface.get_rect(center=(300, 100))
        screen.blit(title_surface, title_rect)
        
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        draw_title()
        button1_rect = pygame.Rect((200, 450, 200, 50))
        button2_rect = pygame.Rect((200, 510, 200, 50))
        draw_button("Start Game", button1_rect, GREEN, WHITE)
        draw_button("Exit", button2_rect, GREEN, WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    game = Game()
                    game.run()
                elif button2_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEMOTION:
                if button1_rect.collidepoint(event.pos):
                    draw_button("Start Game", button1_rect, DARK_GREEN, WHITE)
                if button2_rect.collidepoint(event.pos):
                    draw_button("Exit", button2_rect, DARK_GREEN, WHITE)
        pygame.display.flip()

if __name__ == '__main__':
    main_page()
