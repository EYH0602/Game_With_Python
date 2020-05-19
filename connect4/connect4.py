"""1"""
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame install pygame on windows
import sys
import pygame
import time
import functions as func
from arrow import Arrow

def keydown(screen, event, arrow, board, count, statu):
    """按下响应"""
    key = event.key
    # d或右方向键 -> 向右移动箭头
    if key is pygame.K_d or key is pygame.K_RIGHT:
        arrow.move('Right')

    # a或左方向键 -> 向左移动箭头
    elif key is pygame.K_a or key is pygame.K_LEFT:
        arrow.move('Left')
    
    # s或下方向键 -> 释放球球
    elif key is pygame.K_s or key is pygame.K_DOWN:
        print(count)
        if count[0]%2 == 0:
            user = 1
        else:
            user = 2
        arrow.set_color(user)   # 为下一回玩家设置箭头颜色
        statu[0] = func.drop(board, arrow.getCol(), user)
        # 如果这列到头了，就不能再往上加球，count也就不加了
        if board[0][arrow.getCol()] == 0:
            count[0] += 1

def checkEvents(screen, arrow, board, count, statu):
    """监视键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            sys.exit()
        elif event.type is pygame.KEYDOWN:
            keydown(screen, event, arrow, board, count, statu)

def updateScreen(background_color, screen, arrow, board):
    """更新屏幕上的新图像"""
    # 每个循环重新绘制弹出屏幕
    screen.fill(background_color)
    arrow.build()
    func.draw(board, screen)
    # 弹出新绘制的屏幕
    pygame.display.flip()

def checkEvent(screen):
    """监视键盘和鼠标事件,只给结束界面用"""
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            sys.exit()

def displayWinner(background_color, screen, winner):
    font = pygame.font.Font(None, 100)   # (字体，大小)
    sentence = 'Player ' + str(winner) + ' wins!!!'
    text = font.render(sentence, True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (350, 400)
    while True:
        screen.fill(background_color)
        screen.blit(text, textRect)
        pygame.display.flip()
        checkEvent(screen)

def run():
    """运行游戏"""
    screen_width = 700                 # 弹出屏幕的宽度
    screen_height = 800                # 弹出屏幕的高度
    screen_size = (screen_width, screen_height)
    background_color = (255, 87, 51)   # 弹出屏幕颜色，橙色
    # https://htmlcolorcodes.com/color-chart/ 可以找到颜色10进制代码

    # 创建一个屏幕对象
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Connect 4")
    board = [[0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0]]
    arrow = Arrow(screen)       # 创建箭头对象
    count = [0]   # 数放球球的次数, 为了传引用所以是列表
    statu = ['NONE']    # 记录当前状态

    # 开始游戏
    while True:
        # 根据当前循环次数判断玩家
        checkEvents(screen, arrow, board, count, statu)
        updateScreen(background_color, screen, arrow, board)
        
        # 查询游戏进度，是否产生赢家
        if statu[0] != 'NONE':
            if statu[0] == "no winner":
                print("Game END!! no winner")
            else:
                time.sleep(1)
                print("player " + str(statu[0]) + " wins!!!")
            func.pout(board)
            displayWinner(background_color, screen, statu[0])
            break
        
run()
