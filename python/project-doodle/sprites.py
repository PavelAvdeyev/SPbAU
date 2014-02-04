# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import randint

from config import *

class Rectangle(pygame.Surface):
  def __init__(self, width, heigth,color):
    pygame.Surface.__init__(self,(width, heigth), pygame.SRCALPHA)
    self.fill(color)

class Sprite(pygame.sprite.Sprite):
  def __init__(self, x = 0, y = 0):
    pygame.sprite.Sprite.__init__(self)
    self.x = x
    self.y = y
        
  def move_x(self, x):
    self.x = self.x + x
    self._move()
    
  def move_y(self, y):
    self.y = self.y + y
    self._move()
        
  def set_x(self, x):
    self.x = x
    self._move()
    
  def set_y(self, y):
    self.y = y
    self._move()
        
  def _move(self):
    self.rect.center = (self.x, self.y)

  def set_image(self, img): 
    self.image = img
    self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)
 
  def init_image(self, imgPath):
    self.image = pygame.image.load(imgPath).convert()
    self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)
        

class Button(Sprite):
  def __init__(self, x, y, text):
    Sprite.__init__(self, x, y)        
    self._img_sel = pygame.image.load('img/menu_selected.png').convert()
    self._img_unsel = pygame.image.load('img/menu_unselected.png').convert()
    self.textSprite = TextSprite(self.x, self.y, text)
    self.change_state(False)
        
  def change_state(self, state):
    if state == False:
      self.set_image(self._img_unsel)
      self.textSprite.set_color((255, 165, 149))
    elif state == True:
      self.set_image(self._img_sel)
      self.textSprite.set_color((243, 227, 200))
 
  def get_text_sprite(self):
    return self.textSprite 
  
        
class TextSprite(Sprite):
  def __init__(self, x, y, text = '', size = 35, color = (255, 255, 255)):
    Sprite.__init__(self, x, y)        
    self._font = pygame.font.Font(None, size)  
    self._font_color = color  
    self._text = text
    self._generate_image() 
 
  def set_text(self, text):
    self._text = text
    self._generate_image()

  def set_color(self, color):
    self._font_color = color
    self._generate_image()

  def set_size(self, size):
    self._font = pygame.font.Font(None, size)
    self._generate_image()
    
  def _generate_image(self):
    self.image = self._font.render(self._text, True, self._font_color)
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)
                
class Doodle(Sprite):

  def __init__(self, name = "Anonymus", x = 0, y = 0):
    Sprite.__init__(self, x, y)

    self.img_r = pygame.image.load('img/doodle.gif').convert()
    self.img_l = pygame.transform.flip(self.img_r, True, False) 

    self.name = name
    self.live = True 
    self.y_speed = 5
    self.score = 0
    self.set_image(self.img_r)

  def get_legs_rect(self):
    return pygame.Rect(self.rect.left + self.rect.width * 0.1, self.rect.top + self.rect.height * 0.9, self.rect.width * 0.6, self.rect.height * 0.1)

  def is_live(self): 
    return self.live		

  def get_name(self):
    return self.name
 
  def get_score(self):
    return self.score

  def get_y_speed(self): 
    return self.y_speed
  
  def set_y_speed(self, speed): 
    self.y_speed = speed 
   
  def set_x(self, x):
    if x < self.x:
      self.set_image(self.img_l)
    elif x > self.x:
      self.set_image(self.img_r)
    self.x = x
    
  def inc_y_speed(self, speed):
    self.y_speed = self.y_speed + speed
    
  def inc_score(self, score):
    self.score = self.score + score
  
  def _move(self):
    Sprite._move(self)
    if self.y >= screen_height:
      self.live = 0     
    
        
class StartLine(Sprite):
  def get_surface_rect(self):
    return pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height * 0.1)
    
  def __init__(self, x, y):
    Sprite.__init__(self, x, y)
    self.init_image('img/line.png')

class Platform(Sprite):
  def get_surface_rect(self):
    return pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height * 0.1)

  def __init__(self, x, y): 
    Sprite.__init__(self, x, y)
    self.spring = None

  def get_spring(self): 
    return self.spring 

  def move(self): 
    pass

  def crash(self): 
    pass     

class BasicPlatform(Platform): 
  def __init__(self, x, y):
    Platform.__init__(self, x, y)
    self.init_image('img/lightgreyplatform.gif')
    if randint(-50, 50) >= 0:
      self.spring = Spring(self.x + randint(-int(platform_width // 2 - 10), int(platform_width // 2) - 10), self.y - 20)
    else:
      self.spring = None
             
class MovingPlatform(Platform):
  def __init__(self, x, y):
    Platform.__init__(self, x, y)
    self.init_image('img/blackplatform.gif')    
    self._way = -1 
    self._xSpeed = randint(2, 6)

  def move(self):
    self.move_x(self._xSpeed * self._way)
    if 10 < self.x < 19 or (screen_width - 20) < self.x < (screen_width - 11):
      self._way = -self._way
    
class CrashingPlatform(Platform):
  def __init__(self, x, y):
    Platform.__init__(self, x, y)
    self.init_image('img/greyplatform.gif')
    self._ySpeed = 10
    self._crashed = False
    
  def crash(self):
    self._crashed = True
    self.init_image('img/greyplatformbr.gif')
    
  def move(self):
    if self._crashed == True:
      self.move_y(self._ySpeed)
    
  def renew(self):
    Platform.renew(self)
    self._crashed = False
    self.init_image('img/brownplatform.gif')
      
class Spring(Sprite):
  def get_top_surface(self):
    return pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height * 0.1)
  
  def __init__(self, x, y):
    Sprite.__init__(self, x, y)
    self._compressed = False
    self.init_image('img/spring.png')
      
  def compress(self):
    self._compressed = True
    self.init_image('img/spring_comp.png')
    
            


        
