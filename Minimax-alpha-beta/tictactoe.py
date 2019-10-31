import tkinter as tk
import tkinter.messagebox as messagebox
from copy import deepcopy
import random
from time import sleep


class TicTacToe:
    X = 'X'
    O = 'O'
    initial_board = [3*[None] for _ in range(3)]


    def __init__(self, starting_symbol=None, auto=True):
        if not starting_symbol:
            starting_symbol = TicTacToe.X
        self.starting_symbol = starting_symbol
        self.board = deepcopy(TicTacToe.initial_board)
        self.curr_symbol = starting_symbol
        self.auto = auto
        if auto:
            self.bot_symbol = random.choice([TicTacToe.X,TicTacToe.O])
            # print('bot_symbol', self.bot_symbol)


    def reset(self):
        self.board = deepcopy(TicTacToe.initial_board)
        self.curr_symbol = self.starting_symbol
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]['text'] = " "

        if self.bot_symbol == self.starting_symbol:
            if self.auto:
                self.bot()

    def move(self, row, column):
        if self.board[row][column]:
            return False
        else:
            self.board[row][column] = self.curr_symbol
            self.buttons[row][column]['text'] = self.curr_symbol
            if self.is_won():
                messagebox.showinfo("Game Over", self.curr_symbol + " won!")
                self.reset()
                return True
            if self.is_over():
                messagebox.showinfo("Game Over", "Equality.")
                self.reset()
                return True
            self.curr_symbol = self.other_turn(self.curr_symbol)
            if self.auto:
                if self.curr_symbol == self.bot_symbol:
                    self.bot()
            return True


    def is_won(self, board=None):
        if not board:
            board = self.board
        for r in range(3):
            if (board[r][0]==board[r][1]==board[r][2] and board[r][0]) or\
                (board[0][r]==board[1][r]==board[2][r] and board[0][r]):
                return True
        if (board[0][0]==board[1][1]==board[2][2] and board[0][0]) or\
            (board[0][2]==board[1][1]==board[2][0] and board[0][2]):
            return True

        return False


    def is_over(self, board=None):
        if not board:
            board = self.board
        if all([board[r][c] for r in range(3) for c in range(3)]):
            return True
        return False


    def bot(self):
        def alphabeta(board, alpha, beta, turn, depth):
            nonlocal bot_move
            if self.is_won(board):
                if turn!=self.bot_symbol:
                    return 1
                else:
                    return -1
            if self.is_over(board):
                return 0
            if turn==self.bot_symbol:
                value = -1
                for i, move in enumerate(next_moves(board)):
                    if not i and not depth:
                        bot_move = move # in case bot in losing position
                    newboard = deepcopy(board)
                    newboard[move[0]][move[1]] = turn
                    ab = alphabeta(newboard, alpha, beta, self.other_turn(turn), depth+1)
                    if not depth:
                        #print(ab, move)
                        pass
                    value = max(value, ab)
                    if value > alpha:
                        alpha = value
                        if not depth:
                            bot_move = move
                    if alpha >= beta:
                        break
                return value
            else:
                value = 1
                for move in next_moves(board):
                    newboard = deepcopy(board)
                    newboard[move[0]][move[1]] = turn
                    value = min(value, alphabeta(newboard, alpha, beta, self.other_turn(turn), depth+1))
                    beta = min(beta, value)
                    if alpha >= beta:
                        return value
                return value

        def next_moves(board):
            next_moves = []
            for r in range(3):
                for c in range(3):
                    if not board[r][c]:
                        next_moves.append((r,c))
            return next_moves


        bot_move = None
        alpha, beta = -1, 1
        board = self.board
        s = alphabeta(board, alpha, beta, self.curr_symbol, 0)
        # print('s', s)
        # print('bot_move', bot_move)
        self.move(bot_move[0], bot_move[1])


    def other_turn(self, turn):
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'
        return turn


    def start_game(self):
        self.startGUI()


    def turn_bot_off(self):
        if self.auto:
            self.auto = False
            self.auto_check.set(False)
        else:
            self.auto = True
            self.auto_check.set(True)
            if self.curr_symbol == self.bot_symbol:
                self.bot()


    def startGUI(self):
        self.root = tk.Tk()
        self.root_menu = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.root_menu, tearoff = False)
        self.root_menu.add_cascade(label = "File", menu = self.file_menu)
        self.file_menu.add_command(label = 'Quit', command=exit)
        self.file_menu.add_command(label = 'Reset', command=self.reset)
        self.auto_check = tk.BooleanVar()
        self.auto_check.set(self.auto)
        self.file_menu.add_checkbutton(label = 'Bot', variable=self.auto_check, command = self.turn_bot_off)
        self.root.config(menu = self.root_menu)
        self.window = tk.Frame(self.root)
        self.buttons = [[tk.Button(self.window, text = " ", fg = "black", width = 8, height = 4, bg = "white",\
            cursor = "hand2", command = lambda r=r,c=c:self.move(r,c)) for c in range(3)] for r in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row = r, column = c)
        # print(self.buttons)
        self.window.pack(side="top", fill="both", expand="true", padx=2, pady=2)
        if self.bot_symbol == self.starting_symbol:
            self.bot()
        self.root.mainloop()


def main():
    ttt = TicTacToe()
    ttt.start_game()

if __name__=="__main__":
    main()
