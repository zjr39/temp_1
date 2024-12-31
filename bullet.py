import pygame
from pygame.sprite import Sprite
    # Sprite 类是 Pygame 中用于表示游戏中精灵（如角色、敌人、道具等）的基础类，通常用于创建可以移动和绘制的游戏对象


"""管理子弹的类,相当于Sprite的一个子类"""
class Bullet(Sprite):
    def __init__(self,game):
        """在飞船所处的位置创建一个子弹对象"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color





        """创建子弹的矩形"""
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
            # 子弹并非基于图像文件的，因此使用 pygame.Rect()类 从头开始创建一个矩形对象。
            # 在创建这个类的实例时，必须提供四个参数：矩形左上角的 x 坐标和 y 坐标、矩形的宽度和高度·
        self.rect.midtop = game.ship.rect.midtop
            # 我们在(0,0)处创建一个矩形，子弹的初始位置设置为飞船的顶部中央

        self.y = float(self.rect.y)
            # 子弹的 y 坐标存储为一个浮点数，以便能够微调子弹的速度




    """向上移动子弹"""
    def update(self):
        self.y -= self.settings.bullet_speed        # 更新子弹的准确位置
        self.rect.y = self.y                        # 更新表示子弹位置的 rect 的位置
        # """子弹消失后，删除子弹"""
        # if self.rect.bottom <= 0:
        #     self.kill()
        #     """kill() 方法用于删除当前对象，即删除子弹"""

    """在屏幕上绘制子弹"""
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
            # draw.rect() 方法用于在屏幕上绘制矩形，需要传入三个参数：屏幕对象（表示绘制的表面）、颜色、矩形对象
