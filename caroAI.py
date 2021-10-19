from random import randint
import threading

class caro:
    #false = player, tru = AI
    turn = False
    def __init__(self, xsize, ysize, winning, Search):
        #initiallize game properties and game board
        self.xsize = xsize
        self.ysize = ysize
        #consecutive move on the board to win
        self.winning = winning
        self.gameBoard =  [[' ' for i in range(ysize)] for j in range(xsize)]

        #num of evaluated layers
        self.layers = 0
        self.Search = Search

        #zobrist hasing table
        self.Zobrist = [[[0 for k in range(3)] for j in range(ysize)] for x in range(xsize)]
        for i in range(xsize):
            for j in range(ysize):
                for k in range(3):
                    self.Zobrist[i][j][k] = randint(0, 1000000000)

        self.ZobristDict = {}

        self.Zob = 0
        for i in range(xsize):
            for j in range(ysize):
                self.Zob ^= self.Zobrist[i][j][self.index('')] 

    def checkCondition(self):
        #horizontal
        for i in range(self.xsize):
            for j in range(self.ysize - self.winning + 1):
                z = True
                for k in range(1, self.winning):
                    if (self.gameBoard[i][j + k] != self.gameBoard[i][j + k - 1] or self.gameBoard[i][j + k] == ' '):
                        z = False
                if z and self.gameBoard[i][j] != ' ':
                    return self.gameBoard[i][j]
            
        #vertical
        for j in range(self.ysize):
            for i in range(self.xsize - self.winning + 1):
                z = True
                for k in range(1, self.winning):
                    if (self.gameBoard[i + k][j] != self.gameBoard[i + k - 1][j] or self.gameBoard[i + k][j] == ' '):
                        z = False
                if z and self.gameBoard[i][j] != ' ':
                    return self.gameBoard[i][j]

        #diagonal - main
        for i in range(self.xsize - self.winning + 1):
            for j in range(self.ysize - self.winning + 1):
                z = True
                for k in range(1, self.winning):
                    if (self.gameBoard[i + k][j + k] != self.gameBoard[i + k - 1][j + k - 1] or self.gameBoard[i + k][j + k] == ' '):
                        z = False
                if z and self.gameBoard[i][j] != ' ':
                    return self.gameBoard[i][j]
        
        #diagonal - secondary diagonal
        for i in range(self.winning - 1, self.xsize):
            for j in range(self.ysize - self.winning + 1):
                z = True
                for k in range(1, self.winning):
                    if (self.gameBoard[i - k][j + k] != self.gameBoard[i - k + 1][j + k - 1] or self.gameBoard[i - k][j + k] == ' '):
                        z = False
                if z and self.gameBoard[i][j] != ' ':
                    return self.gameBoard[i][j]

        #draw
        z = True
        for i in range(self.xsize):
            for j in range(self.ysize):
                if self.gameBoard[i][j] == ' ':
                    z = False
        if z:
            #draw
            return ' '
        else:
            #board not full
            return ''
    
    def drawboard(self):
        for i in range(self.xsize):
            print('|', end = '')
            for j in range(self.ysize):
                print(self.gameBoard[i][j] + '|', end = '')
            print('')

    def run(self, px, py):
        #player
        self.gameBoard[px][py] = 'O'
        self.Zob ^= self.Zobrist[px][py][self.index('O')]
        #minimax - ai is max
        (x, y, kq) = self.maz(-100000000, 100000000, 1, 1)
        self.gameBoard[x][y] = 'X'

        self.Zob ^= self.Zobrist[x][y][self.index('X')]

        result = self.checkCondition()
        return(x, y, result)
    
    def index(self, move):
        if move == 'O':
            return 1
        elif move == 'X':
            return 2
        else:
            return 0

    def maz(self, alpha, beta, x0, y0):
        #min for maxkq
        maxkq = -100000000

        #zobrist
        if self.Zob in self.ZobristDict:
            (zx, zy, score) = self.ZobristDict[self.Zob]
            return(zx, zy, score)
        result = self.checkCondition()
        if result == 'X':
            return (x0, y0, 10000)
        elif result == 'O':
            return (x0, y0, -10000)
        if self.layers == self.Search or result != '':
            return (x0, y0, self.Evaluation_Function(x0, y0))
        x = None
        y = None
        for i in range(self.xsize):
            for j in range(self.ysize):
                if  self.gameBoard[i][j] == ' ':
                    self.gameBoard[i][j] = 'X'
                    #zobrist
                    self.Zob ^= self.Zobrist[i][j][self.index('X')]
                    self.layers += 1

                    (minx, miny, score) = self.minz(alpha, beta, i, j)

                    #zobrist
                    self.Zob ^= self.Zobrist[i][j][self.index('')]

                    if score >= beta:
                        self.gameBoard[i][j] = ' '
                        self.layers -= 1
                        self.ZobristDict.update({self.Zob: (i, j, score)})
                        return (i, j, score)

                    if score > alpha:
                        x = i
                        y = j
                        alpha = score

                    self.gameBoard[i][j] = ' '
                    self.layers -= 1
        self.ZobristDict.update({self.Zob: (x, y, alpha)})
        return (x, y, alpha)

    def minz(self, alpha, beta, x0, y0):
        #max for minkq
        minkq = 100000000

        #zobrist
        if self.Zob in self.ZobristDict:
            (zx, zy, score) = self.ZobristDict[self.Zob]
            return(zx, zy, score)

        result = self.checkCondition()
        if result == 'X':
            return (x0, y0, 10000)
        elif result == 'O':
            return (x0, y0, -10000)
        if self.layers == self.Search or result != '':
            return (x0, y0, -self.Evaluation_Function(x0, y0))
        x = None
        y = None
        for i in range(self.xsize):
            for j in range(self.ysize):
                if  self.gameBoard[i][j] == ' ':
                    self.gameBoard[i][j] = 'O'
                    self.Zob ^= self.Zobrist[i][j][self.index('O')]
                    self.layers += 1

                    (maxx, maxy, score) = self.maz(alpha, beta, i, j)

                    self.Zob ^= self.Zobrist[i][j][self.index('')]

                    if score <= alpha:
                        self.gameBoard[i][j] = ' '
                        self.layers -= 1
                        self.ZobristDict.update({self.Zob: (i, j, score)})
                        return (i, j, score)

                    if score < beta:
                        x = i
                        y = j
                        beta = score

                    self.gameBoard[i][j] = ' '
                    self.layers -= 1
        self.ZobristDict.update({self.Zob: (x, y, beta)})
        return (x, y, beta)

    def get_vertical_score(self, x, y):
        moves = 1
        blocked = 0
        for i in range(x + 1, self.xsize - 1):
            if self.gameBoard[i][y] == self.gameBoard[x][y]:
                moves += 1
            elif self.gameBoard[i][y] == ' ':
                break
            elif i == self.xsize - 1:
                blocked += 1
                break
            else:
                blocked += 1
                break

        for i in range(x - 1, 0, -1):
            if self.gameBoard[i][y] == self.gameBoard[x][y]:
                moves += 1
            elif self.gameBoard[i][y] == ' ':
                break
            elif i == 0:
                blocked += 1
                break
            else:
                blocked += 1
                break
        return (moves, blocked)

    def get_horizontal_score(self, x, y):
        moves = 1
        blocked = 0
        for j in range(y + 1, self.ysize - 1):
            if self.gameBoard[x][j] == self.gameBoard[x][y]:
                moves += 1
            elif self.gameBoard[x][j] == ' ':
                break
            elif j == self.ysize - 1:
                blocked += 1
                break
            else:
                blocked += 1
                break

        for j in range(y - 1, 0, -1):
            if self.gameBoard[x][j] == self.gameBoard[x][y]:
                moves += 1
            elif self.gameBoard[x][j] == ' ':
                break
            elif j == 0:
                blocked += 1
                break
            else:
                blocked += 1
                break
        return (moves, blocked)

    def get_diagonal_score_1(self, x, y):
        moves = 1
        blocked = 0
        for k in range(1, min(self.xsize - x - 1, self.ysize - y - 1)):
            if self.gameBoard[x + k][y + k] == self.gameBoard[x][y]:
                moves += 1
            elif self.gameBoard[x + k][y + k] == ' ':
                break
            elif k == min(self.xsize - x - 1, self.ysize - y - 1):
                blocked += 1
                break
            else:
                blocked += 1
                break

        for k in range(1, min(x, y)):
            if self.gameBoard[x - k][y - k] == self.gameBoard[x][y]:
                moves += 1
            elif self.gameBoard[x - k][y - k] == ' ':
                break
            elif k == min(x, y):
                blocked += 1
                break
            else:
                blocked += 1
                break
        return (moves, blocked)

    def get_diagonal_score_2(self, x, y):
        moves = 1
        blocked = 0
        for k in range(1, min(self.xsize - x - 1, y)):
            if self.gameBoard[x + k][y - k] == self.gameBoard[x][y]:
                moves += 1
            elif self.gameBoard[x + k][y - k] == ' ':
                break
            elif k == min(self.xsize - x - 1, y):
                blocked += 1
                break
            else:
                blocked += 1
                break

        for k in range(1, min(x, self.ysize - y - 1)):
            if self.gameBoard[x - k][y + k] == self.gameBoard[x][y]:
                moves += 1
            elif self.gameBoard[x - k][y + k] == ' ':
                break
            elif k == min(x, self.ysize - y - 1):
                blocked += 1
                break
            else:
                blocked += 1
                break
        return (moves, blocked)

    def evaluate(self, moves, blocked):
        if blocked == 0:
            switcher = {
                1: 1,
                2: 5,
                3: 15, 
                4: 81,
                5: 6561
            }
            return switcher.get(moves, 0)
        
        if blocked == 1:
            switcher = {
                2: 1,
                3: 4,
                4: 27,
                5: 6561
            }
            return switcher.get(moves, 0)
        return 0
        
        

    def Evaluation_Function(self, x, y):
        sum = 0
        (move, blocked) = self.get_vertical_score(x, y)
        sum += self.evaluate(move, blocked)
        (move, blocked) = self.get_horizontal_score(x, y)
        sum += self.evaluate(move, blocked)
        (move, blocked) = self.get_diagonal_score_1(x, y)
        sum += self.evaluate(move, blocked)
        (move, blocked) = self.get_diagonal_score_2(x, y)
        sum += self.evaluate(move, blocked)
        return sum
    
    


if __name__ == "__main__":
    mode = 1
    global gameBoard, xsize, ysize, winning
    #creating game board

    while True:
        print("Enter the board size, in x and y dimensions")
        z = False
        while not z:
            try:
                xsize = int(input())
                ysize = int(input())
                z = not z
            except:
                print('something was entered incorrectly. try again')
        print("Enter the number of consecutive moves needed to win the game")
        winning = int(input())
        while winning > max(xsize, ysize):
            print("The winning conditions needs to be lower than the max of tbe two board dimentions. Please try again.")
            winning = int(input())

        gameCaro = caro(xsize, ysize, winning, 1)



