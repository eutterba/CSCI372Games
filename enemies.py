import pygame
import random
pygame.init()
win_height=400
win_width=800
win=pygame.display.set_mode((win_height,win_width))

class enemies:
    def __init__(self, difficulty, x, y, width,height):
        if(x>0):
            vel=-(difficulty)
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hitbox=(self.x, self.y, 64,64)

        score=difficulty*100
    def draw(self,win):
        self.hitbox=(self.x, self.y, 64, 64)
        pygame.draw.rect(win,(0,0,0),self.hitbox, 1)
        
