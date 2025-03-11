import tkinter as tk
import random as rd
import sys

class Tetris:
    def __init__(self) -> None:

        self.DEBUG = False
        self.ACIVE_PIECE = "$"
        self.PASSIVE_PIECE = "@"
        self.BACKGROUND_PIECE = " "
        self.WALL_PIECE = "|"
        self.BOTTOM_PIECE = "_"

        # lines cleared
        self.lines = 0

        # side length - window dimensions
        self.SIDE_LEN = 1000
        # the size of each tile
        self.TILE_SIZE = 30
        self.TILES = self.SIDE_LEN // self.TILE_SIZE
        self.LINE_WID = 3

        # game currently running
        self.gameActive = True

        # width and height
        self.dimensions = (10, 22)

        # turn on instant soft drop
        self.insta_soft_drop = True

        # randomness variable
        self.shuffle_bag = 50

        # gravity (the lower the number, the faster the pieces fall)
        self.GRAVITY = 12
        
        # colors for the tetrominoes
        self.colors = ["#FF5733","#FFC300","#FF33A1","#33FF57","#33A1FF","#FF5733","#FF33A1","#33FF57","#33A1FF","#FFC300","#FD3F59","#0341AE","#72CB3B","#0FD500","#39892F","#FF3213","#78256F","#01EDFA"]

        # directions, UP RIGHT DOWN LEFT CENTER
        self.U, self.R, self.D, self.L, self.C = (-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)

        # shows onyl one rotation of each of the tetrominoes
        self.bag_pieces = {
            # J Piece - Clockwise rotations
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

        # current piece's rotation index
        self.piece_rotation = 0 # 0 - 3 index
        # spawn coordinates for a new piece
        self.spawn_coords = [1, 3]
        # is there currently a piece being held (hold piece - C)
        self.held = False
        # used for all clears
        self.moved = 0
        self.keypressed = False
        self.piece_spawn = (self.spawn_coords[0] * (self.dimensions[0] + 2) + self.spawn_coords[1]) - 1
        self.pieceCenter = self.piece_spawn
        self.U, self.R, self.D, self.L, self.C = (-(self.dimensions[0] + 2), 1, (self.dimensions[0] + 2), -1, 0)
        
        # the full library of piece rotations indicies
        self.pieces = {

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
            # O Piece - No rotations
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
                # 5:[
                #     [self.R, self.U, self.U + self.L, self.C],
                #     [self.D, self.R, self.R + self.U, self.C],
                #     [self.L, self.D, self.D + self.R, self.C],
                #     [self.U, self.L, self.L + self.D, self.C]
                # ],
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
        # create the bag
        self.bag = []
        # initialize the bag
        self.set_bag()

        # set the current piece to the first item in the bag
        self.current_piece = self.bag.pop(0)
        # initialize the help peice as NONE
        self.held_piece = "NONE"

        # ticks per second
        self.tps = 15
        self.counter = 1
        # set the board, create the walls
        self.board = self.set_board()

        # create the root window
        self.root = tk.Tk()
        # set the size of the window
        self.root.geometry(f"{self.SIDE_LEN}x{self.SIDE_LEN}")
        # create the game canvas
        self.game_canvas = tk.Canvas(self.root)
        # set the bg color
        self.game_canvas.config(background="#ECECEC")
        # set the canvas size
        self.game_canvas.config(width=self.SIDE_LEN, height=self.SIDE_LEN)
        # set the title
        self.root.title("Tetris")

        # bind all the keys (change these for new keybinds)
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

    # destroy the window
    def destroy(self: "Tetris", *args) -> None:
        self.root.destroy()
        sys.exit()
    
    # reset the game, when r is pressed
    def reset(self: "Tetris", *args) -> None:
        # reset the board
        self.board = self.set_board()
        # set the bag to empty
        self.bag = []
        # refill the bag with new items
        self.set_bag()
        # add a new peice
        self.add_piece()
        # reset the score to zero
        self.lines = 0

    # this function clears all the active pieces on the board
    # can be used when swapping to a held piece
    def clear_active(self: "Tetris", currentBoard) -> list[str]:
        # for each cell, change it to a background cell if is currently active
        for i, t in enumerate(currentBoard):
            currentBoard[i] = self.BACKGROUND_PIECE if t == self.ACIVE_PIECE else currentBoard[i]
        # return the board
        return currentBoard

    # this function rotates the current active piece on the board peice
    def rotate_piece(self: "Tetris", currentBoard : list[str], rotations: int) -> tuple[list[str], bool]:
        if "".join(currentBoard).count(self.ACIVE_PIECE):
            oldRotation = self.piece_rotation
            oldCenter = self.pieceCenter
            self.piece_rotation = (self.piece_rotation + rotations) % len(self.pieces[self.current_piece])
            for i in self.pieces[self.current_piece][self.piece_rotation]:
                if currentBoard[self.pieceCenter + i] != self.BACKGROUND_PIECE and currentBoard[self.pieceCenter + i] != self.ACIVE_PIECE:
                    # special rotations (for s and z spins etc)
                    for offset in (self.L, self.R, self.D + self.R, self.D + self.L, self.U):
                        self.pieceCenter = oldCenter + offset
                        self.piece_rotation = oldRotation
                        board, res = self.rotate_piece_once(currentBoard[:])
                        if res: return board, res
                    self.piece_rotation = oldRotation
                    self.pieceCenter = oldCenter
                    return currentBoard, False
            # normal rotation
            currentBoard = self.clear_active(currentBoard)
            for i in self.pieces[self.current_piece][self.piece_rotation]:
                currentBoard[self.pieceCenter + i] = self.ACIVE_PIECE
            return currentBoard, True
    
    # rotate the current active peice 90 degrees
    def rotate_piece_once(self: "Tetris", currentBoard: list[str]) -> tuple[list[str], bool]:
        a = self.piece_rotation
        self.piece_rotation = (self.piece_rotation + 1) % len(self.pieces[self.current_piece])
        for i in self.pieces[self.current_piece][self.piece_rotation]:
            if currentBoard[self.pieceCenter + i] != self.BACKGROUND_PIECE and currentBoard[self.pieceCenter + i] != self.ACIVE_PIECE:
                self.piece_rotation = a; return currentBoard, False
        currentBoard = self.clear_active(currentBoard)
        for i in self.pieces[self.current_piece][self.piece_rotation]:
            currentBoard[self.pieceCenter + i] = self.ACIVE_PIECE
        return currentBoard, True
    
    # set the 'bag' (next pieces)
    def set_bag(self: "Tetris") -> None:
        newBag = list(set([i + 1 for i in range(len(self.pieces))]).difference(set(self.bag)))
        fullBag = self.bag[:]

        rd.shuffle(newBag)
        rd.shuffle(fullBag)

        self.bag += newBag
        self.bag += fullBag

    # set the board to a clean slate
    def set_board(self: "Tetris") -> list[str]:
        # create a new list (board representation)
        board = []
        for _ in range(self.dimensions[1]):
            board.append(self.WALL_PIECE)
            for _ in range(self.dimensions[0]):
                board.append(self.BACKGROUND_PIECE)
            board.append(self.WALL_PIECE)
        for _ in range((self.dimensions[0] + 3)):
            board.append(self.BOTTOM_PIECE)
        return board

    # add the next piece from the bag on the board
    def add_piece(self: "Tetris") -> None:
        # if there is no current active piece
        if self.board.count(self.ACIVE_PIECE) == 0:
            # set the piece center to the piece spawn location
            self.pieceCenter = self.piece_spawn
            self.piece_rotation = 0
            # if there are not enough pieces in the bag
            # to show to the player the next 5 pieces, we
            # add more pieces to the bag
            if len(self.bag) < 5: self.set_bag()
            # remove the first item and set it as our current piece
            self.current_piece = self.bag.pop(0)
            for i in self.pieces[self.current_piece][self.piece_rotation]:
                if self.board[self.piece_spawn + i] == self.PASSIVE_PIECE:
                    # if there is a passive piece on our spawn location then the game is over
                    # FIXME change this to the entire piece
                    print("Score: ", self.lines); self.destroy(); sys.exit()
                self.board[self.piece_spawn + i] = self.ACIVE_PIECE

    # add the held peice on the board
    def add_held(self: "Tetris", held: int) -> None:
        self.pieceCenter = self.piece_spawn
        self.piece_rotation = 0
        # for each offset for the piece 'held'
        for i in self.pieces[held][self.piece_rotation]:
            self.board[self.piece_spawn + i] = self.ACIVE_PIECE

    # move the current active piece to the left
    def move_left(self: "Tetris", originalBoard: list[str]) -> list[str]:
        # create a copy of the board
        board = originalBoard[:]
        indicies = []
        for i, t in enumerate(board):
            if t == self.ACIVE_PIECE:
                indicies.append(i)
        # sort based on column number, calculatable with index % width of board
        indicies = sorted(indicies, key=lambda x:x%(self.dimensions[0] + 2))
        can_move = True
        for i in indicies:
            can_move = can_move and not (board[i + self.L] != self.BACKGROUND_PIECE and board[i + self.L] != self.ACIVE_PIECE)
        if can_move:
            for i in indicies:
                board[i] = self.BACKGROUND_PIECE
                board[i + self.L] = self.ACIVE_PIECE
            self.pieceCenter += self.L
        return board
    
    # move the current active piece right
    def move_right(self: "Tetris", originalBoard: list[str]) -> list[str]:
        board = originalBoard[:]
        indicies = []
        for i, t in enumerate(board):
            if t == self.ACIVE_PIECE:
                indicies.append(i)
        indicies = sorted(indicies, key=lambda x:x%(self.dimensions[0] + 2), reverse=True)
        can_move = True
        for i in indicies:
            can_move = can_move and not (board[i + self.R] != self.BACKGROUND_PIECE and board[i + self.R] != self.ACIVE_PIECE)
        if can_move:
            for i in indicies:
                board[i] = self.BACKGROUND_PIECE
                board[i + self.R] = self.ACIVE_PIECE
            self.pieceCenter += self.R
        return board

    # move the current active piece down
    def move_down(self: "Tetris", originalBoard: list[str], insta_soft_drop: list[str]) -> tuple[list[str], bool]:
        if not insta_soft_drop:
            board = originalBoard[:]
            indicies = []
            for i, t in enumerate(board):
                if t == self.ACIVE_PIECE:
                    indicies.append(i)
            indicies = sorted(indicies, reverse=True)
            can_move = True
            for i in indicies:
                can_move = can_move and not (board[i + self.D] != self.BACKGROUND_PIECE and board[i + self.D] != self.ACIVE_PIECE)
            if can_move:
                for i in indicies:
                    board[i] = self.BACKGROUND_PIECE
                    board[i + self.D] = self.ACIVE_PIECE
                self.pieceCenter += self.D
            return board, can_move
        else:
            board = originalBoard[:]
            can_move = True
            while can_move:
                self.pieceCenter += self.D
                indicies = []
                for i, t in enumerate(board):
                    if t == self.ACIVE_PIECE:
                        indicies.append(i)
                indicies = sorted(indicies, reverse=True)
                if not indicies: break
                for i in indicies:
                    can_move = can_move and not (board[i + self.D] != self.BACKGROUND_PIECE and board[i + self.D] != self.ACIVE_PIECE)
                if can_move:
                    for i in indicies:
                        board[i] = self.BACKGROUND_PIECE
                        board[i + self.D] = self.ACIVE_PIECE
            self.pieceCenter -= self.D
            return board, can_move
    
    def hard_drop(self: "Tetris", originalBoard: list[str]) -> list[str]:
        board = originalBoard[:]
        can_move = True
        while can_move:
            indicies = []
            for i, t in enumerate(board):
                if t == self.ACIVE_PIECE:
                    indicies.append(i)
            indicies = sorted(indicies, reverse=True)
            if not indicies:
                break
            for i in indicies:
                can_move = can_move and not (board[i + self.D] != self.BACKGROUND_PIECE and board[i + self.D] != self.ACIVE_PIECE)
            if can_move:
                for i in indicies:
                    board[i] = self.BACKGROUND_PIECE
                    board[i + self.D] = self.ACIVE_PIECE
            #self.draw(board)
        return board
    
    def move_up(self: "Tetris", board: list[str]) -> list[str]:
        indicies = []
        for i, t in enumerate(board):
            if t == self.ACIVE_PIECE:
                indicies.append(i)
        indicies = sorted(indicies)
        can_move = True
        for i in indicies:
            can_move = can_move and not (board[i + self.U] != self.BACKGROUND_PIECE and board[i + self.U] != self.ACIVE_PIECE)
        if can_move:
            for i in indicies:
                board[i] = self.BACKGROUND_PIECE
                board[i + self.U] = self.ACIVE_PIECE
        return board
    
    # change all the active pieces to passive pieces
    def solidify(self: "Tetris") -> list[str]:
        # we can now hold a new piece since we have placed a piece
        self.held = False
        n = [] # create a new board
        for i in self.board: # for each item in the old board
            n.append(i if i != self.ACIVE_PIECE else self.PASSIVE_PIECE)
        return n
    
    def find_filled(self: "Tetris") -> None:
        # check which lines are filled, and remove any that are filled
        lines = [(i == self.PASSIVE_PIECE) for i in self.board]
        for i in range(self.dimensions[1]):
            if all(lines[i * (self.dimensions[0] + 2) + 1:(i + 1) * (self.dimensions[0] + 2) - 1]):
                self.remove_filled(i + 1)

    def remove_filled(self: "Tetris", row_index: int) -> None:
        self.lines += 1
        self.board.insert(0, self.WALL_PIECE)
        for _ in range(self.dimensions[0]):
            self.board.insert(0, self.BACKGROUND_PIECE)
        self.board.insert(0, self.WALL_PIECE)
        a, b = row_index * (self.dimensions[0] + 2), (row_index+1) * (self.dimensions[0] + 2)
        self.board = (self.board[:a]) + (self.board[b:])
    
    def keypress(self: "Tetris", event: tk.Event) -> None:
        if self.DEBUG: print(event)
        self.keypressed = True
        try:
            # use event.keysym (key symbol)
            if event.keysym == "Up":
                self.board, _ = self.rotate_piece(self.board, 1)
            elif event.char == "x":
                self.board, _ = self.rotate_piece(self.board, 2)
            if event.char == "z":
                self.board, _ = self.rotate_piece(self.board, -1)
            elif event.keysym == "Left":
                self.board = self.move_left(self.board)
            elif event.keysym == "space":
                self.board = self.hard_drop(self.board)
                self.board = self.solidify()
                if self.board == self.set_board() and self.keypressed:
                    self.moved = 50; self.lines += 3
                self.add_piece()
                self.find_filled()
                if self.board == self.set_board() and self.keypressed:
                    self.moved = 50; self.lines += 3
            elif event.keysym == "Down":
                self.board, _ = self.move_down(self.board, self.insta_soft_drop)
            elif event.keysym == "Right":
                self.board = self.move_right(self.board)
            elif event.char == ("c") and not self.held:
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
        except: pass

    def game_loop(self: "Tetris") -> None:
        self.add_piece()
        tick = 0
        while self.gameActive:
            self.find_filled()
            if self.board == self.set_board() and self.keypressed:
                self.moved = 50; self.lines += 3
            self.add_piece()
                # check if you can move the element down
                    # move down
                # if it cant then we change it to "garbage"
            if tick > self.GRAVITY:
                a, cnMove = self.move_down(self.board, False)
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

    def pad_board(self: "Tetris", board) -> list:
        new_list = []
        for i in range(self.dimensions[1] + 1):
            for a in range(self.dimensions[0] + 2):
                new_list.append(board[i * (self.dimensions[0] + 2) + a])
            for _ in range((self.TILES - (self.dimensions[0] + 2))):
                new_list.append(" ")
        return new_list

    def format(self: "Tetris", hex: str) -> str:
        return "0" if len(hex) != 2 else "" + hex

    # draw on the canvas
    def draw(self: "Tetris") -> None:
        # delete everythin on the canvas
        self.game_canvas.delete("all")
        # create a faint text in the background, showing the current score
        self.game_canvas.create_text(self.SIDE_LEN//2, self.SIDE_LEN//2, text = self.lines, font=("Courier new", 150, "bold"), fill="#E5E5E5")
        # create an all clear text
        if self.moved > 1:
            self.game_canvas.create_text(self.SIDE_LEN//2, self.SIDE_LEN//2, text="ALL CLEAR", font=("Arial", int(abs(self.moved * 1.3 - 30))), angle=(self.moved * 3.6)%360, fill=f"#{self.format(hex((self.moved * 3)%255)[2:])}{self.format(hex((self.moved * 5)%255)[2:])}{self.format(hex((self.moved * 175)%255)[2:])}")
            self.moved -= 2
        else: self.moved = 0
        # create the shadow of the current piece
        for index, item in enumerate(self.pad_board(self.highlight_piece())):
            ind_col, ind_row = index // (self.SIDE_LEN//self.TILE_SIZE), index % (self.SIDE_LEN//self.TILE_SIZE)
            if item == self.ACIVE_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "#8EE6DB", outline="white")
        if self.LINE_WID:
            for line in range(self.SIDE_LEN//self.TILE_SIZE):
                # iterates creating the vertical lines
                self.game_canvas.create_line(line * self.TILE_SIZE, 0, line*self.TILE_SIZE, self.SIDE_LEN, width = self.LINE_WID)
            for line in range(self.SIDE_LEN//self.TILE_SIZE):
                # create the horizontal lines
                self.game_canvas.create_line(0, line * self.TILE_SIZE, self.SIDE_LEN, line*self.TILE_SIZE, width = self.LINE_WID)
        # draw the items on the board
        for index, item in enumerate(self.pad_board(self.board)):
            ind_col, ind_row = index // (self.SIDE_LEN//self.TILE_SIZE), index % (self.SIDE_LEN//self.TILE_SIZE)
            if item == self.ACIVE_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = self.colors[int(self.current_piece % len(self.colors))])
            if item == self.PASSIVE_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "grey")
            if item == self.WALL_PIECE or item == self.BOTTOM_PIECE:
                self.game_canvas.create_rectangle((ind_row) * self.TILE_SIZE, (ind_col) * self.TILE_SIZE, (ind_row + 1) * self.TILE_SIZE, (ind_col + 1) * self.TILE_SIZE, fill = "black")
            if self.DEBUG: self.game_canvas.create_text((ind_row + 0.5) * self.TILE_SIZE, (ind_col + 0.5) * self.TILE_SIZE, text=item, font=("Arial", 15))
        if len(self.bag) < 5: self.set_bag()
        # draw the top 5 items in the bag
        for i in range(5): self.draw_Pieces((25, (i * 5 + 3)), self.bag[i], self.colors[int(self.bag[i]) % len(self.colors)])
        try: self.draw_Pieces((15, 3), self.held_piece, self.colors[int(self.held_piece) % len(self.colors)])
        except: pass
        # update then pack the canvas
        self.game_canvas.update()
        self.game_canvas.pack()

    def draw_Pieces(self: "Tetris", starting: tuple[int, int], piece: int, color: str) -> None:
        for item in self.bag_pieces[piece][0]:
            row_index, col_index = starting[0], starting[1]
            row_index += item[1]
            col_index += item[0]
            self.game_canvas.create_rectangle(row_index * self.TILE_SIZE, col_index * self.TILE_SIZE, (row_index + 1) * self.TILE_SIZE, (col_index + 1) * self.TILE_SIZE, fill = color)
            if self.DEBUG: self.game_canvas.create_text((row_index + 0.5) * self.TILE_SIZE, (col_index + 0.5) * self.TILE_SIZE,text=str(item[1]),font=("Arial", 15))

    # highlight the current piece's hard drop location
    def highlight_piece(self: "Tetris") -> list[str]:
        return self.hard_drop(self.board)

tetr = Tetris()
tetr.game_loop()
