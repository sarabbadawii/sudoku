# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import *
import string
from tkinter import messagebox

import numpy as np
from Sudoku_DE import Sudoku_DE
from S_BT import S_BT
boards = [
            [["5", "3", "", "", "7", "", "", "", ""],
             ["6", "", "", "1", "9", "5", "", "", ""],
             ["", "9", "8", "", "", "", "", "6", ""],
             ["8", "", "", "", "6", "", "", "", "3"],
             ["4", "", "", "8", "", "3", "", "", "1"],
             ["7", "", "", "", "2", "", "", "", "6"],
             ["", "6", "", "", "", "", "2", "8", ""],
             ["", "", "", "4", "1", "9", "", "", "5"],
             ["", "", "", "", "8", "", "", "7", "9"]]
            ,
            [["", "", "", "9", "", "3", "5", "2", ""],
             ["", "7", "3", "", "5", "2", "", "", ""],
             ["", "", "5", "", "", "", "1", "", "3"],
             ["", "", "", "4", "1", "8", "7", "5", "2"],
             ["", "", "", "", "", "", "", "8", ""],
             ["4", "8", "", "", "", "", "", "1", ""],
             ["", "1", "", "7", "", "5", "8", "", ""],
             ["", "", "8", "", "", "9", "", "", ""],
             ["", "", "4", "8", "6", "", "", "3", "5"]],
            [
                ["", "", "", "6", "", "", "3", "", ""],
                ["", "3", "4", "", "", "", "5", "7", ""],
                ["9", "", "1", "", "7", "", "", "2", ""],
                ["1", "5", "8", "", "4", "3", "7", "", "2"],
                ["", "2", "3", "1", "6", "7", "8", "", "9"],
                ["", "", "", "5", "", "", "1", "", "4"],
                ["3", "", "5", "2", "", "6", "", "", ""],
                ["", "", "", "", "3", "9", "2", "", ""],
                ["", "9", "", "", "", "", "", "1", ""]]

        ]
level=0
root=Tk()
root.geometry('850x500')

root.configure(bg="white smoke")
class GUI():
    count=0
    def __init__(self):
        self.board=[[]]
        self.level=level
        self.board= [["" for col in range(9)] for row in range(9)]
        self.play_board=[[[StringVar(root),"black"]for col in range(9)]for row in range(9)]
        for row in range(9):
            for col in range(9):
                self.play_board[row][col][0].set(boards[self.level][row][col])

        for i in range(9):
            for j in range(9):
                if((i<3 or i>5) and(j<3 or j >5)):
                    color="skyblue"
                elif((i>2 and i<6) and (j>2 and j<6)):
                    color="skyblue"
                else:
                    color="white"
                self.board[i][j]=Entry(root,width=3,font=("Arial",25),bg=color,
                                      fg=self.play_board[i][j][1],borderwidth=4
                                       ,highlightbackground="gray"
                                       ,justify="center",relief="raised",
                                       textvariable=self.play_board[i][j][0])
                self.board[i][j].grid(row=i,column=j,padx=(20,0) if j==0 else (0,0),pady=(10,0)if i==0 else (0,0))
        choose=Label(root,text="choose your method to solve:", fg="gray", relief='raised', borderwidth = 1, font = ('Arial', 11, 'bold'))
        choose.grid(column=11,row=2,padx=10, pady=5)
        backtracking=Button(root,text='Backtracking',command=self.backTracking,
                            activebackground="aliceblue", bg="skyblue")
        backtracking.grid(column=11,row=3,padx=10,pady=5)
        DEvolution=Button(root,text='Differential evolution',command=self.DEvolution,
                          activebackground="aliceblue", bg="skyblue")
        DEvolution.grid(column=11, row=4, padx=10, pady=5)

    def play(self,level):
        self.board = [[]]
        self.level = level
        self.board = [["" for col in range(9)] for row in range(9)]
        self.play_board = [[[StringVar(root), "black"] for col in range(9)] for row in range(9)]
        for row in range(9):
            for col in range(9):
                self.play_board[row][col][0].set(boards[self.level][row][col])

        for i in range(9):
            for j in range(9):
                if ((i < 3 or i > 5) and (j < 3 or j > 5)):
                    color = "skyblue"
                elif ((i > 2 and i < 6) and (j > 2 and j < 6)):
                    color = "skyblue"
                else:
                    color = "white"
                self.board[i][j] = Entry(root, width=3, font=("Arial", 25), bg=color,
                                         fg=self.play_board[i][j][1], borderwidth=4
                                         , highlightbackground="gray"
                                         , justify="center", relief="raised",
                                         textvariable=self.play_board[i][j][0])
                self.board[i][j].grid(row=i, column=j, padx=(20, 0) if j == 0 else (0, 0),
                                      pady=(10, 0) if i == 0 else (0, 0))
        choose = Label(root, text="choose your method to solve:", fg="gray",
                      relief='raised', borderwidth=1,
                       font=('Arial', 11, 'bold'))
        choose.grid(column=11, row=2,padx=10,pady=5)
        backtracking = Button(root, text='Backtracking', command=self.backTracking,
                              activebackground="aliceblue", bg="skyblue")
        backtracking.grid(column=11, row=3, padx=10, pady=5)
        DEvolution = Button(root, text='Differential evolution', command=self.DEvolution,
                            activebackground="aliceblue", bg="skyblue")
        DEvolution.grid(column=11, row=4, padx=10, pady=5)

    def replace(self,my_board):
        myList = [["" for col in range(9)] for row in range(9)]
        for row in range(9):
            for col in range(9):
                if my_board[row][col] == "":
                    myList[row][col] = 0
                else:

                    myList[row][col] = int(my_board[row][col])
        return myList

    def send_results(self,result):

        for i in range(9):
            for j in range(9):
                if(result[i][j]==0):
                   result[i][j]=""
                else:
                    result[i][j]=str(result[i][j])
        return result

    def backTracking(self):
        p=self.replace(boards[self.level])
        s = S_BT()
        if (not s.Solve_Sudoku(p)):
            messagebox.showwarning("warning","this board is not valid")

        else:
            b= self.send_results(p)
            boardProperties = list()
            self.boardProperties = b
            for i in range(9):
                for j in range(9):

                    if(b[i][j] != boards[self.level][i][j]):
                        self.play_board[i][j][1]="blue"

                        self.play_board[i][j][0].set(b[i][j])
                        if ((i < 3 or i > 5) and (j < 3 or j > 5)):
                            color = "skyblue"
                        elif ((i > 2 and i < 6) and (j > 2 and j < 6)):
                            color = "skyblue"
                        else:
                            color = "white"
                        self.board[i][j] = Entry(root, width=3, font=("Arial", 25), bg=color,
                                                 fg=self.play_board[i][j][1], borderwidth=4
                                                 , highlightbackground="gray"
                                                 , justify="center", relief="raised",
                                                 textvariable=self.play_board[i][j][0])
                        self.board[i][j].grid(row=i, column=j, padx=(20, 0) if j == 0 else (0, 0),
                                              pady=(10, 0) if i == 0 else (0, 0))
        self.next_level()

    def DEvolution(self):

        s = Sudoku_DE()
        res=s.solve_by_DE(boards[self.level])
        res=res.tolist()
        b= self.send_results(res)
        boardProperties = list()
        self.boardProperties = b
        for i in range(9):
            for j in range(9):

                if(b[i][j] != boards[self.level][i][j]):
                    self.play_board[i][j][1]="blue"

                    self.play_board[i][j][0].set(b[i][j])
                    if ((i < 3 or i > 5) and (j < 3 or j > 5)):
                        color = "skyblue"
                    elif ((i > 2 and i < 6) and (j > 2 and j < 6)):
                        color = "skyblue"
                    else:
                        color = "white"
                    self.board[i][j] = Entry(root, width=3, font=("Arial", 25), bg=color,
                                                 fg=self.play_board[i][j][1], borderwidth=4
                                                 , highlightbackground="gray"
                                                 , justify="center", relief="raised",
                                                 textvariable=self.play_board[i][j][0])
                    self.board[i][j].grid(row=i, column=j, padx=(20, 0) if j == 0 else (0, 0),
                                              pady=(10, 0) if i == 0 else (0, 0))
        self.next_level()

    def next_level(self):

        level=(self.level+1)%3
        if(level==0):
            messagebox.showinfo("congratulations", "congratulations ^_^, \n you finished the game..")
        else:
            messagebox.showinfo("congratulations", "congratulations ^_^, \n you have opened the next level..")
        self.play(level)







# Press the green button in the gutter to run the script.

if __name__ == '__main__':


    a=GUI()
    a.__init__()
    root.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
