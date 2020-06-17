"""1"""
import pygame
import sys
import random
import time
import functions as func


# total # of mine = func.size*level
def getBoard(level):
    """get the game board"""
    board = []
    for i in range(func.size):
        line = []
        for j in range(func.size):
            line.append('E')
        board.append(line)
    
    # 埋炸弹
    if func.setting["number of mine"] == "default":
        numMine = func.size*level
    else:
        numMine = func.setting["number of mine"]
    i = 0
    while i < numMine:
        x = random.randint(0,func.size-1)
        y = random.randint(0,func.size-1)
        if board[x][y] != 'M':
            board[x][y] = 'M'
            i += 1

    return board

def getRealPos(screenPos):
    """根据屏幕坐标，返回board上的真实坐标"""
    i = screenPos[1]//50
    j = screenPos[0]//50
    return (i, j)

def checkEvents(board, screen):
    status = 'NULL'
    LEFT = 1    # example with photo of mouse
    RIGHT = 3

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            sys.exit()
        # 获取鼠标点击的坐标
        elif event.type is pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()    # this returns a tuple
            realPos = getRealPos(pos)
            print(realPos)
            if event.button == LEFT:   # if get left click, dfs
                func.updateBoard(board, realPos)
            elif event.button == RIGHT:       # if get right click, set flag
                if len(board[realPos[0]][realPos[1]]) == 1 and\
                        (board[realPos[0]][realPos[1]] == 'M' or\
                        board[realPos[0]][realPos[1]] == 'E'):
                    board[realPos[0]][realPos[1]] += 'F'    # add flag
                else:
                    board[realPos[0]][realPos[1]]\
                        = board[realPos[0]][realPos[1]][0:1]    # deflag


def updateScreen(background, screen, board):
    """更新屏幕上的新图像"""
    # 每个循环重新绘制弹出屏幕
    screen.fill(background)
    func.draw(board, screen)
    pygame.display.flip()

def checkEvent(screen):
    """监视键盘和鼠标事件,只给结束界面用"""
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            sys.exit()

def displayEndBoard(background, screen, statement):
    player = func.setting["player"]
    textFont = func.setting["font"]["text_font"]
    textColor = func.hex_to_rgb(func.setting["color"]["text"])

    # alerting text
    fontTitle = pygame.font.SysFont(textFont, 90)   # (字体，大小)
    title = 'Game End'
    text_title = fontTitle.render(title, True, textColor)
    titleRect = text_title.get_rect()
    titleRect.center = (225, 175)

    # status text
    fontSentence = pygame.font.SysFont(textFont, 40)   # (字体，大小)
    sentence = player + ", you " + statement
    text_sentence = fontSentence.render(sentence, True, textColor)
    sentenceRect = text_sentence.get_rect()
    sentenceRect.center = (225, 300)

    # display them
    while True:
        screen.fill(background)
        screen.blit(text_title, titleRect)
        screen.blit(text_sentence, sentenceRect)
        pygame.display.flip()
        checkEvent(screen)

def run():
    """运行游戏"""
    # load setting first
    background = func.hex_to_rgb(func.setting["color"]["background"])
    level = func.setting["level"]
    screenSize = (func.size*50, func.size*50)
    
    # 创建屏幕对象
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Minesweeper")

    board = getBoard(level)
    print("Initial Board")
    func.printBoard(board)

    while True:
        checkEvents(board, screen)
        updateScreen(background, screen, board)
        status = func.isEnd(board, func.size*level)
        if status[0]:
            time.sleep(1)
            print("End Board")
            func.printBoard(board)
            displayEndBoard(background, screen, status[1])


run()
