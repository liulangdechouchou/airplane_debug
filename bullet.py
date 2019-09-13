import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
    """对飞船发射的子弹进行管理的类"""

    def __init__(self,ai_settings,screen,ship):
        super().__init__()
        self.screen = screen
        # 在（0,0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """ 移动子弹"""
        self.y -= self.speed_factor
        self.rect.y = self.y # 这两句本质就是做一个小数的问题。类似self.rect.y -=self.speed_factor

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)