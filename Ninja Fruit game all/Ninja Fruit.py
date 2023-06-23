import pygame
import random

pygame.init()

# define tuning variables
screen_width = 900
screen_height = 600

clock = pygame.time.Clock()
FPS =  60

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Ninja Fruit")
'''
fruit_size = 50
fruitX = screen_width // 2
fruitY = screen_height + fruit_size

fruit = pygame.rect.Rect((fruitX, fruitY, fruit_size, fruit_size))
fruit_speed = -20
'''
class Fruit():
    def __init__(self, x, y):
        self.index = random.randint(0, 4)
        self.color = ['red', 'green', 'orange', 'yellow', 'brown'][self.index]
        self.size = [50, 80, 60, 60, 70][self.index]
        self.rect = pygame.rect.Rect((x, y, self.size, self.size))
        self.fly_force = -random.randint(15, 25)
        self.x_change = random.randint(-7, 7)

    def update(self):
        self.fly_force += 0.5
        self.rect.y += self.fly_force
        self.rect.x += self.x_change
        if self.rect.y > screen_height:
            fruits.remove(self)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

fruits = []

run = True
while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    if len(fruits) == 0:
        count = random.randint(1, 3)
        for i in range(count):
            x = random.randint(100, screen_width - 180)
            y = screen_height
            fruit = Fruit(x, y)
            fruits.append(fruit)

    for fruit in fruits:
        fruit.update()

    screen.fill((190, 130, 90))


    for fruit in fruits:
        fruit.draw()

    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()
