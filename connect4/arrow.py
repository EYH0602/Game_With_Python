"""2"""
# http://www.hyf0602.com/pyGames/gameCodes.html
import pygame

class Arrow():
    """图标，指向玩家将要放球的列"""

    def __init__(self, screen):
        """初始化图标，放置在初始位置"""

        # 加载箭头图像，获取其外接矩形
        self.black = 'images/arrow_black.bmp'   # 设置玩家1的箭头
        self.white = 'images/arrow_white.bmp'   # 设置玩家2的箭头
        self.image = pygame.image.load(self.black)   # 预设为黑色
        self.rect = self.image.get_rect()

        # 将箭头初始位置设置为屏幕顶部中央
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top

        # # 在箭头的属性center中储存浮点数值
        # self.center = float(self.rect.centerx)

        # # 移动标志
        # self.move_right = False
        # self.move_left = False

    def set_color(self, user):
        if user != 1:
            self.image = pygame.image.load(self.black)
        else:
            self.image = pygame.image.load(self.white)

    def build(self):
        """绘制箭头"""
        self.screen.blit(self.image, self.rect)

    def move(self, direction, move_pace=1):
        """移动箭头"""
        if direction == 'Right':
            if self.rect.right < self.screen.get_rect().right:
                self.rect.centerx += move_pace*100

        elif direction == 'Left':
            if self.rect.left > 0:
                self.rect.centerx -= move_pace*100

    def getCol(self):
        return self.rect.centerx//100

