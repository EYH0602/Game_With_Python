import pygame
import json
import re   # regular expression

def hex_to_rgb(hex):
    # credit: https://gist.github.com/matthewkremer/3295567
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

# load setting
settingFile = open("settings.json")
setting = json.load(settingFile)
boomColor = hex_to_rgb(setting["color"]["boom"])
blankColor = hex_to_rgb(setting["color"]["revealed_blank"])
flagColor = hex_to_rgb(setting["color"]["flag"])
numFont = setting["font"]["number_font"]
size = setting["size"]

def printBoard(board):
    for line in board:
        print(line)

def dfs(board, x, y):
    if not re.search("^.E*$", board[x][y]):
        return
    dx = [0,0,1,1,1,-1,-1,-1]   # move in x direction
    dy = [1,-1,0,1,-1,0,-1,1]   # move in y direction
    count = 0;
    
    # find out how many is around this cell
    for i in range(0,8):
        newx = x+dx[i]
        newy = y+dy[i]
        if newx < 0 or newy < 0 or\
             newx >= len(board) or newy >= len(board[0]):
            continue
        if board[newx][newy] == 'M' or board[newx][newy] == 'MF':
            count += 1
    # change this cell to the # of bombs around it
    if count > 0:
        board[x][y] = str(count)
        return
    
    # draw out the region
    board[x][y] = 'B'
    for i in range(0,8):
        newx = x+dx[i]
        newy = y+dy[i]
        if newx < 0 or newy < 0\
            or newx >= len(board) or newy >= len(board[0]):
            continue
        if board[newx][newy] == 'E':
            dfs(board,newx,newy)

def updateBoard(board, pos):
    i = pos[0]
    j = pos[1]
    if board[i][j] == 'M':
        board[i][j] = 'X'
        return 'Boom!!!'
    dfs(board,i,j)
    return 'Going Well'

def isEnd(board, totalM):
    """check to end the game"""
    countM = 0
    countF = 0
    for line in board:
        for cell in line:
            if cell == 'X':
                return (True, "loss...")
            elif cell == 'M':
                countM += 1
            elif cell == 'MF':
                countF += 1
    if countM == 0 and countF == totalM:
        return (True, "win!!!")
    return (False, "None")

def draw(board, screen):
    """根据游戏板子画出屏幕"""
    black = (0,0,0)
    white = (255,255,255)
    
    # 画格子：窗口，颜色，起始位置，结束位置，粗细
    rect = screen.get_rect()
    for i in range(0, size):  
        pygame.draw.line(screen, black, [0, 50 * i], [rect.right, 50 * i], 1)
        pygame.draw.line(screen, black, [50 * i, 0], [50 * i, rect.bottom], 1)

    for i in range(0, len(board)):
        for j in range(0,len(board[0])):
            pos = (j*50+25, i*50+25)
            textPos = (j*50+15, i*50)
            if board[i][j] == 'X':      # Boom!!
                pygame.draw.circle(screen, boomColor, pos, 25)   
            elif board[i][j] == 'B':    # revealed blank
                pygame.draw.circle(screen, blankColor, pos, 25)
            elif re.search("^.*F$", board[i][j]):    # Flag
                pygame.draw.circle(screen, flagColor, pos, 25)
            elif board[i][j].isdigit(): # 数字
                font = pygame.font.SysFont(numFont, 30)
                textsurface = font.render(board[i][j], False, black)
                # set the center of the rectangular object. 
                screen.blit(textsurface, textPos)
