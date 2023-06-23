# 1) танки
# 2) пули

import pygame
from random import randint
pygame.init()

W, H = 600, 400
FPS = 60
f1 = pygame.font.Font(None, 30)
f2 = pygame.font.Font(None, 100)
pygame.time.set_timer(pygame.USEREVENT, 1000)

sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

enemies = []
# pfgjkyt
enemies_max = 1
#for i in range(enemies_max):
#    x, y = randint(0, W-50), 0
#    enemy = (x, y, 50, 50)
#    enemies.append(pygame.Rect(enemy))
bullets = []
enemy_direction = [] #[[0, 0]] * enemies_max #, (1, 0), (1, 0)]

px, py = W // 2 - 25, H - 50
player_speed = 4
player_direction = [0, -1]
player_rect = pygame.Rect([px, py, 50, 50])

score = 0
enemy_speed = 1
bullet_speed = 7
game_end = 300
timer = 0

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        elif event.type == pygame.USEREVENT and len(enemies) < enemies_max:
            x, y = randint(0, W-50), randint(0, H-50)
            enemy = (x, y, 50, 50)
            enemies.append(pygame.Rect(enemy))
            enemy_direction.append([0, 0])

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append([list(player_rect.center), [player_direction[0], player_direction[1]]])




    
    # Управление игроком
    keys = pygame.key.get_pressed()
    player_speed = 4
    if keys[pygame.K_w]:
        player_direction = [0, -1]
        player_rect.y -= player_speed
        if player_rect.y < 0:
            player_rect.y = 0
    elif keys[pygame.K_d]:
        player_direction = [1, 0]
        player_rect.x += player_speed
        if player_rect.x > W - 50:
            player_rect.x = W - 50
    elif keys[pygame.K_s]:
        player_direction = [0, 1]
        player_rect.y += player_speed
        if player_rect.y > H - 50:
            player_rect.y = H - 50
    elif keys[pygame.K_a]:
        player_direction = [-1, 0]
        player_rect.x -= player_speed
        if player_rect.x < 0:
            player_rect.x = 0
        


    if timer > 0:
        timer -= 1

    
    
    if timer == 0:        
        timer = 60
        if enemy_speed < 2:
            enemy_speed = score // 10 + 1
        
        for i in range(len(enemy_direction)):
            # 1-up 2-left 3-right 4-down
            direction = randint(1, 4)
            if direction == 1:
                enemy_direction[i] = [0, -1]
                yspeed = -enemy_speed
                xspeed = 0
            if direction == 2:
                enemy_direction[i] = [-1, 0]
                xspeed = -enemy_speed
                yspeed = 0
            if direction == 3:
                enemy_direction[i] = [1, 0]
                xspeed = enemy_speed
                yspeed = 0
            if direction == 4:
                enemy_direction[i] = [0, 1]
                yspeed = enemy_speed
                xspeed = 0


    for i in range(len(enemies)):
        enemies[i].x += enemy_speed * enemy_direction[i][0]
        enemies[i].y += enemy_speed * enemy_direction[i][1]
        if enemies[i].x < 0:
            enemy_direction[i][0] = -enemy_direction[i][0]
        if enemies[i].y > 0:
            enemy_direction[i][1] = -enemy_direction[i][1]
        if enemies[i].x > W - 50:
            enemy_direction[i][0] = -enemy_direction[i][0]
        if enemies[i].y < H - 50:
            enemy_direction[i][1] = -enemy_direction[i][1]




    sc.fill('black')


    if len(enemies):
        for i in range(len(enemies)):
            pygame.draw.rect(sc, 'grey', enemies[i])
            if enemy_direction[i][0] == -1 or enemy_direction[i][0] == 1:
                pygame.draw.line(sc, 'darkgrey', enemies[i].center, (enemies[i].center[0] + 40 * enemy_direction[i][0], enemies[i].center[1]), 10)
            else:
                pygame.draw.line(sc, 'darkgrey', enemies[i].center, (enemies[i].center[0], enemies[i].center[1] + 40 * enemy_direction[i][1]), 10)

    if score >= 5:
        enemies = []
        sc.fill('black')
        win_text = f2.render('You win!', 1, 'white')
        win_text_pos = win_text.get_rect(center = (W//2, H//2))
        sc.blit(win_text, win_text_pos)
        score = 5
        game_end -= 1
        if game_end == 0:
            play = False



    for bullet in bullets:
        pygame.draw.circle(sc, 'red', bullet[0], 5)

    for i in range(len(bullets)):
        #if len(bullets) < i:
        bullets[i][0][0] += bullet_speed * bullets[i][1][0]
        bullets[i][0][1] += bullet_speed * bullets[i][1][1]
    
        for enemy in enemies:
            if enemy.collidepoint(bullets[i][0]):
                #if len(bullets):
                    #bullets.remove(bullets[i])
                    enemies.remove(enemy)
                    score += 1
                    break

    pygame.draw.rect(sc, 'yellow', player_rect)
    if player_direction[0] == -1 or player_direction[0] == 1:
        pygame.draw.line(sc, 'orange', player_rect.center, (player_rect.center[0] + 40 * player_direction[0], player_rect.center[1]), 10)
    else:
        pygame.draw.line(sc, 'orange', player_rect.center, (player_rect.center[0], player_rect.center[1] + 40 * player_direction[1]), 10)

    for i in range(len(enemies)):
        if player_rect.colliderect(enemies[i]):
            #if player_rect.right > enemies[i].left and player_direction[0] == 1:
            #player_rect.right = enemies[i].left
            #enemies[i].left = player_rect.right
            player_rect.x -= player_speed*-enemy_direction[i][0]
            player_rect.y -= player_speed*-enemy_direction[i][1]
            enemies[i].x -= enemy_speed*enemy_direction[i][0]
            enemies[i].y -= enemy_speed*enemy_direction[i][1]
            #enemy_speed = 0
            #player_speed = 0
            #elif player_rect.left < enemy.right and player_direction[0] == -1:
            #    player_rect.left = enemy.right
            #elif player_rect.bottom > enemy.top and player_direction[1] == 1:
            #    player_rect.bottom = enemy.top
            #elif player_rect.top < enemy.bottom and player_direction[1] == -1:
            #    player_rect.top = enemy.bottom
            #if score > 0:
            #    score -= 1
            #enemies.remove(enemy)

        
            

    score_text = f1.render(f'очки: '+str(score), 1, 'white')
    sc.blit(score_text, (0, 0))


    pygame.display.update()
    
    clock.tick(FPS)


pygame.quit()
