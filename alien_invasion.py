import sys
    # sys模块是 Python 标准库内置模块，能提供和 Python 解释器及运行环境交互的诸多功能（如获取命令行参数、操作模块搜索路径、控制程序退出等）
# 能够在飞船被外星人撞到后让游戏暂停一会
from time import sleep

import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien



class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏的资源"""
        pygame.init()
            # pygame.init()：这行代码是初始化pygame库，它会对pygame内部使用的各种模块（例如显示模块、声音模块等）
            # 进行初始化设置，必须在使用其他pygame功能之前调用，确保相关的子系统都准备就绪。
        self.clock = pygame.time.Clock()
            # pygame.time.Clock() 这部分是创建了一个 Clock 类的实例对象。这个 Clock 对象在 pygame 中有很重要的作用，主要用于控制游戏的帧率
        # 导入设置
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
            # 通过pygame.display.set_mode方法创建了一个游戏显示窗口，参数(1200, 800)指定了窗口的宽度为 1200 像素，高度为 800 像素，
            # 并将返回的表示这个窗口的对象赋值给实例变量self.screen，后续可以通过这个变量来对窗口进行操作，比如在上面绘制游戏元素等。
        pygame.display.set_caption("Alien Invasion")
            # 这行代码用于设置游戏窗口的标题为"Alien Invasion"，让玩家可以直观地知道当前运行的游戏名称。

        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)


        # 创建Play按钮
        self.play_button = Button(self, "Play")


        self.ship = Ship(self)
            # Ship(self) 里的 self 指向的是 AlienInvasion 实例，这让 Ship 能够访问游戏资源
        self.bullets = pygame.sprite.Group()
            # pygame.sprite.Group() 这部分是创建了一个 Group 类的实例对象。这个 Group 对象在 pygame 中用于管理和操作一组相关的精灵对象，
            # 比如在游戏中管理所有的敌人、道具、子弹等元素，如添加、移除子弹，检测碰撞等。相当于一个列表。
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.game_active = False



    def run_game(self):
        """开始游戏的主循环"""
            # 游戏的主体运行逻辑基本都在这个循环内持续运转，保证游戏能实时响应各种情况并不断更新画面、处理交互等，直到满足退出条件为止。
        while True:
            self._check_events()            # 响应鼠标和键盘事件

            if self.game_active:
                self.ship.update()              # 更新飞船的位置
                self._update_bullets()          # 更新子弹的位置
                self._update_aliens()           # 更新外星人的位置

            self._upgrade_screen()          # 更新屏幕
            self.clock.tick(60)             # tick()方法接受一个参数：游戏帧率。这里指每秒更新60帧





    def _check_events(self):
        """响应鼠标和键盘事件"""
        for event in pygame.event.get():
            # 通过pygame.event.get()可以获取到在当前这一帧游戏中发生的所有事件（比如键盘按键按下、鼠标点击、鼠标移动、窗口关闭等事件）,
            # 其主要作用是获取自上一次调用该函数之后到当前时刻游戏中发生的所有事件信息，并将这些事件以列表的形式返回，
            # 然后使用for循环依次遍历这些事件，以便对每个事件进行针对性的处理。
            if event.type == pygame.QUIT:
                # 这里检查当前遍历到的事件类型是否为pygame.QUIT，pygame.QUIT事件通常对应着玩家点击游戏窗口的关闭按钮这个操作。
                sys.exit()
                # 当检测到pygame.QUIT事件时，调用sys.exit()来终止整个 Python 程序的运行，从而实现正常关闭游戏的目的。
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标位置：pygame.mouse.get_pos()返回一个包含当前鼠标坐标的元组 (x, y)
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_keydown_events(self,event):
        """响应按下"""
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self,event):
        """响应释放"""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _check_play_button(self,mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        # collidepoint()方法用于检查一个点是否在一个矩形区域内。
        # 它接受一个元组 (x, y) 作为参数，表示要检查的点的坐标。
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # not self.game_active 为 True 表示游戏当前处于非活动状态。
        if button_clicked and not self.game_active:
            # 还原游戏设置
            self.settings.initialize_dynamic_settings()
            # 重置游戏设置
            self.stats.reset_stats()
            self.game_active = True

            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            # 创建一群新的外星人，并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏光标
            pygame.mouse.set_visible(False)





    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        # if len(self.bullets) < self.settings.bullets_allowed:
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
            # 使用add()方法将新创建的子弹添加到编组bullets中,add()方法是pygame.sprite.Group类中的一个方法，用于将一个精灵对象添加到编组中。
            # 类似于列表的append()方法。不过是专门为Pygame的编组设计的，且只能添加一个精灵对象
        print(len(self.bullets))                # 打印子弹数量


    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        self.bullets.update()
            # 在对编组调用update()方法时，Pygame 会自动遍历编组中的所有元素，并调用每个元素的 update()方法，
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                # 在使用 for 循环遍历列表时，Python要求改列表的长度在整个循环中保持不变。因此不能从 for 循环遍历的列表或编组中删除元素，
                # 因此必须遍历编组的副本。使用copy()方法可以创建一个列表的副本，在副本中循环，删除原列表中的元素。

        # 检查是否有子弹击中了外星人,如果发生碰撞，就删除子弹和外星人
        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # pygame.sprite.groupcollide()函数将一个编组和一个编组进行比较，如果两个编组中有任何元素发生碰撞，就将它们都删除。
        # pygame.sprite.groupcollide()函数返回一个字典，字典的键是子弹，字典的值是外星人
        # True,True表示碰撞后删除子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            # 如果外星舰队被消灭，就删除现有的子弹，并创建一群新的外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            # self.sb.check_high_score()


    def _create_fleet(self):
        """创建外星舰队"""
        # 创建一个外星人，再不断添加，直到没有空间为止，外星人的间距为外星人宽度和外星人的高度
        alien = Alien(self)
        # 属性rect.size返回一个元组，其中包含了矩形的宽度和高度
        alien_width , alien_height = alien.rect.size


        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width

        # 添加一行外星人后，重置 x 值并递增 y 值。
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self,x_position,y_position):
        """创建一个外星人,并将其加入外星军队"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """将整个外星人舰队向下移动，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整个外星舰队的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        # spritecollideany()接受两个实参：一个精灵和一个编组。它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生碰撞的成员后停止遍历编组，并返回那个成员。
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            print("Ship hit!!!")
            self._ship_hit()

        # 检查是否有外星人到达屏幕底端
        self._check_aliens_bottom()



    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将ships_left减1
            self.stats.ships_left -= 1
            # 清空外星人列表和子弹列表
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人，并将飞船放到屏幕底端中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break







    def _upgrade_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 设置背景颜色
        self.screen.fill(self.settings.bg_color)
        # 将飞船绘制到屏幕上
        self.ship.blitme()
        # bullets.sprites()方法返回一个包含编组中所有精灵对象的列表.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 是 pygame.sprite.Group 类的一个方法，用于将精灵组中的所有精灵绘制到指定的 Surface 上
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，则绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()


        pygame.display.flip()
            # 更新整个屏幕显示，将之前在后台缓冲区（也叫离屏缓冲区，用于暂存要绘制的新画面内容）中绘制好的内容一次性全部显示到实际的屏幕上，
            # 让玩家能够看到最新的游戏画面，确保游戏画面能够流畅、持续地更新和展示。







if __name__ == '__main__':
    # 这部分代码是整个游戏程序的入口点。通过if __name__ == '__main__':这个条件判断，可以确保代码在直接作为主程序运行时才会执行后续的操作，
    # 而在被其他模块导入时不会自动执行。

    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
        # 触发类的构造函数__init__执行，完成游戏资源的初始化工作
    ai.run_game()
        # 启动游戏的主循环