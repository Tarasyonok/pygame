# 1) танки
# 2) пули

# import modules
import pygame
from random import randint
pygame.init()

# tuning
W, H = 600, 400
FPS = 60

sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

pygame.display.set_caption('Танки')

# game variables
new_enemy = True
tanks = []


# functions
def draw_background():
    bg_color = (20, 100, 0)
    sc.fill(bg_color)



play = True

# main loop
while play:
    # background
    draw_background()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    if new_tank:
        x, y = randint(0, W-50), randint(0, H-50)
        tank = (x, y, 50, 50)
        tanks.append(pygame.Rect(tank))

    pygame.display.update()
    
    clock.tick(FPS)


pygame.quit()
