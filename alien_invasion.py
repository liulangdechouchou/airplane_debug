#导入pygame库时，需要把工程文件夹下的D:\python_work\venv\pyvenv.cfg中false改成true
import sys

import pygame

from settings import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
# from alien import Alien
from game_stats import GameStats
from button import Button
import bullet
def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height)
    )
    # caption ：标题
    pygame.display.set_caption("Alien chou")
    # 创建按钮
    play_button = Button(ai_settings,screen,'Pay')
    ship = Ship(ai_settings,screen)
    # 创建外星人的空编组
    aliens = Group()
    # 创建一个用于存储子弹的编组
    # Group类 类似于列表，但提供了有助于开发游戏的额外功能，了解即可class 'pygame.sprite.Group
    bullets = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings,screen,aliens,ship)
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    #开始游戏的 主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens)
        if stats.game_active:
            ship.update()

            gf.update_bullets(ai_settings,aliens,bullets,screen,ship)
            gf.update_aliens(ai_settings, aliens,ship,stats,screen,bullets)
        gf.update_screen(ai_settings,screen,ship,bullets,aliens,stats,play_button)
run_game()