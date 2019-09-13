import pygame
class Ship():
    def __init__(self,ai_settings,screen):
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('../images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 放置在屏幕底部居中
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    def blitme(self):
        # “在指定位置绘制飞船”
        self.screen.blit(self.image,self.rect)
    def update(self):
        # self.rect.right 返回飞船外接矩形的右边缘x坐标
        if self.moving_right and self.rect.right <self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
            # self.rect.centerx+=1
        if self.moving_left and self.rect.left >0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top >0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        # centerx是飞船中心的x坐标
        self.rect.centerx = self.center
        self.rect.centery = self.centery
    def center_ship(self):
        # 复位飞船
        # self.center = self.screen_rect.centerx
        self.rect.centerx = self.screen_rect.centerx
        # self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom
        self.center = self.rect.centerx
        self.centery = self.rect.centery