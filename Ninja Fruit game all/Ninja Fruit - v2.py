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

# def font
f = pygame.font.Font(None, 40)

# define game variables
types = [pygame.image.load('fruit images/apple.png').convert_alpha(),
         pygame.image.load('fruit images/watermelon.png').convert_alpha(),
         pygame.image.load('fruit images/orange.png').convert_alpha(),
         pygame.image.load('fruit images/banana.png').convert_alpha(),
         pygame.image.load('fruit images/coconut.png').convert_alpha()]

cut_types = [pygame.image.load('fruit images/cut apple.png').convert_alpha(),
             pygame.image.load('fruit images/cut watermelon.png').convert_alpha(),
             pygame.image.load('fruit images/cut orange.png').convert_alpha(),
             pygame.image.load('fruit images/cut banana.png').convert_alpha(),
             pygame.image.load('fruit images/cut coconut.png').convert_alpha()]
score = 0

def draw_score(text):
    image = f.render(text, f, 'white')
    image_rect = image.get_rect(topleft = (10, 10))
    screen.blit(image, image_rect)

class Fruit():
    def __init__(self, x, y):
        self.index = random.randint(0, 4)
        self.type = types[self.index]
        self.rect = self.type.get_rect(center = (x, y))
        self.fly_force = -random.randint(15, 25)
        self.x_change = random.randint(-7, 7)

    def update(self):
        global score
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            score += 1
            cut1 = Cut_fruit(self.rect.x, self.rect.y, self.index, self.fly_force, self.x_change, 1)
            cut2 = Cut_fruit(self.rect.x, self.rect.y, self.index, self.fly_force, self.x_change, -1)
            cut_fruits.append(cut1)
            cut_fruits.append(cut2)
            fruits.remove(self)
        else:
            self.fly_force += 0.5
            self.rect.y += self.fly_force
            self.rect.x += self.x_change
            if self.rect.y > screen_height:
                fruits.remove(self)

        

    def draw(self):
        screen.blit(self.type, self.rect)


class Cut_fruit():
    def __init__(self, x, y, index, fly_force, x_change, num):
        self.index = index
        self.type = cut_types[self.index]
        self.rect = self.type.get_rect(topleft = (x, y))
        self.fly_force = fly_force
        self.x_change = x_change + 3 * num

    def update(self):
        self.fly_force += 0.5
        self.rect.y += self.fly_force
        self.rect.x += self.x_change
        if self.rect.y > screen_height:
            cut_fruits.remove(self)

        

    def draw(self):
        screen.blit(self.type, self.rect)

fruits = []
cut_fruits = []

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

    for cut_fruit in cut_fruits:
        cut_fruit.update()

    screen.fill((190, 130, 90))


    for fruit in fruits:
        fruit.draw()

    for cut_fruit in cut_fruits:
        cut_fruit.draw()

    draw_score(f'score: {score}')
        
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()
