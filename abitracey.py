# A Bit Racey
# Game By Micah Perteet
# (C) 2020
# imports
import json
import random
import time
import pygame

# pygame init
pygame.init()

# set the size of the display
display_width = 800
display_height = 600

# colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
dark_red = (155,0,0)
green = (0,255,0)
dark_green = (0,155,0)
blue = (0,0,255)

# the size of the car
car_width = 75

# set the display
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("A bit Racey")
clock = pygame.time.Clock()

# load sounds
crash_sound = pygame.mixer.Sound("crash.wav")

# load the car img
carImg = pygame.image.load("car.png")
video = pygame.movie.Movie("video.mp4")
video.set_display(gameDisplay)


# functions 
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count) + "Highscore: " + str(game["highscore"]), True, black)
    gameDisplay.blit(text, (0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    
def car(x,y):
    gameDisplay.blit(carImg,(x,y))
def button(text, textx, texty, textcolor, textsize, butnx, butny, butninactinvecolor, butnactivecolor, butnw, butnh):
    mouse = pygame.mouse.get_pos()
    if butnx + butnw > mouse[0] > butnx and butny + butnh > mouse[1] > butny:
        pygame.draw.rect(gameDisplay, butnactivecolor, (butnx,butny,butnw,butnh))
    else:
        pygame.draw.rect(gameDisplay, butninactinvecolor, (butnx,butny,butnw,butnh))
    message_display(text, textx, texty, False, False, textcolor, textsize)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def crash():
    message_display("You Crashed", 400, 300, True, True, red, 115)
    pygame.mixer.Sound.play(crash_sound)

def message_display(text, x, y, wait, game, color, size):
    largeText = pygame.font.Font("freesansbold.ttf", size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    if wait:
        time.sleep(4)
    if game:
        game_loop()

# the game intro
def game_intro():

    intro = True
    gameDisplay.fill(white)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                quit()
        largeText = pygame.font.Font("freesansbold.ttf", 115)
        TextSurf, TextRect = text_objects("A Bit Racey", largeText, blue)
        TextRect.center = (400, 100)
        gameDisplay.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 150 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(gameDisplay, green, (150,450,100,50))
            if click[0] == 1:
                game_loop()
        else:
            pygame.draw.rect(gameDisplay, dark_green, (150,450,100,50))
        message_display("Start", 195, 475, False, False, black, 30)
        if 550 + 100 > mouse[0] > 550 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(gameDisplay, red, (550,450,100,50))
            if click[0] == 1:
                intro = False
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(gameDisplay, dark_red, (550,450,100,50))
        message_display("Quit", 595, 475, False, False, black, 30)

        pygame.display.update()
        clock.tick(60)

# the main gameloop      
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    score = 0
    
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
    gameExit = False
    highscore = open("highscore", "r")
    game = json.load(highscore)
    highscore.close()
    .play()


    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                    
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_ESCAPE:
                    game_intro()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        
        gameDisplay.fill(white)


        things(thing_startx, thing_starty, thing_width, thing_height, blue)
        thing_starty += thing_speed
        car(x,y)
        font = pygame.font.SysFont(None, 25)
        text = font.render("Dodged: " + str(score) + ", " + "Highscore: " + str(game["highscore"]), True, black)
        gameDisplay.blit(text, (0,0))

        if x > display_width - car_width or x < 0:
            if score > game["highscore"]:
                highscore = open("highscore", "w")
                game["highscore"] = score
                savescore = json.dumps(game)
                highscore.write(savescore)
                highscore.close()
            crash()
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width - thing_width)
            score += 1
            thing_width += 8
            thing_speed += 0.8
            

        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:  
                if score > game["highscore"]:
                    highscore = open("highscore", "w")
                    game["highscore"] = score
                    savescore = json.dumps(game)
                    highscore.write(savescore)
                    highscore.close()
                    message_display("New Highscore!", 400, 150, True, False, black, 40)
                crash()
        pygame.display.update()
        clock.tick(60)
# starting the intro
game_intro()
pygame.quit()
quit()
