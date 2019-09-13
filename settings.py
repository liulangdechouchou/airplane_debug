import pygame
class Settings():
    #存储《外星人入侵》的所有设置的类


    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        # 飞船的设置
        self.ship_speed_factor = 1.5
        # 子弹的设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60 # self.bullet_color类型是元祖
        self.bullet_allowed = 20
        self.alien_speed_factor = 1
        self.fleet_drop_speed =10
        # 1表示右移
        self.fleet_direction = 1
        self.ship_limit = 3
        # 加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings() # dynamic 动态的意思，这个函数是动态参数设置
    def initialize_dynamic_settings(self):
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        self.ship_speed_factor = 1.5
        self.fleet_direction = 1
    def increase_speed(self):
        # 提速
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale