"""3"""
import sys
import pygame

def checkRow(board, row):
    """根据落子的行判断四连"""
    count = 1
    for j in range(1, len(board[row])):
        if board[row][j] == board[row][j-1] and board[row][j] != 0:
            count += 1
        else:
            count = 1
        # 找到4个了
        if count == 4:
            return board[row][j]
    # 没找到4连
    return 'NONE'

def checkCol(board, col):
    """根据落子的列判断四连"""
    count = 1
    for i in range(1, len(board)):
        if board[i][col] == board[i-1][col] and board[i][col] != 0:
            count += 1
        else:
            count = 1
        # 找到了4个
        if count == 4:
            return board[i][col]
    # 没找到4连
    return 'NONE'

def reachEndMajor(row, col, idT):
    """检查主对角线，何时结束"""
    if idT == 'upper':
        return col > 6
    return row > 6

def checkMajor(board, row, col):
    """根据落子的行列检查主对角线"""
    # 根据行列坐标判断初始位置
    # id用来判断对角线在上三角还是下三角
    if col > row:
        i = 0
        j = col-row  
        idT = 'upper'  # 所在主对角线在下三角
    else:
        i = row-col
        j = 0
        idT = 'lower'  # 所在主对角线在上三角

    # 开始检查落子点所在的主对角线
    count  = 1
    i += 1
    j += 1
    while not reachEndMajor(i,j,idT):
        if board[i][j] == board[i-1][j-1] and board[i][j] != 0:
            count += 1
        else:
            count = 1
        # 找到了4个
        print(count)
        if count == 4:
            return board[i][j]
        i += 1
        j += 1
    return 'NONE'

def reachEndMinor(row, col, idT):
    """检查辅对角线，何时结束"""
    if idT == 'upper':
        return col < 0
    return row > 6

def checkMinor(board, row, col):
    """根据落子的行列判断辅对角线"""
    if row+col <= 6:
        i = 0
        j = row+col
        idT = 'upper'
    else:
        i = row-1
        j = 6
        idT = 'lower'
    # 开始检查落子点所在的辅对角线
    count = 1
    i += 1
    j -= 1
    while not reachEndMinor(i,j,idT):
        if board[i][j] == board[i-1][j+1] and board[i][j] != 0:
            count += 1
        else:
            count = 1
        # 找到了4个
        if count == 4:
            return board[i][j]
        i += 1
        j -= 1
    # 没找到
    return 'NONE'

def getStatu(board, row, col):
    """判断是否产生赢家"""
    winner = checkRow(board, row)
    if winner == 'NONE':
        winner = checkCol(board, col)
    if winner == 'NONE':
        winner = checkMajor(board, row, col)
    if winner == 'NONE':
        winner = checkMinor(board, row, col)
    return winner

def drop(board, x, user):
    """落下一子"""
    i = 0
    if board[0][x] == 0:
        while i < len(board) and board[i][x] == 0:
            i += 1
        board[i-1][x] = user
    return getStatu(board, i-1, x)
    
def draw(board, screen):
    """根据游戏板子画出球球们"""
    black = (0,0,0)
    white = (255,255,255)

    # 画格子：窗口，颜色，起始位置，结束位置，粗细
    rect = screen.get_rect()
    for i in range(1, 8):  
        pygame.draw.line(screen, black, [0, 100 * i], [rect.right, 100 * i], 1)
        pygame.draw.line(screen, black, [100 * i, 100], [100 * i, rect.bottom], 1)
    
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            # 根据这里的玩家标记画圆
            if board[i][j] != 0:
                x = j*100 + 50  # 圆心x坐标预置为50
                y = i*100 + 150 # 圆心y坐标预置为150， 0-100为箭头
                if board[i][j] == 1:
                    color = black
                else:
                    color = white
                # 根据颜色和坐标画出半径为50的园
                pygame.draw.circle(screen, color, (x,y), 50)

def pout(board):
    """打印出整个游戏板"""
    for row in board:
        print(row)

def isFull(board):
    """判断棋板是否满了"""
    # 由于游戏规则，只需要判断游戏板的第一行就好
    for cell in board[0]:
        if cell == 0:
            return False
    return True