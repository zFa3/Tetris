import tkinter as tk
import random as rd

class Tetris:
    def __init__(self) -> None:
        self.ACIVE_PIECE = "$"
        self.PASSIVE_PIECE = "@"
        self.BACKGROUND_PIECE = " "
        self.WALL_PIECE = "|"
        self.BOTTOM_PIECE = "_"
        self.showStringRepresentation = False

        self.lines = 0
        self.SIDE_LEN = 1000
        self.TILE_SIZE = 35
        self.TILES = self.SIDE_LEN // self.TILE_SIZE
        self.LINE_WID = 1

        self.gameActive = True

        # width and height
        self.dimensions = (10, 22)
        self.insta_soft_drop = True

        # (1 tick -> 10ms)
        # tick it takes to move auto move down
        self.GRAVITY = 250
        # ticks before 'solidification'
        self.ticks = 15

        self.BACKGROUND_COLOR = "#ECECEC"
        # self.BACKGROUND_COLOR = self.generate_random_color()
        
        # piece colors
        self.colors = ["#FF5733","#FFC300","#FF33A1","#33FF57","#33A1FF","#FF5733","#FF33A1","#33FF57","#33A1FF","#FFC300","#FD3F59","#0341AE","#72CB3B","#0FD500","#39892F","#FF3213","#78256F","#01EDFA"]
        self.colors = [self.generate_random_color() for _ in range(18)]

        self.U, self.R, self.D, self.L, self.C = (-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)

        self.bag_pieces = {
            # J Piece - Clockwise rotations
            1:[[self.C, self.L, (self.L[0] + self.U[0], self.L[1] + self.U[1]) , self.R]],
            # L Piece - Clockwise rotations
            2:[[self.L, self.R, (self.R[0] + self.U[0], self.R[1] + self.U[1]) , self.C]],
            # o Piece - No rotations
            3:[[self.U, self.R, (self.R[0] + self.U[0], self.R[1] + self.U[1]) , self.C]],
            # S Piece - Clockwise rotations
            4:[[self.D, self.L, (self.L[0] + self.U[0], self.L[1] + self.U[1]) , self.C]],
            # Z Piece - Clockwise rotations
            5:[[self.U, self.L, (self.L[0] + self.D[0], self.L[1] + self.D[1]) , self.C]],
            # T Piece - Clockwise Rotations
            6:[[self.L, self.R, self.U, self.C]],
            # I piece - Clockwise Rotations
            7:[[self.L, self.R, (self.R[0] + self.R[0], self.R[1] + self.R[1]) , self.C]]
        }

        self.piece_rotation = 0  # 0 - 3 index
        self.spawn_coords = [1, 3]
        self.moved = 0
        self.held = False
        self.keypressed = False
        self.piece_spawn = (self.spawn_coords[0] * (self.dimensions[0] + 2) + self.spawn_coords[1]) - 1
        self.pieceCenter = self.piece_spawn
        self.U, self.R, self.D, self.L, self.C = (-(self.dimensions[0] + 2), 1, (self.dimensions[0] + 2), -1, 0)

        self.pieces = {
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
                [self.U, self.L, self.D + self.L, self.C],
                [self.R, self.U, self.U + self.L, self.C],
                [self.D, self.R, self.U + self.R, self.C],
                [self.L, self.D, self.D + self.R, self.C],
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

        self.bag = []
        self.set_bag()
        self.current_piece = self.bag.pop(0)
        self.held_piece = "NONE"

        self.counter = 1
        self.board = self.set_board()

        self.root = tk.Tk()
        self.root.geometry(f"{self.SIDE_LEN}x{self.SIDE_LEN}")
        self.game_canvas = tk.Canvas(self.root)
        self.game_canvas.config(background=self.BACKGROUND_COLOR)
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

    def generate_random_color(self):
        return "#" + self.generateHex() + self.generateHex() + self.generateHex()
    
    def generateHex(self):
        integer = rd.randint(0, 15)
        return str(integer if integer < 10 else chr(integer + 55))

    def destroy(self, *args):
        self.root.destroy()
    
    def reset(self, *args):
        self.board = self.set_board()
        self.add_piece()
        self.lines = 0
        self.bag = []
        self.set_bag()

    def clear_active(self, currentBoard):
        for i, t in enumerate(currentBoard):
            if t == self.ACIVE_PIECE:
                currentBoard[i] = self.BACKGROUND_PIECE
        return currentBoard

    def rotate_piece(self, currentBoard, rotations):
        if "".join(currentBoard).count(self.ACIVE_PIECE):
            oldRotation = self.piece_rotation
            oldCenter = self.pieceCenter
            self.piece_rotation = (self.piece_rotation + rotations) % len(self.pieces[self.current_piece])
            for i in self.pieces[self.current_piece][self.piece_rotation]:
                if currentBoard[self.pieceCenter + i] != self.BACKGROUND_PIECE and currentBoard[self.pieceCenter + i] != self.ACIVE_PIECE:
                    self.pieceCenter += self.L
                    self.piece_rotation = oldRotation
                    board, ans = self.rotate_piece_once(currentBoard[:])
                    if ans: return board, ans
                    else:
                        self.pieceCenter = oldCenter + self.D + self.R
                        self.piece_rotation = oldRotation
                        board, ans = self.rotate_piece_once(currentBoard[:])
                        if ans: return board, ans
                        else:
                            self.pieceCenter = oldCenter + self.D + self.L
                            self.piece_rotation = oldRotation
                            board, ans = self.rotate_piece_once(currentBoard[:])
                            if ans: return board, ans
                            else:
                                self.pieceCenter = oldCenter + self.R
                                self.piece_rotation = oldRotation
                                board, ans = self.rotate_piece_once(currentBoard[:])
                                if ans: return board, ans
                                else:
                                    self.pieceCenter = oldCenter + self.U
                                    self.piece_rotation = oldRotation
                                    board, ans = self.rotate_piece_once(currentBoard[:])
                                    if ans: return board, ans
                                    else:
                                        self.piece_rotation = oldRotation
                                        self.pieceCenter = oldCenter
                                        return currentBoard, False
            # normal rotation
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
        newBag = list(set([i + 1 for i in range(len(self.pieces))]).difference(set(self.bag)))
        fullBag = self.bag[:]
        rd.shuffle(newBag)
        rd.shuffle(fullBag)
        self.bag += newBag
        self.bag += fullBag

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

    def move_sideways(self, originalBoard, moveRight):
        board = originalBoard[:]
        indexes = []
        for i, t in enumerate(board):
            if t == self.ACIVE_PIECE:
                indexes.append(i)
        indexes = sorted(indexes, key=lambda x:x%(self.dimensions[0] + 2), reverse = moveRight)
        canMove = True
        for i in indexes:
            next_index = i + (self.R if moveRight else self.L)
            if board[next_index] != self.BACKGROUND_PIECE and board[next_index] != self.ACIVE_PIECE:
                canMove = False
        if canMove:
            for i in indexes:
                next_index = i + (self.R if moveRight else self.L)
                board[i] = self.BACKGROUND_PIECE
                board[next_index] = self.ACIVE_PIECE
            self.pieceCenter += (self.R if moveRight else self.L)
        return board

    def move_down(self, originalBoard, insta_soft_drop):
        board = originalBoard[:]
        canMove = True
        trip = True
        while (canMove and insta_soft_drop) or (canMove and trip):
            self.pieceCenter += self.D
            indexes = []
            for i, t in enumerate(board):
                if t == self.ACIVE_PIECE:
                    indexes.append(i)
            indexes = sorted(indexes, reverse = True)
            if not indexes:
                break
            for i in indexes:
                next_index = i + self.D
                if board[next_index] != self.BACKGROUND_PIECE and board[next_index] != self.ACIVE_PIECE:
                    canMove = False
            if canMove:
                for i in indexes:
                    next_index = i + self.D
                    board[i] = self.BACKGROUND_PIECE
                    board[next_index] = self.ACIVE_PIECE
            trip = False
        if insta_soft_drop: self.pieceCenter -= self.D
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
            if not indexes: break
            for i in indexes:
                next_index = i + self.D
                if board[next_index] != self.BACKGROUND_PIECE and board[next_index] != self.ACIVE_PIECE:
                    canMove = False
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
        if canMove:
            for i in indexes:
                next_index = i + self.U
                board[i] = self.BACKGROUND_PIECE
                board[next_index] = self.ACIVE_PIECE
        return board
    
    def solidify(self):
        # once we drop a piece, we can now hold again
        self.held = False; n = []
        for i in self.board: n.append(self.PASSIVE_PIECE if i == self.ACIVE_PIECE else i)
        return n

    def game_tick(self):
        # move all elements down
        #self.board, moved = self.move_down(self.board)
        # check if there are any filled lines
        self.find_filled()
        # if self.board == self.set_board() and self.keypressed:
        #     self.moved = 50; self.lines += 3
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
        # print(key)
        self.keypressed = True
        try:
            if key.keycode == 2113992448:
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
            elif key.keycode == 2063660802:
                self.board = self.move_sideways(self.board, False)
                self.draw()
            elif key.keycode == 822083616:
                self.board = self.hard_drop(self.board)
                self.board = self.solidify()
                self.find_filled()
                if self.board == self.set_board() and self.keypressed:
                    self.moved = 50; self.lines += 3
                #self.print_board(self.board)
                self.add_piece()
                self.game_tick()
                self.draw()
            elif key.keycode == 2097215233:
                self.board, a = self.move_down(self.board, self.insta_soft_drop)
                self.draw()
            elif key.keycode == 2080438019:
                self.board = self.move_sideways(self.board, True)
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
            self.add_piece()
                # check if you can move the element down
                    # move down
                # if it cant then we change it to "garbage"
            if tick > self.GRAVITY:
                a, cnMove = self.move_down(self.board, False)
                if not cnMove:
                    if self.counter > (self.ticks):
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
            for a in range(self.dimensions[0] + 2): new_list.append(board[i * (self.dimensions[0] + 2) + a])
            for _ in range((self.TILES - (self.dimensions[0] + 2))): new_list.append(" ")
        return new_list

    def format(self, hex):
        return hex if len(hex) == 2 else "0" + hex

    def draw(self):
        # delete the entire frame
        self.game_canvas.delete("all")
        # create the score in the background
        self.game_canvas.create_text(self.SIDE_LEN//2, self.SIDE_LEN//2, text = self.lines, font=("Courier new", 150, "bold"), fill="#E5E5E5")
        # if there are no more pieces left on the board
        if self.moved > 1:
            # create the all clear text
            self.game_canvas.create_text(self.SIDE_LEN//2, self.SIDE_LEN//2, text="ALL CLEAR", font=("Arial", int(abs(self.moved * 1.3 - 30))), angle=(self.moved * 3.6)%360, fill=f"#{self.format(hex((self.moved * 3)%255)[2:])}{self.format(hex((self.moved * 5)%255)[2:])}{self.format(hex((self.moved * 175)%255)[2:])}")
            self.moved -= 2
        else:
            self.moved = 0
        for index, item in enumerate(self.pad_board(self.highlight_piece())):
            ind_col, ind_row = index // (self.SIDE_LEN//self.TILE_SIZE), index % (self.SIDE_LEN//self.TILE_SIZE)
            if item == self.ACIVE_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "#8EE6DB", outline="white")
        if self.LINE_WID > 0:
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
            if self.showStringRepresentation: self.game_canvas.create_text((ind_row + 0.5) * self.TILE_SIZE, (ind_col + 0.5) * self.TILE_SIZE, text=item, font=("Arial", 15))
        for i in range(5):
            if len(self.bag) < 5:
                self.set_bag()
            self.draw_Pieces((25, (i * 5 + 3)), self.bag[i], self.colors[int(self.bag[i]) % len(self.colors)])
        try: self.draw_Pieces((15, 3), self.held_piece, self.colors[int(self.held_piece) % len(self.colors)])
        except: pass

        # update and pack the main frame
        self.game_canvas.update()
        self.game_canvas.pack()

    # draw the different pieces
    def draw_Pieces(self, starting, piece, color):
        for item in self.bag_pieces[piece][0]:
            row_index, col_index = starting[0] + item[1], starting[1] + item[0]
            self.game_canvas.create_rectangle(row_index * self.TILE_SIZE, col_index * self.TILE_SIZE, (row_index + 1) * self.TILE_SIZE, (col_index + 1) * self.TILE_SIZE, fill = color)

    # highlight the active piece's shadow by
    # creating a new board and hard dropping the piece
    # on the copy board
    def highlight_piece(self):
        board = self.hard_drop(self.board)
        return board

tetr = Tetris()
tetr.game_loop()
