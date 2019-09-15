import pygame.font
from pygame.sprite import Group
from ship import Ship
class Scoreboard():
    def __init__(self,ai_settings,screen,stats):
        # 初始化显示得分涉及的属性？(PS:这个套路和开始按钮很像)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # 字体
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont("arial",48) # 实例化了字体对象
        #准备初始得分图像
        self.pre_score()
        self.pre_high_score()
        self.pre_level()
        # 创建一个可以显示的飞船编组
        self.pre_ships()
    def pre_score(self):
        """得分转图像"""
        # 取10的整数倍（用round）
        rounded_score = round(self.stats.score,-1)
        # 字符串格式设置指令format，额外学习，这里{,:}是插入逗号
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render("score:"+score_str,True,self.text_color,self.ai_settings.bg_color)
        # 得分放在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    def show_score(self):
        # 没有screen.blit，图像是不会出现的
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    def pre_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("highest:"+high_score_str, True, self.text_color, self.ai_settings.bg_color)
        # 得分放在右上角
        self.high_score_rect = self.high_score_image.get_rect()

        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20
    def pre_level(self):
        self.level_image = self.font.render("level:"+str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        # 等级放在得分下方
        self.level_rect = self.level_image.get_rect()

        self.level_rect.left = self.screen_rect.left+5
        self.level_rect.top = 20
    def pre_ships(self):
        """显示还有多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10 + ship_number*ship.rect.width
            ship.rect.bottom = self.screen_rect.bottom
            # self.rect.centerx = self.screen_rect.centerx
            # self.rect.centery = self.screen_rect.centery
            # self.rect.bottom = self.screen_rect.bottom
            self.ships.add(ship)