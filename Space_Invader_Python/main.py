import pygame
import random
import math
from pygame import mixer

pygame.init()  # intitialize pygame!

# Load screen
screen = pygame.display.set_mode((800, 600))  # Weight and height (px)

# Load Background
background = pygame.image.load("space-galaxy-background.jpg")

# Window title & Icon
pygame.display.set_caption("Alien Invader")
winicon = pygame.image.load('ufo.png')
pygame.display.set_icon(winicon)

# Player Icon
playerimg = pygame.image.load('space-invaders.png')
playerL = 370
playerU = 480
playerL_change = 0  # change that you want in L

alienimg = []
alienL = []
alienU = []
alienL_change = []
alienU_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    alienimg.append(pygame.image.load("alien.png"))
    alienL.append(random.randint(0,736))
    alienU.append(random.randint(50,175))
    alienL_change.append(0.5) # speed of alien
    alienU_change.append(30)

# Rocket Icon
rocketimg = pygame.image.load('bomb.png')
rocketL = 0
rocketU = 480
rocketU_change = 2
rocket_state = "ready"

# Score
score_Value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10 
textY = 10

# End Game Message
over_text = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x,y):  
    score = font.render("UFOs Destroyed: " + str(score_Value), True, (255,255,255))
    screen.blit(score, (x, y))

def end_game_text(x, y):
    end_text = over_text.render("GAME OVER", True, (255,0,0))
    screen.blit(end_text, (200,250))

def player(x, y):
    screen.blit(playerimg, (x, y))


def alien(x, y, i):
    screen.blit(alienimg[i], (x, y))

def fire_rocket(x, y):
    global rocket_state
    rocket_state = "fire"
    screen.blit(rocketimg, (x+16,y+10)) # Places rocket in spaceship

def isCollision(alienL, alienU, rocketL, rocketU):
    distance = math.sqrt(math.pow(alienL-rocketL, 2)) + (math.pow(alienU-rocketU, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
# Quit event
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            print("Key is pressed")
            if event.key == pygame.K_a:
                print("'A' key is pressed")
                playerL_change = -0.5

            if event.key == pygame.K_d:
                print("'D' key is pressed")
                playerL_change = 0.5

            if event.key == pygame.K_SPACE:
                if rocket_state is "ready": # checks if bullet is on screen
                    rocket_sound = mixer.Sound("laser.wav")
                    rocket_sound.play()
                    rocketL = playerL
                    fire_rocket(playerL,rocketU) # fires rocket at player's x coordinate

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                print("Key is released")
                playerL_change = 0

    # red, green, and blue
    screen.fill((0, 0, 128))

    # Establish Background
    screen.blit(background, (0,0))

    playerL += playerL_change
    if playerL <= 0:
        playerL = 0
    elif playerL >= 736:
        playerL = 736

    # Alien movement
    for i in range(num_of_enemies):

        # End Game
        if alienU[i] > 400:
            for x in range(num_of_enemies):
                alienU[x] = 2000
            end_game_text(250, 250)
            break

        alienL[i] += alienL_change[i]
        if alienL[i] <= 0:
            alienL_change[i] = 0.35
            alienU[i] += alienU_change[i]
        elif alienL[i] >= 736:
            alienL_change[i] = -0.35
            alienU[i] += alienU_change[i]

         # Collision
        collision = isCollision(alienL[i], alienU[i], rocketL, rocketU)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            rocketU = 480
            rocket_state = "ready"
            score_Value += 1
            print(score_Value)
            alienL[i] = random.randint(0,736)
            alienU[i] = random.randint(50,150)

        alien(alienL[i], alienU[i], i)

    # Rocket Movement
    if rocketU <= 0: # If rocket passes screen, rocket resets
        rocketU = 480
        rocket_state = "ready"

    if rocket_state is "fire":
        fire_rocket(rocketL, rocketU)
        rocketU -= rocketU_change

    player(playerL, playerU)
    show_score(textX,textY)
    pygame.display.update()
