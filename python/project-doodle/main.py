#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys

from locations import *
from sprites import *

from config import screen_width, screen_height, fps


class Game():
  def __init__(self):
    pygame.init()
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Vader jump')
    self.location = StartLocation(self)
 
  def play(self): 
    clock = pygame.time.Clock()
    while True:
      clock.tick(fps)
      self.location.draw()
      pygame.display.flip()
      for event in pygame.event.get():
        self.location.event(event)
        self.event(event)            
 
  def event(self, event):
    if event.type == QUIT:
      sys.exit()
    elif event.type == KEYUP:
      if event.key == K_ESCAPE:
        if isinstance(self.location, GameLocation):
          self.location = StartLocation(self)
        elif isinstance(self.location, StartLocation):
          sys.exit()
                
if __name__ == "__main__":
  game = Game()
  game.play()  

