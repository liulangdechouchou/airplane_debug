import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    """单个外星人"""
    def __init__(self,ai_settings,screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image,self.rect)


    def check_edge(self):
        # 碰到屏幕边缘
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):

        #self.x+=(self.ai_settings.alien_speed_factor)
        self.x+=(self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction)
        # 这么折腾一下，还是为了保存小数
        self.rect.x = self.x # 改变self.rect.x才是真的改变了这个实例的x轴坐标，self.x不行
