import pygame
from pygame.locals import *
from random import randint
import time
sizet=40

class apple():
  def __init__(self,p_surface):
     self.p_surface=p_surface
     self.image=pygame.image.load("apple.jpg").convert()
     self.x=sizet*2
     self.y=sizet*2
  def draw(self):
     
     self.p_surface.blit(self.image,(self.x,self.y))
     pygame.display.flip()

  def move(self):
      self.x=randint(0,15)*sizet
      self.y=randint(0,15)*sizet
class snake():
    
    def __init__(self,p_surface,lent):
        self.lent=lent
        self.p_surface=p_surface
        self.x=[sizet]*lent
        self.y=[sizet]*lent
        self.block=pygame.image.load("block.jpg").convert()
        self.direction='right'
    def draw(self):
         self.p_surface.fill((0,128,0), rect=None, special_flags=0)
         for i in range(self.lent):
           self.p_surface.blit(self.block,(self.x[i],self.y[i]))
         pygame.display.flip()
    def increase(self):
         self.lent+=1
         self.x.append(-1)
         self.y.append(-1)
    def up(self):
        self.direction='up'
    def down(self):
        self.direction='down'
    def left(self):
        self.direction='left'
    def right(self):
        self.direction='right'
    def move(self):
      for i in range(self.lent-1,0,-1):
         self.x[i]=self.x[i-1]
         self.y[i]=self.y[i-1]
    
      if self.direction=='left':
        self.x[0]-=sizet
        self.draw()
        if self.x[0]<0:
            raise "over"
          
        
      if self.direction=='right':
        self.x[0]+=sizet
        self.draw()
        if self.x[0]>800:
            raise "over"
      if self.direction=='up':
        self.y[0]-=sizet
        self.draw()
        if self.y[0]<0:
            raise "over"
        
      if self.direction=='down':
        self.y[0]+=sizet
        self.draw()
        if self.y[0]>800:
            raise"over"
        

class game():
    t=0.4
    def __init__(self):
          pygame.init()
         
          pygame.mixer.init()
          self.surface=pygame.display.set_mode((800,800))
          self.surface.fill((0,128,0), rect=None, special_flags=0)
          self.snake=snake(self.surface,2)
          self.snake.draw()
          self.apple=apple(self.surface)
          self.apple.draw()
    def is_collision(self,x1,y1,x2,y2):
          if x1>=x2 and x1<x2+sizet:
            if y1>=y2 and y1<y2+sizet:
              return True
          return False
    def score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.lent*2}",True,(255,255,255))
        self.surface.blit(score,(600,10))
        pygame.display.flip()
    def music(self,name):
      if name == "crash":
            sound = pygame.mixer.Sound("over.wav")
      elif name == 'ding':
            sound = pygame.mixer.Sound("sucess.mp3")

      pygame.mixer.Sound.play(sound)
    def game_over(self):
        self.surface.fill((0,128,0), rect=None, special_flags=0)
        font = pygame.font.SysFont('arial',30)
        score1 = font.render(f"Game over!!!Your score is : {self.snake.lent*2}",True,(255,0,0))
        self.surface.blit(score1,(200,300))
        score2 = font.render(f"To restart the game press enter key",True,(255,0,0))
        self.surface.blit(score2,(200,350))
        pygame.display.flip()
        


    def play(self):
      
      self.snake.move()
      self.apple.draw()
      if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
           self.apple.move()
           self.snake.increase()
           self.music('ding')
           
      for i in range(3,self.snake.lent):  
         if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
             
             raise "over"
      self.score()
      pygame.display.flip()
    def speed(self,t):
      if self.t>0:
        time.sleep(t)
      
      
    def reset(self):
          self.snake=snake(self.surface,2)
          self.snake.draw()
          self.apple=apple(self.surface)
          self.apple.draw()
          self.play()
          pause=False
    def run(self):
          run=True
          pause=False
          while run:
             for event in pygame.event.get():
               if event.type==KEYDOWN:
                  if event.key==K_ESCAPE:
                       run=False
                  if event.key==K_RETURN:
                       pause=False
                       self.reset()
                  if not pause:
                 
                    if event.key==K_UP:
                             self.snake.up()
                    if event.key==K_DOWN:
                            self.snake.down()
                    if event.key==K_LEFT:
                              self.snake.left()
                    if event.key==K_RIGHT:
                            self.snake.right() 
               elif event.type==QUIT:
                   run=False
             try:
               if not pause:
                 self.play()
             except Exception as e:
               self.game_over()
               self.music('crash')
               pause=True
             time.sleep(0.2)
  
             





if __name__=='__main__':
    g=game()
    g.run()
    