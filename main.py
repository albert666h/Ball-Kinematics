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
        self.dt = 0

        self.balls = []

        self.vel = None
        self.showVel = False

        self.ballindex = 0

        # Constants
        self.frictionIntensity = 0.2
        self.g = 9.81

    def start(self):

        for i in range(9):
            self.balls.append(Ball(
                np.array([np.random.randint(35, self.width - 35), np.random.randint(35, self.width - 35)],
                         dtype="float"), 20, np.array([0, 0], dtype="float"), 15))

    def update(self):
        self.dt = self.clock.get_time() / 1000
        self.clock.tick(self.fps)

        for i in range(len(self.balls)):
            ball = self.balls[i]
            if distance(self.mousePos, ball.pos) <= ball.rad:
                ball.selected = True
            else:
                ball.selected = False

            if self.mouseDown and ball.selected and self.vel is None:
                self.vel = ball.pos
                self.showVel = True
                self.ballindex = i
            if self.vel is not None and self.mouseUp and self.ballindex == i:
                ball.vel = (self.vel - self.mousePos) * 10

                self.vel = None
                self.showVel = False

            # update balls

            ball.vel -= ball.vel / (self.frictionIntensity * self.g * 10)

            for j in range(len(self.balls)):
                if i != j:
                    kickball = self.balls[j]
                    d = distance(ball.pos, kickball.pos)
                    if d <= ball.rad + kickball.rad:
                        vel = -kickball.pos + ball.pos
                        vel /= sum(np.sqrt(vel*vel))
                        ball.vel += vel * sum(np.sqrt(ball.vel * ball.vel)) / 2
                        kickball.vel -= vel * sum(np.sqrt(ball.vel * ball.vel)) / 2

            ball.update(self.clock.get_time() / 1000)
            if ball.pos[0] + ball.rad >= self.width - 20:
                ball.pos[0] = self.width - 20 - ball.rad
                ball.vel[0] = - ball.vel[0]
            elif ball.pos[0] - ball.rad <= 20:
                ball.pos[0] = 20 + ball.rad
                ball.vel[0] = - ball.vel[0]
            if ball.pos[1] + ball.rad >= self.height - 20:
                ball.vel[1] = - ball.vel[1]
                ball.pos[1] = self.height - 20 - ball.rad
            elif ball.pos[1] - ball.rad <= 20:
                ball.vel[1] = - ball.vel[1]
                ball.pos[1] = 20 + ball.rad

    def render(self):
        self.window.fill((0, 0, 0))

        # Borders
        pygame.draw.rect(self.window, (255, 187, 0), (0, 0, self.width, 20))
        pygame.draw.rect(self.window, (255, 187, 0), (0, self.height - 20, self.width, 20))
        pygame.draw.rect(self.window, (255, 187, 0), (0, 0, 20, self.height))
        pygame.draw.rect(self.window, (255, 187, 0), (self.width - 20, 0, self.width, self.height))

        # draw ball(s)
        for i in range(len(self.balls)):
            if self.balls[i].selected:
                pygame.draw.circle(self.window, (255, 255, 255), self.balls[i].pos, self.balls[i].rad + 3)

            pygame.draw.circle(self.window, (255, 0, 0), self.balls[i].pos, self.balls[i].rad)

        if self.showVel:
            pygame.draw.line(self.window, (255, 255, 255), self.vel, self.mousePos, 2)
            lp = self.vel
            for i in range(int(distance(self.mousePos, self.vel) / 20)):
                ang = angle(self.mousePos, self.vel) * np.pi / 180
                lps = lp
                lp = lp + np.array([np.cos(ang) * 10, -np.sin(ang) * 10])
                pygame.draw.line(self.window, (255, 255, 255), lps, lp, 2)
                lp = lp + np.array([np.cos(ang) * 10, -np.sin(ang) * 10])

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
