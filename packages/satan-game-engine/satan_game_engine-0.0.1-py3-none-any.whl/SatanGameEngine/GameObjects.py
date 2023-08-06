import pygame as pg
from SatanGameEngine.Colors import *
import time

class Rect:
    def __init__(self, window, x=0, y=0, width=0, height=0, color=COLOR.WHITE, image=None):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image

    def draw(self):
        if self.image:
            self.window.blit(self.image, (self.x, self.y))
        else:
            pg.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        pass

    def handle_input(self):
        pass

    def get_new_pos(self):
        # Return the updated position
        return (self.x, self.y)

class Player(Rect):
    def __init__(self, window, x=0, y=0, width=0, height=0, color=COLOR.WHITE, speed=1, can_sprint=True, sprint_multiplier=2, image=None):
        super().__init__(window, x, y, width, height, color)
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        self.keys = []

        self.velocity_x = 0  # Velocity in x direction
        self.velocity_y = 0  # Velocity in y direction
        self.speed = speed
        self.can_sprint = can_sprint
        self.sprinting = False
        self.sprint_multiplier = sprint_multiplier  # Speed multiplier when sprinting

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def handle_input(self):
        self.keys = pg.key.get_pressed()

        if self.keys[pg.K_w]:
            self.velocity_y = -self.speed
        elif self.keys[pg.K_s]:
            self.velocity_y = self.speed
        else:
            self.velocity_y = 0

        if self.keys[pg.K_a]:
            self.velocity_x = -self.speed
        elif self.keys[pg.K_d]:
            self.velocity_x = self.speed
        else:
            self.velocity_x = 0

        if self.keys[pg.K_LSHIFT]:
            if self.can_sprint == True:
                self.sprinting = True
                self.speed = self.sprint_multiplier
            else:
                self.sprinting = False
                self.speed = 1
        else:
            self.sprinting = False
            self.speed = 1

class Background(Rect):
    def __init__(self, window, image=None):
        super().__init__(window, 0, 0, window.get_width(), window.get_height())
        self.image = image

    def draw(self):
        if self.image:
            self.window.blit(self.image, (0, 0))
        else:
            super().draw()
