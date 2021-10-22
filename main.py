import pygame
import numpy as np
from Ball import Ball
from functions import *


class App:
    def __init__(self):
        self.width = 1080
        self.height = 720
        self.window = pygame.display.set_mode((self.width, self.height))
        self.title = "Ball kinematics"
        pygame.display.set_caption(self.title)

        self.mousePos = np.array([0, 0], dtype="float")
        self.mouseDown = False
        self.mouseUp = False

        self.run = True

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.ball = None

        self.vel = None
        self.showVel = False

    def start(self):
        self.ball = Ball(np.array([600, 300], dtype="float"), 10, np.array([0, 0], dtype="float"))

    def update(self):
        self.clock.tick(self.fps)
        if distance(self.mousePos, self.ball.pos) <= self.ball.rad:
            self.ball.selected = True
        else:
            self.ball.selected = False

        if self.mouseDown and self.ball.selected:
            self.vel = self.ball.pos
            self.showVel = True
        if self.vel is not None and self.mouseUp:
            self.ball.vel = (self.vel - self.mousePos) * 10
            self.vel = None
            self.showVel = False

        # update ball
        self.ball.update(self.clock.get_time() / 1000)
        if self.ball.pos[0] >= self.width - 20 or self.ball.pos[0] <= 20:
            self.ball.vel[0] = - self.ball.vel[0]
        if self.ball.pos[1] >= self.height - 20 or self.ball.pos[1] <= 20:
            self.ball.vel[1] = - self.ball.vel[1]

        self.ball.vel -= self.ball.vel / 20

    def render(self):
        self.window.fill((0, 0, 0))

        # Borders
        pygame.draw.rect(self.window, (255, 187, 0), (0, 0, self.width, 20))
        pygame.draw.rect(self.window, (255, 187, 0), (0, self.height - 20, self.width, 20))
        pygame.draw.rect(self.window, (255, 187, 0), (0, 0, 20, self.height))
        pygame.draw.rect(self.window, (255, 187, 0), (self.width - 20, 0, self.width, self.height))

        # draw ball(s)
        if self.ball.selected:
            pygame.draw.circle(self.window, (255, 255, 255), self.ball.pos, self.ball.rad+3)

        if self.showVel:
            pygame.draw.line(self.window, (255, 255, 255), self.vel, self.mousePos, 2)

        pygame.draw.circle(self.window, (255, 0, 0), self.ball.pos, self.ball.rad)

        # update window
        pygame.display.update()

    def eventManager(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            elif e.type == pygame.MOUSEMOTION:
                self.mousePos = np.array([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]], dtype="float")
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.mouseDown = True
                self.mouseUp = False
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.mouseUp = True
                self.mouseDown = False


app = App()

app.start()

while app.run:
    app.update()
    app.render()
    app.eventManager()
