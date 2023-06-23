import pygame
from pygame.locals import *
import random
pygame.init()

# define tuning variables
screen_width = 900
screen_height = 600

clock = pygame.time.Clock()
FPS =  60

screen = pygame.display.set_mode((screen_width, screen_height))

# def font
f = pygame.font.Font("font/BAUHS93.ttf", 60)

# define game variables
img_bg = pygame.image.load("flappy bird images/bg.png")
img_floor = pygame.image.load("flappy bird images/floor.png")
img_restart_button = pygame.image.load("flappy bird images/restart.png")

bird_images = []
for num in range(1, 4):
    img = pygame.image.load(f"flappy bird images/bird{num}.png")
    bird_images.append(img)

floor_scroll = 0
scroll_speed = 4
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0

pass_pipe = False
flying = False
game_over = False

def draw_score(text):
    img = f.render(text, f, 'white')
    screen.blit(img, (screen_width // 2, 20))

def reset_game():

    pipe_group.empty()
    flappy.vel = 0
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    

    score = 0

    return score

class Bird(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = bird_images
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center = [x, y])
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:    
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                

            # handle the animation
            self.counter += 1
            flap_cooldown = 15
            
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flappy bird images/pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:     
            self.rect.topleft = [x, y + int(pipe_gap / 2)]


    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))

    def draw(self):

        press = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == True:
            press = True

        # draw button
        screen.blit(self.image, self.rect)

        return press
        

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

restart_button = Button(screen_width // 2, screen_height // 2, img_restart_button)

run = True
while run:
    clock.tick(FPS)

    # drawing background
    screen.blit(img_bg, (0, 0))

    # drawing bird
    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)   

    

    # drawing floor
    screen.blit(img_floor, (floor_scroll, 500))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False


    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True


    #check if birs has hit the ground
    if flappy.rect.bottom > 500:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # scrolling floor
        floor_scroll -= scroll_speed
        if abs(floor_scroll) > 20:
            floor_scroll = 0

        pipe_group.update()

    if game_over == True:
        if restart_button.draw():
            print('Clicked')
            game_over = False
            score = reset_game()
            #pygame.time.delay(100)

    draw_score(str(score))

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
               and flying == False and game_over == False:
                flying = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over == True:
                if restart_button.draw():
                    print('Clicked')
                    game_over = False
                    score = reset_game()
                    #pygame.time.delay(100)
    pygame.display.update()

pygame.quit()
