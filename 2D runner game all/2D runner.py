import pygame
import random

pygame.init()

# define tuning variables
screen_width = 900
screen_height = 600

clock = pygame.time.Clock()
FPS =  60

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("2D runner")

# def font
f_score = pygame.font.Font(None, 40)
f_game_over = pygame.font.Font(None, 80)

# define game variables
rect = pygame.rect.Rect(175, -150, 150, 150)
object_size = 150
game_speed = 5

player_rect = pygame.rect.Rect(0, 0, 50, 50)
player_rect.center = (screen_width // 2, screen_height - 50)
player_pos = 1
score = 3000

game_over = False

def draw_bg():
    screen.fill('blue')
    for i in range(150, 751, 200):
        pygame.draw.line(screen, 'black', (i, 0), (i, screen_height), 10)

def draw_text(text, x, y, font):
    image = font.render(text, font, 'white')
    image_rect = image.get_rect(center = (x, y))
    screen.blit(image, image_rect)

def reset_game():
    global game_over, score, player_pos, objects
    game_over = False
    score = 0
    player_pos = 1
    
    objects = []
    start_obj = Object(1)
    objects.append(start_obj)

class Object():
    def __init__(self, line):
        self.line = line
        self.rect = pygame.rect.Rect(175 + 200 * line, -object_size, object_size, object_size)

    def update(self):
        global game_over, score
        #if self.rect.colliderect(player_rect):
        #    game_over = True
        self.rect.y += game_speed
        if self.rect.y > screen_height:
            score += 1
            objects.remove(self)

    def draw(self):
        pygame.draw.rect(screen, 'red', self.rect)
        

objects = []
start_obj = Object(1)
objects.append(start_obj)

run = True
while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over == True:
                reset_game()
                
            if event.type == pygame.KEYDOWN and game_over == False:
                if event.key == pygame.K_RIGHT and player_pos < 2:
                    player_pos += 1
                if event.key == pygame.K_LEFT and player_pos > 0:
                    player_pos -= 1

    game_speed = 5 + min(score // 10, 20000)
    if game_over == False:
        player_rect.center = (250 + 200 * player_pos, screen_height - 50)
        
        if objects[-1].rect.y > 400:
            line = random.randint(0, 2)
            obj = Object(line)
            objects.append(obj)

        for obj in objects:
            obj.update()

        draw_bg()
        
        for obj in objects:
            obj.draw()

        pygame.draw.rect(screen, 'green', player_rect)
        draw_text(f'score: {score}', 70, 30, f_score)

    else:
        screen.fill('blue')
        draw_text(f'your score is {score}', screen_width // 2, screen_height // 2 - 100, f_game_over)
        draw_text('game over', screen_width // 2, screen_height // 2, f_game_over)
        draw_text('press R to restart', screen_width // 2, screen_height // 2 + 100, f_game_over)
        
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
