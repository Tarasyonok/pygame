# 1) танки
# 2) пули

# импортирование модулей
import pygame
from random import randint, choice
pygame.init()

# переменные настройки
W, H = 600, 400
FPS = 60

sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

pygame.display.set_caption('Танки')

# игровые переменные
new_tank_timer = 0 # new enemy every 5 seconds
new_tank = True
tank_speed = 3
tank_color = (200, 200, 200)
cell_size = 50
tank_direction = [1, 0]

tanks = []


# танки
class Tank:
    def __init__(self, color, timer, x_pos, y_pos):
        tanks.append(self)
        self.rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        self.color = color
        self.timer = timer
    
    def update(self):
        if self.timer == 0:
            self.timer = 180
            self.color = choice(['red', 'yellow', 'blue', 'orange'])

        if self.timer:
            self.timer -= 1
        
    def draw(self):
        pygame.draw.rect(sc, self.color, self.rect)


# функции
def draw_background():       # отрисовка фона
    bg_color = (20, 100, 0)
    sc.fill(bg_color)

play = True
# главный цикл

while play:
    
    # фон
    draw_background()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


    # добавление нового вражеского танка
    if new_tank_timer:
        new_tank_timer -= 1

    if new_tank_timer == 0 and len(tanks) < 5:
        new_tank_timer = randint(30, 180)
        x, y = randint(0, W-cell_size), randint(0, H-cell_size)
        Tank((255, 255, 255), 60, x, y)

    for tank in tanks:
        tank.draw()

    for tank in tanks:
        tank.update()
    #tanks[0].update()

    pygame.display.update()
    
    clock.tick(FPS)


pygame.quit()
