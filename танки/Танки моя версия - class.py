# 1) танки
# 2) пули

# импортирование модулей
import pygame
from random import randint, choice
pygame.init()

# переменные настройки
W, H = 1800, 800
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
tank_direction = [choice([1, -1]), 0]

tanks = []

# танк игрока
player_rect = pygame.Rect(W//2, H//2, cell_size, cell_size)

player_speed = 3
# танки
class Tank:
    def __init__(self, color, speed, direction, turn_delay, shot_delay,  x_pos, y_pos):
        tanks.append(self)
        self.rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        self.speed = speed
        self.color = color
        self.direction = direction
        self.turn_delay = turn_delay
        self.shot_delay = shot_delay


    def update(self):
        if self.turn_delay == 0:
            self.turn_delay = randint(30, 120)
            if self.direction[0] == 0:
                self.direction[0] = choice([1, -1])
                self.direction[1] = 0
            else:
                self.direction[1] = choice([1, -1])
                self.direction[0] = 0

        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

        if self.rect.x < 0 or self.rect.x > W-cell_size or self.rect.y < 0 or self.rect.y > H-cell_size:
            self.rect.x -= self.speed * self.direction[0]
            self.rect.y -= self.speed * self.direction[1]
            self.direction[0] = -self.direction[0]
            self.direction[1] = -self.direction[1]

        if self.turn_delay:
            self.turn_delay -= 1


    def draw(self):
        pygame.draw.rect(sc, self.color, self.rect)
        x, y = self.rect.centerx + self.direction[0]*40, self.rect.centery + self.direction[1]*40
        pygame.draw.line(sc, (50, 50, 50), self.rect.center, (x, y), 10)
    


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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT] and player_speed != 6:
        player_speed += 3
    else:
        player_speed = 3

    if keys[pygame.K_w] and player_rect.y > 0:
        player_rect.y -= player_speed
        #keys[pygame.K_d] = False
        #keys[pygame.K_s] = False
        #keys[pygame.K_a] = False
    elif keys[pygame.K_d] and player_rect.x < W - cell_size:
        player_rect.x += player_speed
        #keys[pygame.K_s] = False
        #keys[pygame.K_a] = False
    elif keys[pygame.K_s] and player_rect.y < H - cell_size:
        player_rect.y += player_speed
        #keys[pygame.K_a] = False
    elif keys[pygame.K_a] and player_rect.x > 0:
        player_rect.x -= player_speed


            # добавление нового вражеского танка
    if new_tank_timer:
        new_tank_timer -= 1

    if new_tank_timer == 0 and len(tanks) < 5:
        new_tank_timer = 300
        x, y = randint(0, W-cell_size), randint(0, H-cell_size)
        tank_direction = [choice([1, -1]), 0]
        Tank(tank_color, tank_speed, tank_direction, 60, 0, x, y)

    for tank in tanks:
        tank.draw()

    for tank in tanks:
        tank.update()

    pygame.draw.rect(sc, 'yellow', player_rect)
    pygame.display.update()
    
    clock.tick(FPS)


pygame.quit()
