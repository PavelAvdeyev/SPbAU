# -*- coding: utf-8 -*-

import pygame
import sys
from pygame.locals import *
from random import randint

from config import *
from sprites import Rectangle, Button, TextSprite, StartLine, Doodle, Platform, BasicPlatform, MovingPlatform, CrashingPlatform, Spring


class Location(object):

  def __init__(self, parent):
    self.window = pygame.display.get_surface()
    self.background = pygame.image.load('img/background.png').convert()
    self.parent = parent

  def event(self,event):
    pass

  def draw(self):
    pass

#Main menu
class StartLocation(Location):
    
  def __init__(self, parent):
    Location.__init__(self, parent)

    pygame.mouse.set_visible(True)
    pygame.key.set_repeat(False)

    self._startbtn = Button(screen_width // 2, screen_width // 3, "Start")
    self._exitbtn = Button(screen_width // 2, screen_width // 3 + 70, "Exit")

    self._controls = pygame.sprite.Group()
    self._controls.add(self._startbtn)
    self._controls.add(self._exitbtn)

    self._controls_captions = pygame.sprite.Group()
    self._controls_captions.add(self._startbtn.get_text_sprite())
    self._controls_captions.add(self._exitbtn.get_text_sprite())

    self.window.blit(self.background, (0, 0))
        
  def draw(self):
    self._controls.clear(self.window, self.background)
    self._controls.draw(self.window)
    self._controls_captions.draw(self.window)
    
  def event(self, event):
    if event.type == MOUSEMOTION:
      for btn in self._controls:
        btn.change_state(btn.rect.collidepoint(pygame.mouse.get_pos()))
    elif event.type == MOUSEBUTTONUP:
      if self._startbtn.rect.collidepoint(pygame.mouse.get_pos()):
        self.parent.location = GameLocation(self.parent, "Player")
      elif self._exitbtn.rect.collidepoint(pygame.mouse.get_pos()):
        sys.exit()
    
#Game menu
class GameLocation(Location):

  def __init__(self, parent, name):
    Location.__init__(self, parent)
    pygame.key.set_repeat(10)
    pygame.mouse.set_visible(0)

    self.doodle = Doodle(name, screen_width // 2, screen_height - 120)
    self.allsprites = pygame.sprite.Group()
    self.allsprites.add(self.doodle)

    self.start_line = StartLine(screen_width // 2, screen_height - 40)
    self.is_remove_start_line = True
    self.allsprites.add(self.start_line)

    self.platforms = []
    self.springs = []
    for i in range(0, platform_count):
      platform = self._random_platform(False)
      self.platforms.append(platform)
      self.allsprites.add(platform)
      if platform.get_spring() != None: 
        self.springs.append(platform.get_spring())
        self.allsprites.add(platform.get_spring())

    self.score_sprite = TextSprite(50, 25, self.doodle.name, 45, (0,0,0))
    self.allsprites.add(self.score_sprite)
    self.header = Rectangle(screen_width, 50, (0, 191, 255, 128))
    self.window.blit(self.background, (0, 0))
        
  def _random_platform(self, top = True):
    x = randint(platform_width, screen_width - platform_width)
    bad_y = []
    for spr in self.allsprites:
      bad_y.append((spr.y - platform_y_padding, spr.y + platform_y_padding + spr.rect.height))
        
    good = False
    for i in range(0, 10):
      if top:
        y = randint(-40, 30)
      else:
        y = randint(0, screen_height)
      good = True
      for bad_y_item in bad_y:
        if bad_y_item[0] <= y <= bad_y_item[1]:
          good = False
          break
      if good: 
        break
            
    dig = randint(0, 100)
    if dig <= 30:
      return MovingPlatform(x, y)
    elif dig > 30 and dig <= 60:
      return CrashingPlatform(x, y)
    else:
      return BasicPlatform(x, y)
  
  def _update_platforms(self): 
    for spr in self.platforms: 
      if self.doodle.get_legs_rect().colliderect(spr.get_surface_rect()) and self.doodle.get_y_speed() <= 0: 
        spr.crash()            
        self.doodle.set_y_speed(jump_speed)
          
      spr.move()
      
      if spr.y >= screen_height:
        self.allsprites.remove(spr)
        self.platforms.remove(spr)

        if spr.get_spring() != None:
          self.springs.remove(spr.get_spring())
          self.allsprites.remove(spr.get_spring())

        platform = self._random_platform()

        self.platforms.append(platform)
        self.allsprites.add(platform)
        if platform.get_spring() != None:
          self.springs.append(platform.get_spring()) 
          self.allsprites.add(platform.get_spring())
       
  def _update_springs(self): 
    for spr in self.springs: 
      if self.doodle.get_legs_rect().colliderect(spr.get_top_surface()) and self.doodle.get_y_speed() <= 0:
        spr.compress()
        self.doodle.set_y_speed(spring_speed)
  
  def _update_scores(self): 
    if self.doodle.y < screen_height // 2:
      self.doodle.inc_score(self.doodle.get_y_speed())
      for spr in self.allsprites:
        if not isinstance(spr, TextSprite):
          spr.move_y(self.doodle.get_y_speed())
   
  def _update_start_line(self):
    if self.is_remove_start_line: 
      if self.doodle.get_legs_rect().colliderect(self.start_line.get_surface_rect()) and self.doodle.get_y_speed() <= 0: 
        self.doodle.set_y_speed(jump_speed)
      
      if self.start_line.y >= screen_height:
        self.allsprites.remove(self.start_line)
        self.is_remove_start_line = False
                         
  def draw(self):
    if self.doodle.is_live():
      self.allsprites.clear(self.window, self.background)  
      self.doodle.inc_y_speed(-gravitation)

      if self.doodle.x < 0:
        self.doodle.set_x(screen_width)
      elif self.doodle.x > screen_width:
        self.doodle.set_x(0)        
      self.doodle.move_y(-self.doodle.get_y_speed())

      self._update_platforms()
      self._update_springs()
      self._update_start_line()
      self._update_scores()
      
      self.allsprites.draw(self.window)
      self.score_sprite.set_text("               %s,    %s" % (self.doodle.get_name(), int(self.doodle.get_score() // 10)))
      self.window.blit(self.header, (0,0))
    else:
      self.parent.location = GameLocation(self.parent, self.doodle.get_name())
      

  def event(self, event):
    if event.type == KEYDOWN:
      if event.key == K_LEFT:
        self.doodle.set_x(self.doodle.x - 10)
      elif event.key == K_RIGHT:
        self.doodle.set_x(self.doodle.x + 10)
            


