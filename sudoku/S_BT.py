import numpy as np
class S_BT:
    def Empty_place(self,board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    r = i
                    c = j
                    return r,c
        return None,None


    def valid_number(self,board,guess,r,c):
        for i in range(9):
            if guess == board[r][i]:
                return False

        for i in range(9):
            if guess == board[i][c]:
                return False

        row_start = r - r%3
        column_start = c - c%3
        for i in range(row_start,row_start+3):
            for j in range(column_start,column_start+3):
                if guess == board[i][j]:
                    return False

        return True

    def Solve_Sudoku(self,bo):
        board=bo
        row,column = self.Empty_place(board)

        if row == None:
           return True


        for guess in range(1,10):
            if(self.valid_number(board,guess,row,column)):
                board[row][column] = guess

                if(self.Solve_Sudoku(board)):
                    return True

                board[row][column] = 0

        return False