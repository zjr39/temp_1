# pygame.font模块能让字符串渲染为图像到屏幕上
import pygame.font

class Button():
    def __init__(self,game,msg):
        """初始化按钮的属性"""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width,self.height = 200,50
        self.button_color = (0,135,0)
        self.text_color = (255,255,255)
        # 实惨None表示使用默认字体，48表示字体大小
        self.font = pygame.font.SysFont(None,48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需要创建一次
        self._prep_msg(msg)



    def _prep_msg(self,msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        # font.render()将存储在msg中的文本转换为图像
        # 实参True表示开启反锯齿功能，让文本的边缘更平滑
        # 余下的两个实参分别是文本颜色和背景色(如果没有指定背景色，Pygame将使用透明的背景)
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        # screen.fill()用来绘制表示按钮的矩形
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)