import tkinter as tk
import random as rd

class Tetris:
    def __init__(self) -> None:
        self.ACIVE_PIECE = "#"
        self.PASSIVE_PIECE = "@"
        self.BACKGROUND_PIECE = " "
        self.WALL_PIECE = "|"
        self.BOTTOM_PIECE = "_"
        self.gameActive = True

        # width and height
        self.dimensions = (4, 22)
        self.U, self.R, self.D, self.L, self.C = (-(self.dimensions[0] + 2), 1, (self.dimensions[0] + 2), -1, 0)

        # randomness variable
        self.shuffle_bag = 100
        self.GRAVITY = 1

        self.piece_rotation = 0  # 0 - 3 index
        self.spawn_coords = [1, 3]
        self.piece_spawn = (self.spawn_coords[0] * (self.dimensions[0] + 2) + self.spawn_coords[1]) - 1
        self.pieceCenter = self.piece_spawn
        self.pieces = {
#           "|### #### ###|"
#           "|#O# #### ###|"
#           "|### #### ###|"
#           "|### #### ###|"

            # CLOCKWISE ROTATIONS

            # J Piece - Clockwise rotaations
            1:[
                [self.U, self.R, self.R + self.R, self.C],
                [self.R, self.D, self.D + self.D, self.C],
                [self.D, self.L, self.L + self.L, self.C],
                [self.L, self.U, self.U + self.U, self.C]
            ],
            # L Piece - Clockwise rotations
            2:[
                [self.L, self.R, self.R + self.U, self.C],
                [self.U, self.D, self.D + self.R, self.C],
                [self.R, self.L, self.L + self.D, self.C],
                [self.D, self.U, self.U + self.L, self.C]
            ],
            # o Piece - No rotations
            3:[
                [self.U, self.R, self.R + self.U, self.C]
            ],
            # S Piece - Clockwise rotations
            4:[
                [self.D, self.L, self.L + self.U, self.C],
                [self.L, self.U, self.U + self.R, self.C],
                [self.U, self.R, self.R + self.D, self.C],
                [self.R, self.D, self.D + self.L, self.C]
            ],
            # Z Piece - Clockwise rotations
            5:[
                [self.U, self.L, self.L + self.D, self.C],
                [self.R, self.U, self.U + self.L, self.C],
                [self.D, self.R, self.R + self.U, self.C],
                [self.L, self.D, self.D + self.R, self.C]
            ],
            # T Piece - Clockwise Rotations
            6:[
                [self.L, self.R, self.U, self.C],
                [self.U, self.R, self.D, self.C],
                [self.D, self.R, self.L, self.C],
                [self.L, self.D, self.U, self.C]
            ],
            # I piece - Clockwise Rotations
            7:[
                [self.L, self.R, self.R + self.R, self.C],
                [self.U, self.D, self.D + self.D, self.C],
                [self.U, self.U + self.L, self.U + self.R, self.U + self.R + self.R],
                [self.R, self.R + self.U, self.R + self.D, self.R + self.D + self.D]
            ]
        }
        self.bag = []; self.set_bag()
        self.current_piece = self.bag.pop(0)
        self.held_piece = "NONE"

        # ticks per second
        # frames per second
        self.fps = 1
        self.tps = 15
        self.board = []
        self.set_board()
    

        self.SIDE_LEN = 600
        self.TILE_SIZE = 20
        self.TILES = self.SIDE_LEN // self.TILE_SIZE
        self.LINE_WID = 1

        self.root = tk.Tk()
        self.root.geometry(f"{self.SIDE_LEN}x{self.SIDE_LEN}")
        self.game_canvas = tk.Canvas(self.root)
        self.game_canvas.config(background="#C0FFEE")

        self.root.bind("<Up>", self.keypress)
        self.root.bind("<Left>", self.keypress)
        self.root.bind("<Right>", self.keypress)
        self.root.bind("<space>", self.keypress)
        self.root.bind("c", self.keypress)

    def clear_active(self, currentBoard):
        for i, t in enumerate(currentBoard):
            if t == self.ACIVE_PIECE:
                currentBoard[i] = self.BACKGROUND_PIECE
        return currentBoard

    def rotate_piece(self, currentBoard):
        a = self.piece_rotation
        self.piece_rotation = (self.piece_rotation + 1) % len(self.pieces[self.current_piece])
        for i in self.pieces[self.current_piece][self.piece_rotation]:
            if currentBoard[self.pieceCenter + i] != self.BACKGROUND_PIECE and currentBoard[self.pieceCenter + i] != self.ACIVE_PIECE:
                self.piece_rotation = a; return currentBoard
        currentBoard = self.clear_active(currentBoard)
        for i in self.pieces[self.current_piece][self.piece_rotation]:
            currentBoard[self.pieceCenter + i] = self.ACIVE_PIECE
        return currentBoard

    def set_bag(self):
        self.bag = [i + 1 for i in range(len(self.pieces))]
        for _ in range(self.shuffle_bag):
            a, b = rd.randint(0, len(self.pieces) - 1), rd.randint(0, len(self.pieces) - 1)
            a1 = self.bag[a]
            self.bag[a] = self.bag[b]
            self.bag[b] = a1

    def set_board(self):
        self.board = []
        for _ in range(self.dimensions[1]):
            self.board.append(self.WALL_PIECE)
            for _ in range(self.dimensions[0]):
                self.board.append(self.BACKGROUND_PIECE)
            self.board.append(self.WALL_PIECE)
        for _ in range((self.dimensions[0] + 3)):
            self.board.append(self.BOTTOM_PIECE)

    def add_piece(self):
        if self.board.count(self.ACIVE_PIECE) == 0:
            self.pieceCenter = self.piece_spawn
            self.piece_rotation = 0
            if len(self.bag) == 0:
                self.set_bag()
            self.current_piece = self.bag.pop(0)
            for i in self.pieces[self.current_piece][self.piece_rotation]:
                self.board[self.piece_spawn + i] = self.ACIVE_PIECE

    def add_held(self, held):
        self.pieceCenter = self.piece_spawn
        self.piece_rotation = 0
        for i in self.pieces[held][self.piece_rotation]:
            self.board[self.piece_spawn + i] = self.ACIVE_PIECE

    def move_left(self, originalBoard):
        board = originalBoard[:]
        indexes = []
        for i, t in enumerate(board):
            if t == self.ACIVE_PIECE:
                indexes.append(i)
        indexes = sorted(indexes, key=lambda x:x%(self.dimensions[0] + 2))
        canMove = True
        for i in indexes:
            next_index = i + self.L
            if board[next_index] != self.BACKGROUND_PIECE and board[next_index] != self.ACIVE_PIECE:
                canMove = False
        if canMove:
            for i in indexes:
                next_index = i + self.L
                board[i] = self.BACKGROUND_PIECE
                board[next_index] = self.ACIVE_PIECE
            self.pieceCenter += self.L
        return board
    
    def move_right(self, originalBoard):
        board = originalBoard[:]
        indexes = []
        for i, t in enumerate(board):
            if t == self.ACIVE_PIECE:
                indexes.append(i)
        indexes = sorted(indexes, key=lambda x:x%(self.dimensions[0] + 2), reverse=True)
        canMove = True
        for i in indexes:
            next_index = i + self.R
            if board[next_index] != self.BACKGROUND_PIECE and board[next_index] != self.ACIVE_PIECE:
                canMove = False
        if canMove:
            for i in indexes:
                next_index = i + self.R
                board[i] = self.BACKGROUND_PIECE
                board[next_index] = self.ACIVE_PIECE
            self.pieceCenter += self.R
        return board

    def move_down(self, originalBoard):
        board = originalBoard[:]
        indexes = []
        for i, t in enumerate(board):
            if t == self.ACIVE_PIECE:
                indexes.append(i)
        indexes = sorted(indexes, reverse=True)
        canMove = True
        for i in indexes:
            next_index = i + self.D
            if board[next_index] != self.BACKGROUND_PIECE and board[next_index] != self.ACIVE_PIECE:
                canMove = False
                #print(board[next_index], next_index, i, board[i])
        if canMove:
            for i in indexes:
                next_index = i + self.D
                board[i] = self.BACKGROUND_PIECE
                board[next_index] = self.ACIVE_PIECE
            self.pieceCenter += self.D
        return board, canMove
    
    def hard_drop(self, originalBoard) -> str:
        board = originalBoard[:]
        canMove = True
        while canMove:
            indexes = []
            for i, t in enumerate(board):
                if t == self.ACIVE_PIECE:
                    indexes.append(i)
            indexes = sorted(indexes, reverse=True)
            if not indexes:
                break
            for i in indexes:
                next_index = i + self.D
                if board[next_index] != self.BACKGROUND_PIECE and board[next_index] != self.ACIVE_PIECE:
                    canMove = False
                    #print(board[next_index], next_index, i, board[i])
            if canMove:
                for i in indexes:
                    next_index = i + self.D
                    board[i] = self.BACKGROUND_PIECE
                    board[next_index] = self.ACIVE_PIECE
            #self.draw(board)
        self.add_piece()
        return board
    
    def soft_drop(self, originalBoard) -> str:
        board = originalBoard[:]
        canMove = True
        while canMove:
            indexes = []
            for i, t in enumerate(board):
                if t == self.ACIVE_PIECE:
                    indexes.append(i)
            indexes = sorted(indexes, reverse=True)
            if not indexes:
                break
            for i in indexes:
                next_index = i + self.D
                if board[next_index] != self.BACKGROUND_PIECE and board[next_index] != self.ACIVE_PIECE:
                    canMove = False
                    #print(board[next_index], next_index, i, board[i])
            if canMove:
                for i in indexes:
                    next_index = i + self.D
                    board[i] = self.BACKGROUND_PIECE
                    board[next_index] = self.ACIVE_PIECE
            #self.draw(board)
        self.add_piece()
        return board

    def move_up(self, board) -> str:
        indexes = []
        for i, t in enumerate(board):
            if t == self.ACIVE_PIECE:
                indexes.append(i)
        indexes = sorted(indexes)
        canMove = True
        for i in indexes:
            next_index = i + self.U
            if board[next_index] != self.BACKGROUND_PIECE and board[next_index] != self.ACIVE_PIECE:
                canMove = False
                #print(board[next_index], next_index, i, board[i])
        if canMove:
            for i in indexes:
                next_index = i + self.U
                board[i] = self.BACKGROUND_PIECE
                board[next_index] = self.ACIVE_PIECE
        return board

    def print_board(self, board):
        print("\033c")
        for i in range(self.dimensions[1] + 1):
            for j in range(self.dimensions[0] + 2):
                try:
                    #if i * (self.dimensions[0] + 2) + j == self.pieceCenter:
                    #    print("O", end = "")
                    #else:
                    print(board[i * (self.dimensions[0] + 2) + j], end = "")
                except: pass
            print()
    
    def print_debug(self, board):
        for i in range(self.dimensions[1] + 1):
            for j in range(self.dimensions[0] + 2):
                try:
                    if i * (self.dimensions[0] + 2) + j == self.pieceCenter:
                        print("O")
                    elif board[i * (self.dimensions[0] + 2) + j] == self.ACIVE_PIECE:
                        print(board[i * (self.dimensions[0] + 2) + j], end = "")
                    else:
                        print(" ", end = "")
                        #print(i * (self.dimensions[0] + 2) + j, end = "")
                except: pass
            print()
    
    def solidify(self):
        n = []
        for i in self.board:
            if i == self.ACIVE_PIECE:
                n.append(self.PASSIVE_PIECE)
            else: n.append(i)
        return n

    def game_tick(self):
        # move all elements down
        #self.board, moved = self.move_down(self.board)
        
        # check if there are any filled lines
        self.find_filled()
            # clear the filled lines
        # check if you lost the game
            # close the program
        # check if there are no active pieces on the board
            # add a new random piece to the board
    
    def find_filled(self) -> None:
        # check which ones are filled
        lines = [(i == self.PASSIVE_PIECE) for i in self.board]
        for i in range(self.dimensions[1]):
            if all(lines[i * (self.dimensions[0] + 2) + 1:(i + 1) * (self.dimensions[0] + 2) - 1]):
                self.remove_filled(i + 1)
    
    def remove_filled(self, row_index: int) -> None:
        self.board.insert(0, self.WALL_PIECE)
        for _ in range(self.dimensions[0]):
            self.board.insert(0, self.BACKGROUND_PIECE)
        self.board.insert(0, self.WALL_PIECE)
        a, b = row_index * (self.dimensions[0] + 2), (row_index+1) * (self.dimensions[0] + 2)
        self.board = (self.board[:a]) + (self.board[b:])
    
    def keypress(self, key):
        if key.char == ("w") or key.keycode == 38:
            #self.board = self.move_up(self.board)
            #self.board = self.move_down(self.board)
            self.board = self.rotate_piece(self.board)
            self.draw()
        elif key.char == ("a") or key.keycode == 37:
            self.board = self.move_left(self.board)
            self.draw()
        elif key.char == ("s") or key.keycode == 32:
            self.board = self.hard_drop(self.board)
            self.board = self.solidify()
            self.add_piece()
            self.game_tick()
            self.draw()
        elif key.char == ("d") or key.keycode == 39:
            self.board = self.move_right(self.board)
            self.draw()
        elif key.char == ("c"):
            self.board = self.clear_active(self.board)
            if self.held_piece == "NONE":
                self.held_piece = self.current_piece
                self.add_piece()
            else:
                self.add_held(self.held_piece)
                b = self.current_piece
                self.current_piece = self.held_piece
                self.held_piece =  b
            self.draw()

    def game_loop(self):
        self.draw()
        tick = 0
        while self.gameActive:
            if tick > 8:
                tick = 0
                #tm.sleep(1/self.fps)
                self.add_piece()
                a, cnMove = self.move_down(self.board)
                if not cnMove:
                    self.board = self.solidify()
                    # check if you can move the element down
                        # move down
                    # if it cant then we change it to "garbage"
                else:
                    self.board = a
            tick += 1
            self.game_tick()
            self.game_canvas.after(10)
            self.draw()

    def pad_board(self, board) -> list:
        new_list = []
        for i in range(self.dimensions[1] + 1):
            #new_list.append(" " * (self.TILES - (self.dimensions[0] + 2)))
            for a in range(self.dimensions[0] + 2):
                new_list.append(board[i * (self.dimensions[0] + 2) + a])
            for _ in range((self.TILES - (self.dimensions[0] + 2))):
                new_list.append(" ")
        return new_list

    def draw(self):
        self.game_canvas.config(width=self.SIDE_LEN, height=self.SIDE_LEN)
        self.game_canvas.delete("all")
        for line in range(self.SIDE_LEN//self.TILE_SIZE):
            # iterates creating the vertical lines
            self.game_canvas.create_line(line * self.TILE_SIZE, 0, line*self.TILE_SIZE, self.SIDE_LEN, width = self.LINE_WID)
        for line in range(self.SIDE_LEN//self.TILE_SIZE):
            # create the horizontal lines
            self.game_canvas.create_line(0, line * self.TILE_SIZE, self.SIDE_LEN, line*self.TILE_SIZE, width = self.LINE_WID)
        for index, item in enumerate(self.pad_board(self.board)):
            ind_col, ind_row = index // (self.SIDE_LEN//self.TILE_SIZE), index % (self.SIDE_LEN//self.TILE_SIZE)
            if item == self.ACIVE_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "#FABE57")
            if item == self.PASSIVE_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "#FA8857")
            if item == self.WALL_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "#0F0F0F")
        '''
        for index, item in enumerate(self.pad_board(self.board)):
            ind_col, ind_row = index // (self.SIDE_LEN//self.TILE_SIZE), index % (self.SIDE_LEN//self.TILE_SIZE)
            self.game_canvas.create_text((ind_row + 0.5) * self.TILE_SIZE, (ind_col + 0.5) * self.TILE_SIZE, text=item, font=("Arial", 15))
        '''
        self.game_canvas.update()
        self.game_canvas.pack()


tetr = Tetris()
#tetr.print_board(tetr.pieces[1])
#tetr.print_board(tetr.rotate_piece(tetr.pieces[1]))
tetr.game_loop()