import pygame as _pygame
from settings import settings
import tkinter as tk
from collections import defaultdict

MOVE_HIGHLIGHT_RADIUS = settings["board"]["move_highlight_radius"]
CAPTURE_HIGHLIGHT_RADIUS = settings["board"]["capture_highlight_radius"]
CAPTURE_HIGHLIGHT_WIDTH = settings["board"]["capture_highlight_width"]
PROMOTION_HIGHLIGHT_RADIUS = settings["board"]["promotion_highlight_radius"]
PIECE_SIZE = settings["board"]["piece_size"]
BOARD_SIZE = settings["board"]["size"]

WHITE = tuple(settings["colors"]["white"])
BLACK = tuple(settings["colors"]["black"])
RED = tuple(settings["colors"]["red"])
GREEN = tuple(settings["colors"]["green"])

BROWN = _pygame.Color("#b58863")
BEIGE = _pygame.Color("#f0d9b5")
HIGHLIGHT = _pygame.Color("#8877DD99")
MOVE_HIGHLIGHT = _pygame.Color("#5fa14460")
CAPTURE_HIGHLIGHT = _pygame.Color("#d42a2a60")
PROMOTION_HIGHLIGHT = _pygame.Color("#fff7005f")

CAPTURE_SOUND = _pygame.mixer.Sound("Assets/Sounds/capture.wav")
MOVE_SOUND = _pygame.mixer.Sound("Assets/Sounds/move.wav")
CASTLE_SOUND = _pygame.mixer.Sound("Assets/Sounds/castle.wav")
CHECK_SOUND = _pygame.mixer.Sound("Assets/Sounds/check.wav")
PROMOTE_SOUND = _pygame.mixer.Sound("Assets/Sounds/promote.wav")
GAME_START_SOUND = _pygame.mixer.Sound("Assets/Sounds/game-start.wav")
GAME_END_SOUND = _pygame.mixer.Sound("Assets/Sounds/game-end.wav")
TEN_SECONDS_SOUND = _pygame.mixer.Sound("Assets/Sounds/tenseconds.wav")
NOTIFY_SOUND = _pygame.mixer.Sound("Assets/Sounds/notify.wav")
ILLEGAL_SOUND = _pygame.mixer.Sound("Assets/Sounds/illegal.wav")

BOARD_NAME_CONFIG = [
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["r", "n", "b", "q", "k", "b", "n", "r"],
] # Uppercase for white, lowercase for black

PIECE_DEFAULT_ATTRIBUTES = {"can_double_move": False, 
                            "can_take_en_passant": False,
                            "can_be_en_passant": False,
                            "can_castle": False,
                            "can_promotion": False,
                            "checkable": False,
                            "takeable": True}

show_debug_info = False

class BoardLocation:
    def __init__(self, rank:int, file:int):
        self.rank = rank
        self.file = file
    
    def __str__(self):
        if self.rank < 0 or self.rank > 7 or self.file < 0 or self.file > 7:
            return "None"
        else:
            return f"{["a", "b", "c", "d", "e", "f", "g", "h"][self.file]}{self.rank + 1}"
    
    def __eq__(self, other):
        if isinstance(other, BoardLocation):
            return self.rank == other.rank and self.file == other.file
        else:
            return NotImplemented

    def update_to_position(self, offset_rank:int, offset_file:int):
        self.rank += offset_rank
        self.file += offset_file

class Movement:
    def __init__(self, to:BoardLocation, need_to_be_clear:list[list[BoardLocation]], type:str):
        self.to = to
        self.need_to_be_clear = need_to_be_clear
        self.type = type # Type of Movement: "normal", "capture", "jump", "jump-capture", "promotion", etc.
    
    def __str__(self):
        clear_str = ', '.join( 
            '[' + ', '.join(str(loc) for loc in group) + ']'
            for group in self.need_to_be_clear
        )
        return f"Move to {self.to}, clears: {clear_str if clear_str else '[]'}, type: {self.type}"
    
    def update_to_position(self, offset_rank:int, offset_file:int):
        self.to.update_to_position(offset_rank, offset_file)
        for clear_spaces in self.need_to_be_clear:
            for clear_space in clear_spaces:
                clear_space.update_to_position(offset_rank, offset_file)

class Pattern:
    def __init__(self, name: str, pattern: list[Movement]):
        self.name = name
        self.pattern = pattern # list of Movement objects
    
    def __str__(self):
        moves_str = "\n  ".join(str(movement) for movement in self.pattern)
        return f"{self.name.capitalize()} Moves:\n  {moves_str}"

    def update_to_position(self, location:BoardLocation, direction:int) -> list[Movement]:
        rank_offset = location.rank
        file_offset = location.file
        
        new_pattern = []
        for movement in self.pattern:
            # offset the main movement location
            original_move = movement.to
            new_move_location = BoardLocation(
                rank_offset + direction * original_move.rank,
                file_offset + direction * original_move.file
            )
            # offset each group of clear spaces
            new_clear_spaces = [
                [
                    BoardLocation(
                        rank_offset + direction * cs.rank, # flip dir
                        file_offset + direction * cs.file
                    )
                    for cs in clear_group
                ]
                for clear_group in movement.need_to_be_clear]
            # create a new move with updated positions
            new_movement = Movement(new_move_location, new_clear_spaces, movement.type)
            new_pattern.append(new_movement)

        return new_pattern

class ClassicPiecesMovement:
    @staticmethod
    def generate_linear_moves(directions: list[tuple[int, int]], max_distance: int) -> list[Movement]:
        moves = []
        for dx, dy in directions:
            for dist in range(1, max_distance + 1):
                destination = BoardLocation(dist * dx, dist * dy)
                clear_path = [BoardLocation(i * dx, i * dy) for i in range(1, dist)] # spaces before the end
                if clear_path:
                    moves.append(Movement(destination, [clear_path], "normal"))
                    moves.append(Movement(destination, [clear_path], "capture"))
                else:
                    # for adjacent steps (like king), no need_to_be_clear
                    moves.append(Movement(destination, [], "normal"))
                    moves.append(Movement(destination, [], "capture"))
        return moves

    pawn_movement = Pattern("pawn", [
        Movement(BoardLocation(1, 0), [], "normal"),
        Movement(BoardLocation(1, 1), [], "capture"),
        Movement(BoardLocation(1, -1), [], "capture")
    ])

    knight_movement = Pattern("knight", [
        Movement(BoardLocation(2, 1), [], "jump"), Movement(BoardLocation(2, 1), [], "jump-capture"),
        Movement(BoardLocation(2, -1), [], "jump"), Movement(BoardLocation(2, -1), [], "jump-capture"),
        Movement(BoardLocation(-2, 1), [], "jump"), Movement(BoardLocation(-2, 1), [], "jump-capture"),
        Movement(BoardLocation(-2, -1), [], "jump"), Movement(BoardLocation(-2, -1), [], "jump-capture"),
        Movement(BoardLocation(1, 2), [], "jump"), Movement(BoardLocation(1, 2), [], "jump-capture"),
        Movement(BoardLocation(1, -2), [], "jump"), Movement(BoardLocation(1, -2), [], "jump-capture"),
        Movement(BoardLocation(-1, 2), [], "jump"), Movement(BoardLocation(-1, 2), [], "jump-capture"),
        Movement(BoardLocation(-1, -2), [], "jump"), Movement(BoardLocation(-1, -2), [], "jump-capture")
    ])

    bishop_movement = Pattern(
        "bishop", generate_linear_moves([(1, 1), (1, -1), (-1, 1), (-1, -1)], 8)
    )

    rook_movement = Pattern(
        "rook", generate_linear_moves([(1, 0), (-1, 0), (0, 1), (0, -1)], 8)
    )

    queen_movement = Pattern(
        "queen", generate_linear_moves([
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ], 8)
    )

    king_movement = Pattern("king", [
        Movement(BoardLocation(1, 0), [], "normal"), Movement(BoardLocation(1, 0), [], "capture"),
        Movement(BoardLocation(-1, 0), [], "normal"), Movement(BoardLocation(-1, 0), [], "capture"),
        Movement(BoardLocation(0, 1), [], "normal"), Movement(BoardLocation(0, 1), [], "capture"),
        Movement(BoardLocation(0, -1), [], "normal"), Movement(BoardLocation(0, -1), [], "capture"),
        Movement(BoardLocation(1, 1), [], "normal"), Movement(BoardLocation(1, 1), [], "capture"),
        Movement(BoardLocation(1, -1), [], "normal"), Movement(BoardLocation(1, -1), [], "capture"),
        Movement(BoardLocation(-1, 1), [], "normal"), Movement(BoardLocation(-1, 1), [], "capture"),
        Movement(BoardLocation(-1, -1), [], "normal"), Movement(BoardLocation(-1, -1), [], "capture")
    ])

class Piece:
    def __init__(self, 
                 name:str,
                 pattern:Pattern, 
                 square:BoardLocation, 
                 colour:str, # "white" or "black"
                 sprite:_pygame.Surface = None, 
                 worth:int = None,
                 direction:int = 1,
                 size:int = PIECE_SIZE,
                 attributes:dict = None,
                 theme:int = 1):
        self.name = name
        self.theme = theme
        if sprite is None:
            sprite = self.try_get_automatic_sprite(name, colour)
        else:
            sprite = _pygame.transform.scale(sprite, (size, size))
        self.sprite = sprite
        self.square = square
        if worth is None:
            worth = self.try_get_default_worth(name)
        self.worth = worth
        self.colour = colour
        self.legal_moves:list[Movement] = []
        self.pattern = pattern
        self.movement = pattern.update_to_position(square, direction)
        self.direction = direction # 1 for white, -1 for black
        self.size = size
        self.attributes = PIECE_DEFAULT_ATTRIBUTES.copy()
        if attributes: self.attributes.update(attributes) # this changes values of attributes if they are provided
        self.selected = False
        self.square_log:list[BoardLocation] = []
    
    def try_get_automatic_sprite(self, name:str, colour:str):
        try:
            image = _pygame.image.load(f"Assets\\Sprites\\Theme{self.theme}\\{colour[0].lower()}_{name.lower()}.png")
            return image
        except FileNotFoundError:
            return self.create_placeholder_piece(BLACK if name.islower() else WHITE, name)

    def try_get_default_worth(self, name:str):
        """
        Returns the default worth of the piece based on its name.
        If the piece is not found, returns 0.
        """
        default_worths = {
            "p": 1,
            "r": 5,
            "n": 3,
            "b": 3,
            "q": 9,
            "k": 0
        }
        return default_worths.get(name.lower(), 0)

    def create_placeholder_piece(self, color:_pygame.Color, piece_char:str):
        surf = _pygame.Surface((50, 50), _pygame.SRCALPHA)
        color_rgb = color
        _pygame.draw.circle(surf, color_rgb, (25, 25), 20)
        font = _pygame.font.SysFont("Arial", 24, bold=True)
        text = font.render(piece_char.upper(), True, BLACK if color == WHITE else WHITE)
        text_rect = text.get_rect(center=(25, 25))
        surf.blit(text, text_rect)
        return surf

    @staticmethod
    def check_move_legality(move:Movement, opposite_pieces_locations:list[BoardLocation], same_pieces_locations:list[BoardLocation], allow_takes:bool = True) -> bool:
        """
        Check if the move is legal for the piece.
        This is a basic check and does not consider checks or checkmates.
        """
        legal = True
        if not (0 <= move.to.rank < 8 and 0 <= move.to.file < 8):
            legal = False
        if move.type in ["normal", "capture"]: # check for pieces in the way, all 'need_to_be_clear' squares are not occupied
            blocked = False
            for piece_location in opposite_pieces_locations + same_pieces_locations:
                for clear_squares in move.need_to_be_clear:
                    for square in clear_squares:
                        if piece_location == square:
                            legal = False
                            blocked = True
                            break
                    if blocked: break
        if not allow_takes and "capture" in move.type:
            legal = False
        if move.type == "normal":
            if move.to in opposite_pieces_locations + same_pieces_locations: legal = False
        elif move.type == "capture":
            if move.to not in opposite_pieces_locations: legal = False
        elif move.type == "jump": # this is if the piece can jump over other pieces
            if move.to in opposite_pieces_locations + same_pieces_locations: legal = False
        elif move.type == "jump-capture": # this is if the piece can jump over other pieces and capture them
            if move.to not in opposite_pieces_locations: legal = False
        return legal

    def update(self, opposite_pieces_locations:list[BoardLocation], same_pieces_locations:list[BoardLocation]):
        if not self.selected: return # if the piece is not selected, do not update its legal moves
        # Update the position of the piece for the movement pattern
        self.movement = self.pattern.update_to_position(self.square, self.direction)
        # Update the legal moves of a piece
        self.legal_moves = []
        for move in self.movement:
            if self.check_move_legality(move, opposite_pieces_locations, same_pieces_locations):
                self.legal_moves.append(move)
        
        # Double Moving
        double_movement_legal_moves = []
        if self.attributes["can_double_move"] and len(self.square_log) == 0:
            for move in self.legal_moves:
                if "capture" in move.type: continue # Do not double move if the piece can capture
                double_movement = self.pattern.update_to_position(move.to, self.direction)
                for double_move in double_movement:
                    if self.check_move_legality(double_move, opposite_pieces_locations, same_pieces_locations, False):
                        double_movement_legal_moves.append(double_move)
            self.legal_moves.extend(double_movement_legal_moves)
        
        # Promotion
        if self.attributes["can_promotion"]:
            for move in self.legal_moves:
                if move.to.rank == (7 if self.colour == "white" else 0): move.type = move.type + "-promotion"

    def move(self, new_square:BoardLocation):
        self.square_log.append(self.square) # log the previous square
        self.square = new_square # Move the piece to the new square
    
    def unmove(self): 
        # Unmove the piece to the previous square
        if self.square_log:
            self.square = self.square_log.pop()
    
    def promote(self):
        """
        Promotes the piece to a queen.
        This is a simple implementation, you can change it to promote to any piece.
        """
        self.name = "Q" if self.colour == "white" else "q"
        self.sprite = self.try_get_automatic_sprite(self.name, self.colour)
        self.pattern = ClassicPiecesMovement.queen_movement
        self.attributes["can_promotion"] = False # Disable promotion after promoting
        self.worth = self.try_get_default_worth(self.name) # Update the worth of the piece

    def draw_legal_moves(self, screen:_pygame.Surface, ranks_locations:list[int], files_locations:list[int]):
        for move in self.legal_moves:
            if "promotion" in move.type:
                if "normal" in move.type or "jump" in move.type:
                    _pygame.draw.circle(screen, PROMOTION_HIGHLIGHT, (ranks_locations[move.to.file], files_locations[move.to.rank]), PROMOTION_HIGHLIGHT_RADIUS)
                elif "capture" in move.type:
                    _pygame.draw.circle(screen, PROMOTION_HIGHLIGHT, (ranks_locations[move.to.file], files_locations[move.to.rank]), CAPTURE_HIGHLIGHT_RADIUS, CAPTURE_HIGHLIGHT_WIDTH)
            elif "capture" in move.type:
                _pygame.draw.circle(screen, CAPTURE_HIGHLIGHT, (ranks_locations[move.to.file], files_locations[move.to.rank]), CAPTURE_HIGHLIGHT_RADIUS, CAPTURE_HIGHLIGHT_WIDTH)
            elif "normal" in move.type or "jump" in move.type:
                _pygame.draw.circle(screen, MOVE_HIGHLIGHT, (ranks_locations[move.to.file], files_locations[move.to.rank]), MOVE_HIGHLIGHT_RADIUS)
    
    def draw(self, screen:_pygame.Surface, ranks_locations:list[int], files_locations:list[int], turn:str):
        self.sprite = _pygame.transform.scale(self.sprite, (self.size, self.size))
        screen.blit(self.sprite, (ranks_locations[self.square.file] - self.size / 2, files_locations[self.square.rank] - self.size / 2))
        if self.selected and turn == self.colour:
            self.draw_legal_moves(screen, ranks_locations, files_locations)

class Move:
    def __init__(self,
                 piece: Piece,
                 at:BoardLocation,
                 to:BoardLocation,
                 captured:Piece = None,
                 castling:bool = False,
                 en_passant:bool = False,
                 promotion:Piece = None,
                 check:bool = False, 
                 checkmate:bool = False):
        self.piece = piece
        self.at = at
        self.to = to
        self.captured = captured
        self.castling = castling
        self.en_passant = en_passant # Possible castling to promotion?
        self.promotion = promotion # Promotion is the piece object that was promoted to
        self.check = check
        self.checkmate = checkmate
    
    def __str__(self):
        return self.notation()

    def notation(self):
        """
        Gets a algebraic notation for the move.
        https://www.chess.com/article/view/chess-notation#algebraic-notation
        """
        if self.castling:
            return "O-O-O" # Edit later for other side
        
        if self.piece.name.lower() != "p":
            notation = self.piece.name
        notation += str(self.from_square)
        if self.captured_piece:
            notation += "x"
        notation += str(self.to_square)
        if self.promotion:
            notation += "=" + self.promotion.name
        if self.checkmate:
            notation += "#"
        elif self.check:
            notation += "+"
        return notation

class ChessBoard:
    def __init__(self, 
                 x:int, y:int, 
                 size: int, 
                 starting_configuration:list[list[str]],
                 included_pieces:dict[str, dict], # dict of piece name to attributes
                 turn:str = "white",
                 perspective:str = "white",
                 dark: _pygame.Color = BROWN,
                 light: _pygame.Color = BEIGE,
                 theme: int = 1,
                 move_sound: _pygame.mixer.Sound = MOVE_SOUND,
                 capture_sound: _pygame.mixer.Sound = CAPTURE_SOUND,
                 promotion_sound: _pygame.mixer.Sound = PROMOTE_SOUND): 
        self.position:list[list[Piece]] = self.position_pieces(included_pieces, starting_configuration, theme) # Rows and columns of pieces
        self.turn = turn
        self.dark = dark
        self.light = light
        self.size = size / 8
        self.move_sound = move_sound
        self.capture_sound = capture_sound
        self.promotion_sound = promotion_sound
        self.perspective = perspective
        self.ranks_locations, self.files_locations = self.calculate_locations(x, y, self.size, perspective)
        self.selected_square = None
        self.moves_stack = []
        # self.en_passant_square = None # This is the square where the en-passant can be done
    
    # @staticmethod
    # def simulate_move(current_position:list[list[Piece]], piece:Piece|BoardLocation, move_to:BoardLocation):
    #     return current_position

    @staticmethod
    def position_pieces(included_pieces:dict[str, dict], starting_configuration:list[list[str]], theme:int):
        # Make sure included pieces has all the pieces in lowercase keys
        position = [[None for _ in range(8)] for _ in range(8)]
        for rank in range(8):
            for file in range(8):
                piece_name = starting_configuration[rank][file]
                if piece_name is None:
                    position[rank][file] = None
                else:
                    position[rank][file] = Piece(**included_pieces[piece_name.lower()], 
                                                name=piece_name, 
                                                square=BoardLocation(rank, file), 
                                                colour="white" if piece_name.isupper() else "black",
                                                direction=1 if piece_name.isupper() else -1,
                                                theme=theme)
        return position
    
    @staticmethod
    def calculate_locations(x:int, y:int, size:int, perspective:str):
        ranks = [int(x + j * size + size / 2) for j in range(8)]
        files = [int(y + i * size + size / 2) for i in range(8)]

        if perspective == "white":
            files.reverse()
        if perspective == "black":
            ranks.reverse()
        return ranks, files
    
    def square_to_coordinates(self, square:BoardLocation):
        return (self.ranks_locations[square.file], self.files_locations[square.rank])

    def coordinates_to_square(self, coordinates: tuple[int, int]) -> BoardLocation:
        x, y = coordinates
        half_size = self.size / 2
        file = next(
            (f for f in range(8) if self.ranks_locations[f] - half_size <= x < self.ranks_locations[f] + half_size), None)
        rank = next(
            (r for r in range(8) if self.files_locations[r] - half_size <= y < self.files_locations[r] + half_size), None)
        return BoardLocation(rank, file) if rank is not None and file is not None else None

    def get_piece_at_square(self, square:BoardLocation):
        return self.position[square.rank][square.file]
    
    # def attacking(self, square:BoardLocation): # Returns a list of pieces that are attacking the square
    #     flattened_position = [piece for row in self.position for piece in row if piece is not None]
    #     attacking_pieces = []
    #     for piece in flattened_position:
    #         for legal_move in piece.legal_moves:
    #             if legal_move.type == "capture" and legal_move.to == square:
    #                 attacking_pieces.append(piece)
    #     return attacking_pieces

    def get_position(self):
        """
        Gets the position (as in chess position) of the board and returns it as a 2d list of piece names.
        Each piece is represented by its name, or None if there is no piece on that square
        """
        position_list = [[None for _ in range(8)] for _ in range(8)]
        for rank in range(8):
            for file in range(8):
                if self.position[rank][file] == None:
                    position_list[rank][file] = None
                else:
                    position_list[rank][file] = self.position[rank][file].name
        return position_list

    def get_fen(self, copy_to_clipboard:bool=False) -> str:
        """
        Returns the FEN representation of the board
        Field 1: Pieces locations
        Field 2: Active colour
        Field 3: Castling rights
        Field 4: En passant target square
        Field 5: Halfmove clock
        Field 6: Fullmove number
        https://www.chess.com/terms/fen-chess#what-is-fen

        To copy for chess.com do f'[FEN {fen_string}]'
        """
        position_list = self.get_position()[::-1]
        fen_string = ""
        # get these things
        castling_rights = ["K", "Q", "k", "q"]
        en_passant_target = "-"
        halfmove_clock = 0
        fullmove_number = 0

        # Pieces Locations
        for rank in position_list:
            empty_spaces = 0
            for square in rank:
                if square is None:
                    empty_spaces += 1
                else:
                    if empty_spaces > 0:
                        fen_string += str(empty_spaces)
                        empty_spaces = 0
                    fen_string += square
            if empty_spaces > 0:
                fen_string += str(empty_spaces)
            fen_string += "/"
        # Active Colour
        fen_string += " " + self.turn[0]
        # Castling rights
        fen_string += " " + ("".join(castling_rights) if len(castling_rights) > 0 else "-")
        # En passant target square
        fen_string += " " + (en_passant_target if en_passant_target is not None else "-")
        # Halfmove clock
        fen_string += " " + str(halfmove_clock)
        # Fullmove number
        fen_string += " " + str(fullmove_number)
        if copy_to_clipboard:
            r = tk.Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(f"[FEN {fen_string}]")
            r.update() # now it stays on the clipboard after the window is closed
            r.destroy()
            print(f"Copied FEN to clipboard: {fen_string}") # Change to alert later CHANGE THIS LATER
        return fen_string
    
    def log_move(self, piece: Piece, at: BoardLocation, to: BoardLocation, captured: Piece = None):
        self.moves_stack.append(Move(piece, at, to, captured))

    def pop(self, amount_of_moves: int):
        for _ in range(amount_of_moves):
            if not self.moves_stack:
                break
            last_move: Move = self.moves_stack.pop()
            self.turn = "white" if self.turn == "black" else "black"

            moved_piece = self.get_piece_at_square(last_move.to)
            self.position[last_move.to.rank][last_move.to.file] = None
            self.position[last_move.at.rank][last_move.at.file] = moved_piece
            if last_move.captured:
                self.position[last_move.to.rank][last_move.to.file] = last_move.captured
            moved_piece.unmove()

    def move(self, at: BoardLocation, to: BoardLocation):
        piece = self.get_piece_at_square(at)
        if piece:
            if not piece.colour == self.turn:
                return False
            for move in piece.legal_moves:
                if move.to == to:
                    captured = None
                    if "capture" in move.type:
                        captured = self.get_piece_at_square(to)
                        self.position[to.rank][to.file] = None

                    self.position[at.rank][at.file] = None
                    piece.move(to)
                    self.position[to.rank][to.file] = piece

                    if "promotion" in move.type:
                        piece.promote()
                        self.promotion_sound.play()
                    elif "capture" in move.type:
                        self.capture_sound.play()
                    else:
                        self.move_sound.play()

                    self.log_move(piece, at, to, captured)
                    self.turn = "black" if self.turn == "white" else "white"
                    return True
        return False

    def handle_click(self, mouse_pos: tuple[int, int]):
        clicked_square = self.coordinates_to_square(mouse_pos)
        if clicked_square is None: # Click was outside the board
            self.selected_square = None
            return
        clicked_piece = self.get_piece_at_square(clicked_square)
        if clicked_piece: # Case 1: Clicked on a piece
            if self.selected_square == clicked_square: # Deselect if clicking the same piece
                self.selected_square = None
            elif self.selected_square: # A piece is selected
                if clicked_piece.colour == self.turn: # Select a new same team piece
                    self.selected_square = clicked_square
                else: # Try to move to opponent's square (capture)
                    if not self.move(self.selected_square, clicked_square):
                        self.selected_square = clicked_square
            else: # Nothing selected yet, select this piece
                self.selected_square = clicked_square
        else: # Case 2: Clicked on empty square
            if self.selected_square:
                if not self.move(self.selected_square, clicked_square):
                    self.selected_square = None

    def update(self):
        flattened_position = [piece for row in self.position for piece in row if piece is not None]
        white_pieces_locations = [p.square for p in flattened_position if p.colour == "white"]
        black_pieces_locations = [p.square for p in flattened_position if p.colour == "black"]
        for piece in flattened_position:
            if piece.colour == "white":
                piece.update(black_pieces_locations, white_pieces_locations)
            else:
                piece.update(white_pieces_locations, black_pieces_locations)
        for piece in flattened_position:
            piece.selected = False
        if self.selected_square is not None:
            piece = self.get_piece_at_square(self.selected_square)
            if piece:
                piece.selected = True
    
    def draw(self, screen:_pygame.Surface, show_coordinates:bool = True):
        # draw the board
        for rank in range(8):
            for file in range(8):
                if (rank + file) % 2 == 0:
                    color = self.light
                else:
                    color = self.dark
                if self.selected_square is not None:

                    if self.selected_square == BoardLocation(file, rank):
                        color = HIGHLIGHT
                _pygame.draw.rect(screen, color, (self.ranks_locations[rank] - self.size / 2, self.files_locations[file] - self.size / 2, self.size + 1, self.size + 1))

                # draw the chess coordinates
                if show_coordinates:
                    font = _pygame.font.SysFont("Mono", 20)
                    if self.perspective == "white":
                        coordinate_rank, coordinate_file = 0, 0
                    else:
                        coordinate_rank, coordinate_file = 7, 7
                    if rank == coordinate_rank:
                        text = font.render(str(file + 1), True, self.dark if (rank + file) % 2 == 0 else self.light)
                        screen.blit(text, (self.ranks_locations[rank] - self.size / 2, self.files_locations[file] - self.size / 2))
                    if file == coordinate_file:
                        text = font.render(chr(rank + 65), True, self.dark if (rank + file) % 2 == 0 else self.light)
                        screen.blit(text, (self.ranks_locations[rank] + self.size / 2 - text.get_width(), self.files_locations[file] + self.size / 2 - text.get_height()))
        
        # draw the pieces and the legal moves of the selected piece
        flattened_position = [piece for row in self.position for piece in row if piece is not None]
        for piece in flattened_position:
            piece.draw(screen, self.ranks_locations, self.files_locations, self.turn)
        
        # Print Turn
        font = _pygame.font.SysFont("Mono", 25)
        text = font.render(f"Turn: {self.turn}", True, RED)
        screen.blit(text, (10, 10))

        # Debugging information
        if show_debug_info:
            mouse_pos = _pygame.mouse.get_pos()
            font = _pygame.font.SysFont("Mono", 15)
            text = font.render(f"{self.coordinates_to_square(mouse_pos)}", True, RED)
            screen.blit(text, (10, 35))
            text = font.render(f"{mouse_pos[0]}, {mouse_pos[1]}", True, RED)
            screen.blit(text, (10, 50))

            if self.selected_square is not None:
                text = font.render(f"Selected: {self.selected_square}", True, RED)
                screen.blit(text, (10, 65))
                piece = self.get_piece_at_square(self.selected_square)
                if piece:
                    text = font.render(f"Piece: {piece.square}", True, RED)
                    screen.blit(text, (10, 80))
                    text = font.render(f"Legal:", True, RED)
                    screen.blit(text, (10, 95))
                    for i in range(len(piece.legal_moves)):
                        text = font.render(f"{i + 1}: {piece.legal_moves[i].to}, {piece.legal_moves[i].type}", True, RED)
                        screen.blit(text, (10, 110 + i * 15))

def initialize_classic_game(x, y, size = BOARD_SIZE, starting_configuration = BOARD_NAME_CONFIG, theme = 1, play_start_sound = GAME_START_SOUND):
    play_start_sound.play()
    chessboard = ChessBoard(
        x=x,
        y=y,
        size=size,
        starting_configuration=starting_configuration,
        included_pieces={
            "p": {
                "pattern": ClassicPiecesMovement.pawn_movement,
                "attributes": {"can_double_move": True, "can_en_passant": True, "can_promotion": True},
            },
            "r": {"pattern": ClassicPiecesMovement.rook_movement},
            "n": {"pattern": ClassicPiecesMovement.knight_movement},
            "b": {"pattern": ClassicPiecesMovement.bishop_movement},
            "q": {"pattern": ClassicPiecesMovement.queen_movement},
            "k": {"pattern": ClassicPiecesMovement.king_movement},
        },
        theme=theme
    )
    return chessboard