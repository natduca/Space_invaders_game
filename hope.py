import pygame
import time
import math
from classes import spaceship
from classes import bullet
from classes import barrier
from pygame import mixer
import random

pygame.init()

mixer.music.load('background.wav')
mixer.music.play(-1)

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

yours = spaceship(pygame.image.load('spaceship!.png'), 380, 480, 0, 0, 3, 3)
Enemy = spaceship(pygame.image.load('enemy.png'), random.randint(0, 735), random.randint(50, 150), 0.4, 0, 1, 1)
# Enemy3 = spaceship(pygame.image.load('enemy.png'), random.randint(0, 735), random.randint(50, 150), 0.5, 0, 1, 1)
Enemy1 = spaceship(pygame.image.load('ufo (1).png'), random.randint(0, 735), random.randint(50, 150), 0.1, 0, 3, 3)
Enemy2 = spaceship(pygame.image.load('ufo (2).png'), random.randint(0, 735), random.randint(50, 150), 0.25, 0, 2, 2)
Barrier1 = barrier(pygame.image.load('mansory.png'), 380, 400, 5, 5)
Barrier2 = barrier(pygame.image.load('mansory.png'), 170, 400, 5, 5)
Barrier3 = barrier(pygame.image.load('mansory.png'), 590, 400, 5, 5)
BarrierX = [Barrier1.X, Barrier2.X, Barrier3.X]
BarrierY = [Barrier1.Y, Barrier2.Y, Barrier3.Y]
BarrierHealth = [Barrier1.CHP, Barrier2.CHP, Barrier3.CHP]

EnemyX = [Enemy.X, Enemy1.X, Enemy2.X]
EnemyY = [Enemy.Y, Enemy1.Y, Enemy2.Y]
Enemyimg = [Enemy.image, Enemy1.image, Enemy2.image]
EnemyXchange = [Enemy.speedX, Enemy1.speedX, Enemy2.speedX]
EnemyYchange = [Enemy.speedY, Enemy1.speedY, Enemy2.speedY]
EnemyHP = [Enemy.CHP, Enemy1.CHP, Enemy2.CHP]
Enemy_health = [Enemy.health, Enemy1.health, Enemy2.health]

yourbullet = bullet(pygame.image.load('bullet.png'), 0, 0, 0, 0.7, True)
enemybullet = bullet(pygame.image.load('bulletrotated.png'), 0, 0, 0, 0.7, True)

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

TextX = 10
TextY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def enemy_shoot(ship):
    bullet_sound = mixer.Sound('laser.wav')
    bullet_sound.play()
    enemybullet.X = EnemyX[ship]
    enemybullet.Y = EnemyY[ship]
    fire_bullet(enemybullet, enemybullet.X, enemybullet.Y)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def barrier(x, y):
    screen.blit(Barrier1.image, (x, y))

def player(x, y):
    screen.blit(yours.image, (x, y))


def enemy(x, y, i):
    screen.blit(Enemyimg[i], (x, y))


def fire_bullet(bullet, x, y):
    bullet.ready = False
    screen.blit(bullet.image, (x + 16, y + 10))


def isCollision(X1, Y1, X2, Y2, pix):
    distance = math.sqrt((math.pow(X1 - X2, 2)) + (math.pow(Y1 - Y2, 2)))
    if distance < pix:
        return True


running = True
while running:
    # red, green, blue
    screen.fill((155, 155, 155))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                yours.speedX = -0.2
            if event.key == pygame.K_RIGHT:
                yours.speedX = 0.2
            if event.key == pygame.K_SPACE and yourbullet.ready:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                yourbullet.X = yours.X
                yourbullet.Y = yours.Y
                fire_bullet(yourbullet, yourbullet.X, yourbullet.Y)
            if event.key == pygame.K_w and enemybullet.ready:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                enemybullet.X = EnemyX[1]
                enemybullet.Y = EnemyY[1]
                fire_bullet(enemybullet, enemybullet.X, enemybullet.Y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                yours.speedX = 0

    yours.X += yours.speedX

    if yours.X < -50:
        yours.X = 790
    elif yours.X > 790:
        yours.X = -50

    for i in range(len(EnemyX)):
        EnemyX[i] += EnemyXchange[i]
        if EnemyX[i] <= 0:
            EnemyXchange[i] = abs(EnemyXchange[i])
            EnemyY[i] += 40
        elif EnemyX[i] >= 736:
            EnemyXchange[i] = -EnemyXchange[i]
            EnemyY[i] += 40
        run_in = isCollision(EnemyX[i], EnemyY[i], yours.X, yours.Y, 40)
        if run_in:
            for j in range(len(EnemyY)):
                EnemyY[j] = 10000
        if EnemyY[i] > 800:
            over_text1 = over_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(over_text1, (200, 250))
            mixer.music.stop()
            for j in range(len(EnemyX)):
                EnemyX[j] = -200000
            break


        they_hit = isCollision(EnemyX[i], EnemyY[i], yourbullet.X, yourbullet.Y, 35)
        if they_hit:
            hit_sound = mixer.Sound('explosion.wav')
            hit_sound.play()
            yourbullet.Y = 800
            yourbullet.ready = True
            EnemyHP[i] -= 1
            if EnemyHP[i] <= 0:
                score_value += 1
                EnemyX[i] = random.randint(0, 735)
                EnemyY[i] = random.randint(50, 150)
                EnemyHP[i] = Enemy_health[i]
        enemy(EnemyX[i], EnemyY[i], i)

    numb = random.randint(0, 2)
    if enemybullet.ready:
        enemy_shoot(numb)
    # if numb == 2 and enemybullet.ready:
    #     enemy_shoot(1)
    # if numb == 3 and enemybullet.ready:
    #     enemy_shoot(2)

    if yourbullet.Y <= 0:
        yourbullet.Y = 800
        yourbullet.ready = True
    if not yourbullet.ready:
        fire_bullet(yourbullet, yourbullet.X, yourbullet.Y)
        yourbullet.Y -= yourbullet.speedY
    if enemybullet.Y > 900 and enemybullet.X > 0:
        enemybullet.ready = True
    if not enemybullet.ready:
        fire_bullet(enemybullet, enemybullet.X, enemybullet.Y)
        enemybullet.Y += enemybullet.speedY

    your_hit = isCollision(yours.X, yours.Y, enemybullet.X, enemybullet.Y, 35)
    if your_hit:
        hit_sound = mixer.Sound('explosion.wav')
        hit_sound.play()
        yours.CHP -= 1
        enemybullet.Y = 600
        print(yours.CHP)
        if yours.CHP <= 0:
            game_over_text()
            for j in range(len(EnemyX)):
                EnemyX[j] = -200000

    for i in range(len(BarrierX)):
        barrier(BarrierX[i], BarrierY[i])
        barrier_hit = isCollision(BarrierX[i], BarrierY[i], enemybullet.X, enemybullet.Y, 37)
        if barrier_hit:
            hit_sound = mixer.Sound('explosion.wav')
            hit_sound.play()
            enemybullet.Y = 600
            BarrierHealth[i] -= 1
            if BarrierHealth[i] <= 0:
                BarrierX[i] = 2000
                BarrierY[i] = 50
        barrier_hit1 = isCollision(BarrierX[i], BarrierY[i], yourbullet.X, yourbullet.Y, 37)
        if barrier_hit1:
            hit_sound = mixer.Sound('explosion.wav')
            hit_sound.play()
            yourbullet.Y = 800
            yourbullet.ready = True
            BarrierHealth[i] -= 1
            if BarrierHealth[i] <= 0:
                BarrierX[i] = 2000
                BarrierY[i] = 50
    player(yours.X, yours.Y)
    show_score(TextX, TextY)
    pygame.display.update()
