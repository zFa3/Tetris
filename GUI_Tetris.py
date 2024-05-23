import tkinter as tk
import random as rd

class Tetris:
    def __init__(self) -> None:
        self.ACIVE_PIECE = "$"
        self.PASSIVE_PIECE = "@"
        self.BACKGROUND_PIECE = " "
        self.WALL_PIECE = "|"
        self.BOTTOM_PIECE = "_"
        '''
        self.ACIVE_PIECE = 1
        self.PASSIVE_PIECE = 2
        self.BACKGROUND_PIECE = 3
        self.WALL_PIECE = 4
        self.BOTTOM_PIECE = 5
        '''
        self.lines = 0
        self.SIDE_LEN = 800
        self.TILE_SIZE = 30
        self.TILES = self.SIDE_LEN // self.TILE_SIZE
        self.LINE_WID = 1
        self.draw_lines = False

        self.gameActive = True

        # width and height
        self.dimensions = (4, 22)

        # randomness variable
        self.shuffle_bag = 50
        self.GRAVITY = 8
        self.colors = {
            0: "#FF5733",
            1: "#FFC300",
            2: "#FF33A1",
            3: "#33FF57",
            4: "#33A1FF",
            5: "#FF5733",
            6: "#FF33A1",
            7: "#33FF57",
            8: "#33A1FF",
            9: "#FFC300",
            10:"#FD3F59",
            11:"#0341AE",
            12:"#72CB3B",
            13:"#0FD500",
            14:"#39892F",
            15:"#FF3213",
            16:"#78256F",
            17:"#01EDFA"
        }
        self.U, self.R, self.D, self.L, self.C = (-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)
        self.U, self.R, self.D, self.L, self.C = (-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)
        self.bag_pieces = {
            # J Piece - Clockwise rotaations
            1:[
                [self.C, self.L, (self.L[0] + self.U[0], self.L[1] + self.U[1]) , self.R],
            ],
            # L Piece - Clockwise rotations
            2:[
                [self.L, self.R, (self.R[0] + self.U[0], self.R[1] + self.U[1]) , self.C],
            ],
            # o Piece - No rotations
            3:[
                [self.U, self.R, (self.R[0] + self.U[0], self.R[1] + self.U[1]) , self.C]
            ],
            # S Piece - Clockwise rotations
            4:[
                [self.D, self.L, (self.L[0] + self.U[0], self.L[1] + self.U[1]) , self.C],
            ],
            # Z Piece - Clockwise rotations
            5:[
                [self.U, self.L, (self.L[0] + self.D[0], self.L[1] + self.D[1]) , self.C],
            ],
            # T Piece - Clockwise Rotations
            6:[
                [self.L, self.R, self.U, self.C],
            ],
            # I piece - Clockwise Rotations
            7:[
                [self.L, self.R, (self.R[0] + self.R[0], self.R[1] + self.R[1]) , self.C],
            ]
        }

        self.piece_rotation = 0  # 0 - 3 index
        self.spawn_coords = [1, 3]
        self.held = False
        self.moved = 0
        self.keypressed = False
        self.piece_spawn = (self.spawn_coords[0] * (self.dimensions[0] + 2) + self.spawn_coords[1]) - 1
        self.pieceCenter = self.piece_spawn
        self.U, self.R, self.D, self.L, self.C = (-(self.dimensions[0] + 2), 1, (self.dimensions[0] + 2), -1, 0)
        self.pieces = {
#           "|### #### ###|"
#           "|#O# #### ###|"
#           "|### #### ###|"
#           "|### #### ###|"

            # CLOCKWISE ROTATIONS

            # J Piece - Clockwise rotaations
            1:[
                [self.C, self.L, self.L + self.U, self.R],
                [self.C, self.U, self.U + self.R, self.D],
                [self.C, self.R, self.R + self.D, self.L],
                [self.C, self.D, self.D + self.L, self.U]
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
                [self.L, self.U, self.U + self.R, self.C],
                [self.U, self.R, self.R + self.D, self.C],
                [self.R, self.D, self.D + self.L, self.C],
                [self.D, self.L, self.L + self.U, self.C]
            ],
            # Z Piece - Clockwise rotations
            5:[
                [self.R, self.U, self.U + self.L, self.C],
                [self.D, self.R, self.R + self.U, self.C],
                [self.L, self.D, self.D + self.R, self.C],
                [self.U, self.L, self.L + self.D, self.C]
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
        self.counter = 1
        self.board = self.set_board()
        '''
        self.board = list(
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|          |"
            "|@@@  @@@@@|"
            "|@@@@  @@@@|"
            "_____________"
#            "|$$$$$  $$$|"
#            "|$$$$  $$$$|"
        )
        '''
        self.root = tk.Tk()
        self.root.geometry(f"{self.SIDE_LEN}x{self.SIDE_LEN}")
        self.game_canvas = tk.Canvas(self.root)
        self.game_canvas.config(background="#ECECEC")
        self.game_canvas.config(width=self.SIDE_LEN, height=self.SIDE_LEN)
        self.root.title("Tetris")

        self.root.bind("r", self.reset)
        self.root.bind("x", self.keypress)
        self.root.bind("z", self.keypress)
        self.root.bind("<Up>", self.keypress)
        self.root.bind("<Left>", self.keypress)
        self.root.bind("<Right>", self.keypress)
        self.root.bind("<Down>", self.keypress)
        self.root.bind("<space>", self.keypress)
        self.root.bind("c", self.keypress)
        self.root.bind("<Escape>", self.destroy)

    def destroy(self, *args):
        self.root.destroy()
    
    def reset(self, *args):
        self.board = self.set_board()
        self.add_piece()
        self.lines = 0

    def clear_active(self, currentBoard):
        for i, t in enumerate(currentBoard):
            if t == self.ACIVE_PIECE:
                currentBoard[i] = self.BACKGROUND_PIECE
        return currentBoard

    def rotate_piece(self, currentBoard, asda):
        if "".join(currentBoard).count(self.ACIVE_PIECE):
            a = self.piece_rotation
            self.piece_rotation = (self.piece_rotation + asda) % len(self.pieces[self.current_piece])
            for i in self.pieces[self.current_piece][self.piece_rotation]:
                if currentBoard[self.pieceCenter + i] != self.BACKGROUND_PIECE and currentBoard[self.pieceCenter + i] != self.ACIVE_PIECE:
                    uh = self.pieceCenter
                    self.pieceCenter += self.L
                    self.piece_rotation = a
                    board, ans = self.rotate_piece_once(currentBoard[:])
                    if ans: return board, ans
                    else:
                        uh = self.pieceCenter
                        self.pieceCenter +=  self.D + self.R
                        self.piece_rotation = a
                        board, ans = self.rotate_piece_once(currentBoard[:])
                        if ans: return board, ans
                        else:
                            uh = self.pieceCenter
                            self.pieceCenter +=  self.D + self.L
                            self.piece_rotation = a
                            board, ans = self.rotate_piece_once(currentBoard[:])
                            if ans: return board, ans
                            else:        
                                self.pieceCenter = uh + self.R
                                self.piece_rotation = a
                                board, ans = self.rotate_piece_once(currentBoard[:])
                                if ans: return board, ans
                                else:
                                    uh = self.pieceCenter
                                    self.pieceCenter +=  self.D
                                    self.piece_rotation = a
                                    board, ans = self.rotate_piece_once(currentBoard[:])
                                    if ans: return board, ans
                                    else:
                                        self.piece_rotation = a; return currentBoard, False
            currentBoard = self.clear_active(currentBoard)
            for i in self.pieces[self.current_piece][self.piece_rotation]:
                currentBoard[self.pieceCenter + i] = self.ACIVE_PIECE
            return currentBoard, True
    
    def rotate_piece_once(self, currentBoard):
        a = self.piece_rotation
        self.piece_rotation = (self.piece_rotation + 1) % len(self.pieces[self.current_piece])
        for i in self.pieces[self.current_piece][self.piece_rotation]:
            if currentBoard[self.pieceCenter + i] != self.BACKGROUND_PIECE and currentBoard[self.pieceCenter + i] != self.ACIVE_PIECE:
                self.piece_rotation = a; return currentBoard, False
        currentBoard = self.clear_active(currentBoard)
        for i in self.pieces[self.current_piece][self.piece_rotation]:
            currentBoard[self.pieceCenter + i] = self.ACIVE_PIECE
        return currentBoard, True

    def set_bag(self):
        bag = [i + 1 for i in range(len(self.pieces))]
        #self.bag = [6 for i in range(len(self.pieces))]
        for _ in range(self.shuffle_bag):
            a, b = rd.randint(0, len(self.pieces) - 1), rd.randint(0, len(self.pieces) - 1)
            a1 = bag[a]
            bag[a] = bag[b]
            bag[b] = a1
        self.bag += bag
        #print(self.bag)

    def set_board(self):
        board = []
        for _ in range(self.dimensions[1]):
            board.append(self.WALL_PIECE)
            for _ in range(self.dimensions[0]):
                board.append(self.BACKGROUND_PIECE)
            board.append(self.WALL_PIECE)
        for _ in range((self.dimensions[0] + 3)):
            board.append(self.BOTTOM_PIECE)
        return board

    def add_piece(self):
        if self.board.count(self.ACIVE_PIECE) == 0:
            self.pieceCenter = self.piece_spawn
            self.piece_rotation = 0
            if len(self.bag) < 5:
                self.set_bag()
            self.current_piece = self.bag.pop(0)
            for i in self.pieces[self.current_piece][self.piece_rotation]:
                if self.board[self.piece_spawn + i] == self.PASSIVE_PIECE:
                    print("Score: ", self.lines); raise PermissionError("GAME OVER")
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
        self.held = False
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
        if self.board == self.set_board() and self.keypressed:
            self.moved = 50; self.lines += 3
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
        self.lines += 1
        self.board.insert(0, self.WALL_PIECE)
        for _ in range(self.dimensions[0]):
            self.board.insert(0, self.BACKGROUND_PIECE)
        self.board.insert(0, self.WALL_PIECE)
        a, b = row_index * (self.dimensions[0] + 2), (row_index+1) * (self.dimensions[0] + 2)
        self.board = (self.board[:a]) + (self.board[b:])
    
    def keypress(self, key):
        #print(key.char)
        self.keypressed = True
        try:
            if key.char == ("w") or key.keycode == 38:
                #self.board = self.move_up(self.board)
                #self.board = self.move_down(self.board)
                self.board, a = self.rotate_piece(self.board, 1)
                self.draw()
            elif key.char == "x":
                self.board, a = self.rotate_piece(self.board, 2)
                self.draw()

            if key.char == "z":
                self.board, a = self.rotate_piece(self.board, -1)
                self.draw()
            elif key.char == ("a") or key.keycode == 37:
                self.board = self.move_left(self.board)
                self.draw()
            elif key.char == ("s") or key.keycode == 32:
                self.board = self.hard_drop(self.board)
                self.board = self.solidify()
                self.find_filled()
                if self.board == self.set_board() and self.keypressed:
                    self.moved = 50; self.lines += 3
                #self.print_board(self.board)
                self.add_piece()
                self.game_tick()
                self.draw()
            elif key.keycode == 40:
                self.board, a = self.move_down(self.board)
                self.draw()
            elif key.char == ("d") or key.keycode == 39:
                self.board = self.move_right(self.board)
                self.draw()
            elif key.char == ("c") and not self.held:
                self.held = True
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
                return
        except: pass

    def game_loop(self):
        self.add_piece()
        self.draw()
        tick = 0
        while self.gameActive:
            self.game_tick()
            #tm.sleep(1/self.fps)
            self.add_piece()
                # check if you can move the element down
                    # move down
                # if it cant then we change it to "garbage"
            if tick > self.GRAVITY:
                a, cnMove = self.move_down(self.board)
                if not cnMove:
                    if self.counter > 15:
                        self.counter = 0
                        self.board = self.solidify()
                    else:
                        self.counter += 1
                else:
                    self.board = a
                    tick = 0
            tick += 1
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

    def format(self, hex):
        if len(hex) != 2:
            hex = "0" + hex
        return hex

    def draw(self):
        self.game_canvas.delete("all")
        self.game_canvas.create_text(self.SIDE_LEN//2, self.SIDE_LEN//2, text = self.lines, font=("Courier new", 150, "bold"), fill="#E5E5E5")
        if self.moved > 1:
            self.game_canvas.create_text(self.SIDE_LEN//2, self.SIDE_LEN//2, text="ALL CLEAR", font=("Arial", int(abs(self.moved * 1.3 - 30))), angle=(self.moved * 3.6)%360, fill=f"#{self.format(hex((self.moved * 3)%255)[2:])}{self.format(hex((self.moved * 5)%255)[2:])}{self.format(hex((self.moved * 175)%255)[2:])}")
            self.moved -= 2
        else:
            self.moved = 0
        for index, item in enumerate(self.pad_board(self.highlight_piece())):
            ind_col, ind_row = index // (self.SIDE_LEN//self.TILE_SIZE), index % (self.SIDE_LEN//self.TILE_SIZE)
            if item == self.ACIVE_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "#8EE6DB", outline="white")
        if self.draw_lines:
            for line in range(self.SIDE_LEN//self.TILE_SIZE):
                # iterates creating the vertical lines
                self.game_canvas.create_line(line * self.TILE_SIZE, 0, line*self.TILE_SIZE, self.SIDE_LEN, width = self.LINE_WID)
            for line in range(self.SIDE_LEN//self.TILE_SIZE):
                # create the horizontal lines
                self.game_canvas.create_line(0, line * self.TILE_SIZE, self.SIDE_LEN, line*self.TILE_SIZE, width = self.LINE_WID)
        for index, item in enumerate(self.pad_board(self.board)):
            ind_col, ind_row = index // (self.SIDE_LEN//self.TILE_SIZE), index % (self.SIDE_LEN//self.TILE_SIZE)
            if item == self.ACIVE_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = self.colors[int(self.current_piece % len(self.colors))])
            if item == self.PASSIVE_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "grey")
            if item == self.WALL_PIECE or item == self.BOTTOM_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "black")
        '''
            self.game_canvas.create_text((ind_row + 0.5) * self.TILE_SIZE, (ind_col + 0.5) * self.TILE_SIZE, text=item, font=("Arial", 15))
        '''
        for i in range(5):
            if len(self.bag) < 5:
                self.set_bag()
            self.draw_Pieces((25, (i * 5 + 3)), self.bag[i], self.colors[int(self.bag[i]) % len(self.colors)])
        try: self.draw_Pieces((15, 3), self.held_piece, self.colors[int(self.held_piece) % len(self.colors)])
        except: pass
        self.game_canvas.update()
        self.game_canvas.pack()

    def draw_Pieces(self, starting, piece, color):
        for item in self.bag_pieces[piece][0]:
            row_index, col_index = starting[0], starting[1]
            row_index += item[1]
            col_index += item[0  ]
            self.game_canvas.create_rectangle(row_index * self.TILE_SIZE, col_index * self.TILE_SIZE, (row_index + 1) * self.TILE_SIZE, (col_index + 1) * self.TILE_SIZE, fill = color)
            #self.game_canvas.create_text((row_index + 0.5) * self.TILE_SIZE, (col_index + 0.5) * self.TILE_SIZE,text=str(item[1]),font=("Arial", 15))

    def highlight_piece(self):
        board = self.hard_drop(self.board)
        return board

tetr = Tetris()
tetr.game_loop()
