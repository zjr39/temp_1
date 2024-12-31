import pygame.image


class Ship:
    def __init__(self,game):
        # Ship 的 __init__ 方法接受两个参数：除了 self 引用，还有一个指向当前 AlienInvasion 实例的引用，这让 Ship 能够访问 AlienInvasion 中定义的所有游戏资源
        """初始化飞船并设置其初始位置"""
        self.screen = game.screen
            # 这行代码从传入的 game 对象中获取了代表游戏屏幕的 Surface 对象，并赋值给 self.screen。这样，在 Ship 类的实例中就能方便地访问和操作游戏屏幕了
        self.screen_rect = game.screen.get_rect()
            # 通过调用 game.screen（同样是那个游戏屏幕 Surface 对象）的 get_rect() 方法，获取了屏幕对应的矩形对象（Rect），
            # 这个矩形对象定义了屏幕的位置和大小信息。它在后续确定飞船位置等操作中会起到重要作用，比如用于将飞船放置在屏幕的特定位置上。

        """加载飞船图像并获取其外接矩形"""
        self.image = pygame.image.load('images/ship.bmp')
            # 使用 pygame.image 模块的 load 方法从指定的文件路径（'images/ship.bmp'）加载飞船的图像文件，将其转换为一个 Surface 对象并赋值给 self.image
        self.rect = self.image.get_rect()
            # 获取该图像对应的矩形对象

        """每艘新飞船都放在屏幕底部中央"""
        self.rect.midbottom = self.screen_rect.midbottom
            # 通过将飞船图像的矩形对象（self.rect）的 midbottom（底部中央位置）属性设置为与屏幕矩形对象（self.screen_rect）的 midbottom 属性相同，巧妙地将飞船放置在了屏幕的底部中央位置

        self.settings = game.settings

        """将位置赋给一个能存储浮点数的变量"""
        self.x = float(self.rect.x)
            # rect只会保留整数部分。所有使用 float() 函数将 self.rect.x 的值转换为浮点数并赋值。

        """移动标志"""
        self.moving_right = False
        self.moving_left = False



    """根据移动标志调整飞船的位置"""
    def update(self):
        # 更新飞船的属性 x 的值，而不是其外接矩形的属性 x 的值
        if self.moving_right and self.rect.right < self.screen_rect.right:      # .right 返回外接矩形的右边缘的 x 坐标
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:                       # 此处不能用elif
            self.x -= self.settings.ship_speed


        """根据 self.x 更新 rect 对象"""
        self.rect.x = self.x



    """在指定位置绘制飞船"""
    def blitme(self):
        self.screen.blit(self.image,self.rect)
            # blit 是 pygame 中用于将一个 Surface 对象（这里就是 self.image，即飞船的图像）绘制到另一个 Surface 对象（游戏屏幕）上的方法，
            # 它需要传入两个参数，一个是要绘制的图像 Surface 对象，另一个是该图像对应的矩形对象（self.rect），矩形对象用于确定图像在目标表面（游戏屏幕）上的绘制位置
            # 通过调用这个方法，飞船图像就会按照之前设定好的位置（在 __init__ 方法中确定的屏幕底部中央）出现在游戏屏幕上了。

    def center_ship(self):
        """将飞船放在屏幕底部中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)