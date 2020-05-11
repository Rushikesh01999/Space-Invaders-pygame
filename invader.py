import pygame
import random
import math
from pygame import mixer

pygame.init()

# display screen (width and height)
screen = pygame.display.set_mode((800, 600))

# chnanging logo bg color and name
pygame.display.set_caption("space invader")

# creating position for player
playerImg = pygame.image.load("player.png")
playerX = 300
playerY = 480
playerX_change = 0

# creating position for enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(5):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(3)
    enemyY_change.append(20)

# creating position for bullet
bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "Ready"

# load background image
background = pygame.image.load("background.jpg")


# Load music
mixer.music.load('music.mp3')
mixer.music.play(-1)
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 82)
textX = 10
textY = 10
over_textX = 180
over_textY = 250


def show_score(X, Y):
    score = font.render("Score" + str(score_value), True, (255, 255, 20))
    screen.blit(score, (X, Y))


def game_over(X, Y):
    game = over_font.render("Game Over", True, (0, 0, 0))
    screen.blit(game, (X, Y))
    show_score(X + 150, Y + 100)


def player(X, Y):
    # blit
    screen.blit(playerImg, (X, Y))


def enemy(X, Y, i):
    screen.blit(enemyImg[i], (X, Y))


def bullet_fire(X, Y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bullet, (X + 16, Y + 10))


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# create infine screen, if not done screen will appear for fraction of sec and then disappear,game loop
running = True
while running:

    screen.fill((0, 0, 0))  # always should appear at top / background color
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # Keystrokes setup for spacceship
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 4
            if event.key == pygame.K_RIGHT:
                playerX_change += 4
            if event.key == pygame.K_SPACE:
                if bullet_state in "Ready":
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Provide barrier so it doesnts go outside boundry
    playerX += playerX_change

    if playerX >= 736:
        playerX = 736
    if playerX <= 0:
        playerX = 0

    # provide movement to the enemy
    for i in range(5):

        if enemyY[i] > 480:
            for j in range(5):
                enemyY[j] = 2000
            game_over(over_textX, over_textY)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] -= 3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] += 3
            enemyY[i] += enemyY_change[i]

        # collision detection
        collisions = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collisions is True:
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1
            print(score_value)

            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 200)

        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"
    if bullet_state in "Fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # calling function
    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
