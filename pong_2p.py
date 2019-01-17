# imports necessary modules
import pygame
from pygame.locals import *
from random import choice

pygame.init()  # initializes pygame module and different elements and variables for the game
height = 800
width = 800
screen = pygame.display.set_mode((width, height), FULLSCREEN)
arena = Rect(0, 0, height, width)  # the game's court
centerline = Rect(width/2, 0, 1, width)  # the game's court's centerline


def update_scores(b, p1, p2):  # updates the scores of 2 players by using the ball's x value if the ball isn't in-game

    if b.rect.x < 10 and not b.check_ig():
        p2.score += 1
        p2.reset()
        p1.reset()

    if b.rect.x > 0 and not b.check_ig():
        p1.score += 1
        p1.reset()
        p2.reset()


class Ball(object):
    # this is a class used to create the game's ball
    # it contains the necessary functions related to the ball

    def __init__(self):  # initializes the ball object
        self.rect = Rect(width/2-7, height/2-7, 15, 15)  # the ball's rectangle that is drawn to the screen
        self.vely = choice([5, -5])  # the ball's velocity on the y axis
        self.velx = choice([5, -5])  # the ball's velocity on the y axis

    def draw(self):  # draws the ball to the screen
        pygame.draw.rect(screen, [255, 255, 255], self.rect)

    def move(self, p1, p2):  # moves the ball according to it's velocity on the x and y axii and makes it bounce
        self.rect.move_ip(self.velx, self.vely)

        # Check for collisions with border
        if self.rect.x < 0 or self.rect.x > width:
            self.velx = -self.velx
        if self.rect.y < 0:
            self.vely = abs(self.vely)
        elif self.rect.y > width:
            self.vely = -abs(self.vely)

        # Check for collisions with players
        if self.rect.colliderect(p1):
            self.vely = (self.rect.centery - p1.rect.centery)*0.1
            self.velx = abs(self.velx)
        elif self.rect.colliderect(p2):
            self.vely = (self.rect.centery - p2.rect.centery)*0.1
            self.velx = -abs(self.velx)
        # Increase velocity
        if abs(self.velx) < 40:
            self.velx *= 1.001

    def check_ig(self, p1=None, p2=None):  # checks if the ball is still in game
        if self.rect.x < 0:  # if player 2 wins
            return False
        elif self.rect.x > width:  # if player 1 wins
            return False
        else:
            return True


class Pong(object):
    # this is a class used to create the game's players
    # it contains the necessary functions related to the players

    def __init__(self, name, posx, posy, bot=True):  # initializes the object
        self.name = name  # the player's name (a 'str' object)
        self.posx = posx  # the player's postion on the x axis
        self.posy = posy  # the player's positon on the y axis
        self.rect = Rect(self.posx, self.posy-100, 20, 200)  # the player's racket that is drawn
        self.score = 0  # the player's score
        self.scorefont = pygame.font.SysFont(name, 40)  # the player's font that is used to render and draw the score
        self.bot = bot  # true if the player is not human (default is true)
        self.win_msg = "{0} wins the round".format(self.name)
        self.msg_font = pygame.font.SysFont("end_msgfont", 40)

    def draw_score(self):  # draws the player's score

        # the temporary surface to which the player's score is rendered
        scoresurface = self.scorefont.render(str(self.score), 0, [255, 255, 255])

        # pastes the surface to the right position on the screen depending on the player's name
        if self.name == "Player 1":
            screen.blit(scoresurface, (width/4, 60))
        elif self.name == "Player 2":
            screen.blit(scoresurface, (width*0.75, 60))

    def reset(self):
        self.rect = Rect(self.posx, self.posy - 100, 20, 200)

    def draw(self):
        pygame.draw.rect(screen, [255, 255, 255], self.rect)
        self.draw_score()

    def handle_keys(self):
        # handles the keys pressed by the user and moves the player's racket up or down accordingly
        if not self.bot:
            if self.name == "Player 1":
                k = pygame.key.get_pressed()
                if k[K_e] and self.rect.y > 0:
                    self.rect.move_ip(0, -9)

                if k[K_d] and self.rect.y < height-200:
                    self.rect.move_ip(0, 9)
            elif self.name == "Player 2":
                k = pygame.key.get_pressed()
                if k[K_UP] and self.rect.y > 0:
                    self.rect.move_ip(0, -9)

                if k[K_DOWN] and self.rect.y < height-200:
                    self.rect.move_ip(0, 9)

    def move(self, bally):
        # moves the player if it isn't human
        if self.bot:
            if bally < self.rect.y+100 and self.rect.y > 5:
                self.rect.move_ip(0, -7)

            if bally > self.rect.y+100 and self.rect.y < height-205:
                self.rect.move_ip(0, 7)

# Initializing players and loop
running = True
player1 = Pong("Player 1", width * 0.02, height / 2, False)
player2 = Pong("Player 2", width * 0.98 - 20, height / 2, False)

while running:  # main game loop
    pygame.Surface.fill(screen, [0, 0, 0])  # clears the screen

    # draws all object in their initial postions at the beginning of the round
    pygame.draw.rect(screen, [255, 255, 255], centerline)
    pygame.draw.rect(screen, [255, 255, 255], arena, 10)
    ball = Ball()
    player1.draw()
    player2.draw()
    ball.draw()
    player1.draw_score()
    player2.draw_score()

    # updates the screen then waits a second
    pygame.display.flip()
    pygame.time.wait(1000)

    # initializes useful variables
    new_round = True
    clock = pygame.time.Clock()

    while new_round:  # starts a new loop at each round

        clock.tick(60)  # sets the tickrate for the game

        # quits the game when necessary
        key = pygame.key.get_pressed()
        if key[K_ESCAPE]:
            running = False
            new_round = False
            break
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                new_round = False
                break

        # clears the screen then draws the court on top of it
        pygame.Surface.fill(screen, [0, 0, 0])
        pygame.draw.rect(screen, [255, 255, 255], centerline)
        pygame.draw.rect(screen, [255, 255, 255], arena, 10)

        # moves then draws each element of the game (players and ball)
        ball.move(player1, player2)
        ball.draw()
        player1.handle_keys()
        player1.move(ball.rect.y)
        player1.draw()
        player2.move(ball.rect.y)
        player2.handle_keys()
        player2.draw()

        # updates the scores
        update_scores(ball, player1, player2)

        # checks if a ball is in game; if not, the round ends
        if not ball.check_ig():
            new_round = False

        # finally refreshes the whole screen
        pygame.display.flip()
