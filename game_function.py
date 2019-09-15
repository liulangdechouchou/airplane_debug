"""
game_function本质就是函数收纳器

"""
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
def check_keydown_events(event,ai_settings,screen,ship,bullets,stats, aliens,sb):
    """响应按下键盘"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        # new_bullet是Bullet的一个实例
        fire_bullet(bullets, ai_settings, screen, ship)
    elif event.key == pygame.K_p:
        start_game(stats,aliens,bullets,ship,ai_settings,screen,sb)


# def write_high_score(high_score):
#     high_score

def check_keyup_events(event,ship):
    """响应松开键盘"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_q:
        # write_high_score()
        sys.exit()
def check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb):
    # 问题：这到底循环一次有几个event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # print(event.key) event.key是273 274 等等数字（int类型）
            check_keydown_events(event,ai_settings,screen,ship,bullets,stats, aliens,sb)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 返回点击时的鼠标x,y坐标
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,ship,ai_settings,screen,sb)

            # if event.key == pygame.K_RIGHT:
            #     ship.moving_right = False
            # elif event.key == pygame.K_LEFT:
            #     ship.moving_left = False
def update_screen(ai_settings,screen,ship,bullets,aliens,stats,play_button,sb):
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)  # 设置背景色
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()  # 在指定位置绘制飞船
    # 对编组调用draw，会根据编组内部元素的属性rect绘制每个元素
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def check_bullet_alien_collisions(ai_settings,aliens,bullets,screen,ship,stats,sb):
    """检测子弹与外星人的碰撞"""
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        # 每颗子弹都是collisions的一个键，键对应的值是一个列表，包含所以该子弹撞到的外星人
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            sb.pre_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # empty方法 是编组的自带方法，清空编组。
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,aliens,ship)
        stats.level += 1
        sb.pre_level()



def update_bullets(ai_settings,aliens,bullets,screen,ship,stats,sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中外星人
    # sprite.groupcollide被传入两个编组，它会一一比对，如果rect碰撞，则会返回一个字典/在字典中新增键值对。
    # 后面的两个True表示，检测到碰撞要不要删除
    check_bullet_alien_collisions(ai_settings,aliens,bullets,screen,ship,stats,sb)



def fire_bullet(bullets,ai_settings,screen,ship):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings,alien_width):
    # 计算一行容纳多少外星人
    available_space_x =  ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x


def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (2 *alien_height)-(alien_height+ship_height))
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    # 创建一个外星人并将其放在当前行
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def create_fleet(ai_settings,screen,aliens,ship):
    """创建外星人群"""
    # 先创建一个外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 刚开始这整反了。应该是行的循环在外层，每行画几个在内层
            # 整反也没事，横着画还是竖着画的问题
            create_alien(ai_settings,screen,aliens,alien_number,row_number)



def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    # 对编组遍历，要使用sprites（）
    for alien in aliens.sprites():
        alien.rect.y +=ai_settings.fleet_drop_speed # y轴是向下增加的
    ai_settings.fleet_direction*=-1 # 改变方向，去反方向

def update_aliens(ai_settings, aliens,ship,stats,screen,bullets,sb):

    """检查是否有外星人处于屏幕边缘，并调整"""
    check_fleet_edges(ai_settings,aliens)
    # 对编组调用某种方法，相当于对编组中的所有实例都调用一遍该方法
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        # sprite.spritecollideany的方法，先不深究
        ship_hit(ai_settings, aliens,ship,stats,screen,bullets,sb)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets,sb)

def ship_hit(ai_settings, aliens,ship,stats,screen,bullets,sb):
    if stats.ships_left > 0:
        # 被撞倒后飞船生命值-1
        stats.ships_left -=1
        # 清空外星人和子弹的编组
        aliens.empty()
        bullets.empty()
        sb.pre_ships()
        # 创建新外星人,复位飞船
        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        # 游戏进入非活动状态，光标可见
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb):
    """检查是否有外星人到达底部"""
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >=screen_rect.bottom:
            ship_hit(ai_settings, aliens,ship,stats,screen,bullets,sb)
            # break 就是碰底直接死
            break

def check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,ship,ai_settings,screen,sb):
    # 单击时开始游戏
    # collidepoint检查鼠标的x,y坐标点是否在按钮的rect内
    # 当且仅当鼠标点击按钮且游戏在非活动状态时，才能重置游戏
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        # 重置游戏
        start_game(stats,aliens,bullets,ship,ai_settings,screen,sb)
        # stats.game_active = True
        # # 游戏进入活动状态后，光标不可见
        # pygame.mouse.set_visible(False)
        # stats.reset_stats()
        # aliens.empty()
        # bullets.empty()
        # create_fleet(ai_settings,screen,aliens,ship)
        # ship.center_ship()

def start_game(stats,aliens,bullets,ship,ai_settings,screen,sb):
    """单击play按钮后，被调用。归零"""
    stats.game_active = True
    ai_settings.initialize_dynamic_settings()
    # 游戏进入活动状态后，光标不可见
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()
    sb.pre_level()
    sb.pre_score()
    sb.pre_ships()
    # sb.pre_high_score()


def check_high_score(stats,sb):
    """检查是否产生了最高分"""
    if stats.high_score < stats.score:
        stats.high_score = stats.score
        sb.pre_high_score()