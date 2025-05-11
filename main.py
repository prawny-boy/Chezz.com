import pygame as _pygame
from sys import exit as _exit

_pygame.init()
_pygame.font.init()
_pygame.mixer.init()

# ASSETS
# Sounds
# click_sound = _pygame.mixer.Sound("Assets/Sounds/click.wav")
# move_sound = _pygame.mixer.Sound("Assets/Sounds/move.wav")
# Sprites
logo = _pygame.image.load("Assets/Sprites/logo.png")
icon = _pygame.image.load("Assets/Sprites/icon.png")
company_logo = _pygame.image.load("Assets/Sprites/company.png")

# CONSTANTS
FRAME_RATE = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVE_HIGHLIGHT_RADIUS = 7.5
CAPTURE_HIGHLIGHT_RADIUS = 30
CAPTURE_HIGHLIGHT_WIDTH = 3
PIECE_SIZE = 50
BOARD_SIZE = 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = _pygame.Color('#b58863')
BEIGE = _pygame.Color('#f0d9b5')
HIGHLIGHT = _pygame.Color('#8877DD99')
MOVE_HIGHLIGHT = _pygame.Color('#5fa14460')
CAPTURE_HIGHLIGHT = _pygame.Color('#d42a2a60')

BOARD_CONFIG = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', None, 'P', 'P', 'P', 'P'], 
    [None, None, None, 'P', None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
]

# CLASSES
class BoardLocation:
    def __init__(self, rank:int, file:int):
        self.rank = rank
        self.file = file
    
    def __str__(self):
        if self.rank < 0 or self.rank > 7 or self.file < 0 or self.file > 7:
            return "None"
        else:
            return f"{["a", "b", "c", "d", "e", "f", "g", "h"][self.file]}{self.rank + 1}"
    
    def offset(self, offset_rank:int, offset_file:int):
        self.rank += offset_rank
        self.file += offset_file
    
    def get_rank(self):
        return self.rank
    
    def get_file(self):
        return self.file

class Move():
    def __init__(self, move:BoardLocation, need_to_be_clear:list[BoardLocation], type:str):
        self.move = move
        self.need_to_be_clear = need_to_be_clear
        self.type = type # "normal", "capture"
    
    def offset(self, offset_rank:int, offset_file:int):
        self.move.offset(offset_rank, offset_file)
        new_clear_spaces = []
        for clear_space in self.need_to_be_clear:
            clear_space.offset(offset_rank, offset_file)
            new_clear_spaces.append(clear_space)
        self.need_to_be_clear = new_clear_spaces
    
    def get_move(self):
        return self.move

class MovementPattern:
    def __init__(self, name:str, pattern:list[Move]):
        self.name = name
        self.pattern = pattern # list of tuples (x, y) of what to add to the position (0, 0)
    
    def update_to_position(self, location: BoardLocation, direction: int) -> list[Move]:
        rank_offset = location.get_rank()
        file_offset = location.get_file()

        new_pattern = []
        for move in self.pattern:
            # Offset the main move location
            original_move = move.move
            new_move_location = BoardLocation(
                original_move.get_rank() + rank_offset,
                original_move.get_file() + file_offset
            )

            # Offset all the need_to_be_clear locations
            new_clear_spaces = [
                BoardLocation(cs.get_rank() + rank_offset, cs.get_file() + file_offset)
                for cs in move.need_to_be_clear
            ]

            # Create a new Move with the updated values
            new_move = Move(new_move_location, new_clear_spaces, move.type)
            new_pattern.append(new_move)

        return new_pattern

class ClassicPiecesMovement:
    pawn_movement = MovementPattern("pawn", [Move(BoardLocation(1, 0), [], "normal"),
                                            Move(BoardLocation(2, 0), [], "normal"),
                                            Move(BoardLocation(1, 1), [], "capture"),
                                            Move(BoardLocation(1, -1), [], "capture")])
    knight_movement = MovementPattern("knight", [Move(BoardLocation(2, 1), [], "jump"),
                                                Move(BoardLocation(2, -1), [], "jump"),
                                                Move(BoardLocation(-2, 1), [], "jump"),
                                                Move(BoardLocation(-2, -1), [], "jump"),
                                                Move(BoardLocation(1, 2), [], "jump"),
                                                Move(BoardLocation(1, -2), [], "jump"),
                                                Move(BoardLocation(-1, 2), [], "jump"),
                                                Move(BoardLocation(-1, -2), [], "jump")])
    bishop_movement = MovementPattern("bishop", [Move(BoardLocation(1, 1), [], "normal"),
                                                Move(BoardLocation(1, -1), [], "normal"),
                                                Move(BoardLocation(-1, 1), [], "normal"),
                                                Move(BoardLocation(-1, -1), [], "normal")])
    rook_movement = MovementPattern("rook", [Move(BoardLocation(1, 0), [], "normal"),
                                            Move(BoardLocation(-1, 0), [], "normal"),
                                            Move(BoardLocation(0, 1), [], "normal"),
                                            Move(BoardLocation(0, -1), [], "normal")])
    queen_movement = MovementPattern("queen", [Move(BoardLocation(1, 0), [], "normal"),
                                             Move(BoardLocation(-1, 0), [], "normal"),
                                             Move(BoardLocation(0, 1), [], "normal"),
                                             Move(BoardLocation(0, -1), [], "normal"),
                                             Move(BoardLocation(1, 1), [], "normal"),
                                             Move(BoardLocation(1, -1), [], "normal"),
                                             Move(BoardLocation(-1, 1), [], "normal"),
                                             Move(BoardLocation(-1, -1), [], "normal")])
    king_movement = MovementPattern("king", [Move(BoardLocation(1, 0), [], "normal"),
                                            Move(BoardLocation(-1, 0), [], "normal"),
                                            Move(BoardLocation(0, 1), [], "normal"),
                                            Move(BoardLocation(0, -1), [], "normal"),
                                            Move(BoardLocation(1, 1), [], "normal"),
                                            Move(BoardLocation(1, -1), [], "normal"),
                                            Move(BoardLocation(-1, 1), [], "normal"),
                                            Move(BoardLocation(-1, -1), [], "normal")])

class Piece:
    def __init__(self, 
                 name:str,
                 pattern:MovementPattern, 
                 square:BoardLocation, 
                 sprite:_pygame.Surface, 
                 worth:int,
                 direction:int = 1,
                 special:str = None):
        self.name = name
        if sprite is None:
            sprite = self.create_placeholder_piece(BLACK if name.islower() else WHITE, name)
        else:
            sprite = _pygame.transform.scale(sprite, (PIECE_SIZE, PIECE_SIZE))
        self.sprite = sprite
        self.square = square
        self.worth = worth
        self.legal_moves:list[Move] = []
        self.pattern = pattern
        self.movement = pattern.update_to_position(square, direction)
        self.direction = direction # 1 for white, -1 for black
        self.special = special # "normal", "king" can move into check,"jump" means ignore pieces in the way, "pawn" means can capture en passant, promotion and 2 squares first move
        self.selected = False
    
    def create_placeholder_piece(self, color:_pygame.Color, piece_char:str):
        surf = _pygame.Surface((50, 50), _pygame.SRCALPHA)
        color_rgb = color
        _pygame.draw.circle(surf, color_rgb, (25, 25), 20)
        font = _pygame.font.SysFont("Arial", 24, bold=True)
        text = font.render(piece_char.upper(), True, BLACK if color == WHITE else WHITE)
        text_rect = text.get_rect(center=(25, 25))
        surf.blit(text, text_rect)
        return surf

    def update(self, all_pieces_locations:list[BoardLocation]):
        # Update the position of the piece for the movement pattern
        self.movement = self.pattern.update_to_position(self.square, self.direction)
        # Update the legal moves of a piece
        self.legal_moves = []
        for move in self.movement:
            if move.move.get_rank() >= 0 and move.move.get_rank() < 8 and move.move.get_file() >= 0 and move.move.get_file() < 8: # check if the move is within the board limits
                if move.type == "normal": # check if the move is not blocked by other pieces
                    for piece_location in all_pieces_locations:
                        if piece_location.get_rank() == move.move.get_rank() and piece_location.get_file() == move.move.get_file():
                            break
                    else: # this means that the move is not blocked by other pieces
                        self.legal_moves.append(move)
                elif move.type == "capture": # check if the move is onto a piece
                    for piece_location in all_pieces_locations:
                        if piece_location.get_rank() == move.move.get_rank() and piece_location.get_file() == move.move.get_file():
                            self.legal_moves.append(move)
                            break
                elif move.type == "jump": # this is if the piece can jump over other pieces
                    self.legal_moves.append(move)
        if self.selected == True:
            print([str(move.move) for move in self.legal_moves])

    def move_to(self, new_square:BoardLocation):
        self.square = new_square
    
    def draw_legal_moves(self, screen:_pygame.Surface, ranks_locations:list[int], files_locations:list[int]):
        for move in self.legal_moves:
            if move.type == "normal":
                _pygame.draw.circle(screen, MOVE_HIGHLIGHT, (ranks_locations[move.move.get_file()], files_locations[move.move.get_rank()]), MOVE_HIGHLIGHT_RADIUS)
            elif move.type == "capture":
                _pygame.draw.circle(screen, CAPTURE_HIGHLIGHT, (ranks_locations[move.move.get_file()], files_locations[move.move.get_rank()]), CAPTURE_HIGHLIGHT_RADIUS, CAPTURE_HIGHLIGHT_WIDTH)
    
    def draw(self, screen:_pygame.Surface, ranks_locations:list[int], files_locations:list[int]):
        self.sprite = _pygame.transform.scale(self.sprite, (PIECE_SIZE, PIECE_SIZE))
        screen.blit(self.sprite, (ranks_locations[self.square.get_file()] - PIECE_SIZE / 2, files_locations[self.square.get_rank()] - PIECE_SIZE / 2))
        if self.selected:
            _pygame.draw.circle(screen, HIGHLIGHT, (ranks_locations[self.square.get_file()], files_locations[self.square.get_rank()]), MOVE_HIGHLIGHT_RADIUS)
            self.draw_legal_moves(screen, ranks_locations, files_locations)

class ChessBoard:
    def __init__(self, 
                 x:int, y:int, 
                 size: int, 
                 screen:_pygame.Surface,
                 starting_configuration:list[list[str]] = BOARD_CONFIG,
                 pieces:dict[str, dict] = None,
                 perspective:str = "white",
                 dark: _pygame.Color = BROWN,
                 light: _pygame.Color = BEIGE): 
        self.x = x
        self.y = y
        self.size = size / 8
        self.all_pieces:list[Piece] = self.make_pieces(pieces, starting_configuration)
        self.dark = dark
        self.light = light
        self.perspective = perspective
        self.ranks_locations, self.files_locations = self.calculate_positions()
        self.selected_square = None
    
    def calculate_positions(self):
        ranks = [int(self.x + j * self.size + self.size / 2) for j in range(8)]
        files = [int(self.y + i * self.size + self.size / 2) for i in range(8)]

        if self.perspective == "white":
            files.reverse()
        if self.perspective == "black":
            ranks.reverse()
        print(ranks, files)
        return ranks, files

    def make_pieces(self, pieces_dict:dict[str, dict], starting_configuration:list[list[str]]):
        for piece_name in pieces_dict.keys():
            if not piece_name.lower() == piece_name:
                pieces_dict[piece_name.lower()] = pieces_dict.pop(piece_name) # Change the key to lowercase

        pieces = []
        for rank in range(8):
            for file in range(8):
                piece_name = starting_configuration[rank][file]
                if piece_name is not None:
                    pieces.append(Piece(**pieces_dict[piece_name.lower()], name=piece_name, square=BoardLocation(rank, file)))
                    print(f"Piece {piece_name} created at {rank}, {file}")
            
        return pieces
    
    def square_to_coordinates(self, square:BoardLocation):
        return (self.ranks_locations[square.get_file()], self.files_locations[square.get_rank()])

    def coordinates_to_square(self, coordinates: tuple[int, int]) -> BoardLocation:
        x, y = coordinates

        # Find closest file and rank using ranges instead of exact indexing
        file = next((f for f in range(8) if self.ranks_locations[f] - self.size / 2 <= x < self.ranks_locations[f] + self.size / 2), None)
        rank = next((r for r in range(8) if self.files_locations[r] - self.size / 2 <= y < self.files_locations[r] + self.size / 2), None)

        return BoardLocation(rank, file) if rank is not None and file is not None else None

    def get_position(self):
        # Gets the position (as in chess position) of the board and returns it as how starting_configuration is
        pass

    def handle_click(self, mouse_pos:tuple[int, int]):
        self.selected_square = self.coordinates_to_square(mouse_pos)
        print(f"selected square: {str(self.selected_square)}")

    def update(self):
        # update the pieces
        for piece in range(len(self.all_pieces)):
            self.all_pieces[piece].update([piece.square for piece in self.all_pieces]) # get all the pieces locations

        # update selected square
        if self.selected_square is not None:
            for piece in range(len(self.all_pieces)):
                if self.all_pieces[piece].square.get_rank() == self.selected_square.get_rank() and self.all_pieces[piece].square.get_file() == self.selected_square.get_file():
                    self.all_pieces[piece].selected = True
                else:
                    self.all_pieces[piece].selected = False
        else:
            for piece in range(len(self.all_pieces)):
                self.all_pieces[piece].selected = False
    
    def draw(self, screen:_pygame.Surface, show_coordinates:bool = True):
        # draw the board
        for rank in range(8):
            for file in range(8):
                if (rank + file) % 2 == 0:
                    color = self.light
                else:
                    color = self.dark
                if self.selected_square is not None:

                    if self.selected_square.get_rank() == file and self.selected_square.get_file() == rank:
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
        for piece in self.all_pieces:
            coordinates = self.square_to_coordinates(piece.square)
            piece.draw(screen, self.ranks_locations, self.files_locations)
        
        # Debugging information
        mouse_pos = _pygame.mouse.get_pos()
        font = _pygame.font.SysFont("Mono", 15)
        text = font.render(f"{chessboard.coordinates_to_square(mouse_pos)}", True, RED)
        screen.blit(text, (10, 10))

        if self.selected_square is not None:
            text = font.render(f"Selected: {self.selected_square}", True, RED)
            screen.blit(text, (10, 30))
            for piece in self.all_pieces:
                if piece.square.get_rank() == self.selected_square.get_rank() and piece.square.get_file() == self.selected_square.get_file():
                    text = font.render(f"Piece: {piece.square}", True, RED)
                    screen.blit(text, (10, 50))
                    text = font.render(f"Movement: {[str(i.move) for i in piece.movement]}", True, RED)
                    screen.blit(text, (10, 70))
                    text = font.render(f"Legal: {[str(i.move) for i in piece.legal_moves]}", True, RED)
                    screen.blit(text, (10, 90))
                    break

# FUNCTIONS
# def load_piece_sprites():
#     pieces = {}
#     piece_types = {
#         'p': chess.PAWN,
#         'n': chess.KNIGHT,
#         'b': chess.BISHOP,
#         'r': chess.ROOK,
#         'q': chess.QUEEN,
#         'k': chess.KING
#     }
    
#     try:
#         for color in ['w', 'b']:
#             for piece_char, piece_type in piece_types.items():
#                 filename = f"Assets/Sprites/{color}{piece_char}.png"
#                 if os.path.exists(filename): 
#                     pieces[(chess.WHITE if color == 'w' else chess.BLACK, piece_type)] = pygame.image.load(filename)
#                 else:
#                     pieces[(chess.WHITE if color == 'w' else chess.BLACK, piece_type)] = create_placeholder_piece(color, piece_char)
#     except:
#         for color in [chess.WHITE, chess.BLACK]:
#             for piece_type in piece_types.values():
#                 pieces[(color, piece_type)] = create_placeholder_piece(
#                     'w' if color == chess.WHITE else 'b',
#                     next(k for k, v in piece_types.items() if v == piece_type)
#                 )
    
#     return pieces

def splash_screen(icons_to_show:list[_pygame.Surface]):
    alpha = 0
    dir = "+"
    icon_idx = 0
    for icon in icons_to_show:
        icons_to_show[icons_to_show.index(icon)] = _pygame.transform.scale(icon, (200, 200))
    icon = icons_to_show[icon_idx]
    while True:
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                _pygame.quit()
                exit()
            if event.type == _pygame.MOUSEBUTTONDOWN:
                dir = "-"
        
        if dir == "+":
            alpha += 2
            if alpha == 300:
                dir = "-"
        else:
            alpha -= 2
            if alpha == 0:
                icon_idx += 1
                try:
                    icon = icons_to_show[icon_idx]
                except IndexError:
                    screen.fill((0, 0, 0))
                    return
                dir = "+"
        
        screen.fill((0, 0, 0))
        icon.set_alpha(alpha)
        screen.blit(icon, (SCREEN_WIDTH / 2 - icon.get_width() / 2, SCREEN_HEIGHT / 2 - icon.get_height() / 2))
        _pygame.display.flip()
        clock.tick(FRAME_RATE)

screen = _pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
_pygame.display.set_caption("Chezz.com")
_pygame.display.set_icon(icon)
clock = _pygame.time.Clock()

if __name__ == "__main__":
    # splash_screen([company_logo, logo])

    # Create Chess Board and Pieces
    chessboard = ChessBoard(SCREEN_WIDTH / 2 - BOARD_SIZE / 2, SCREEN_HEIGHT / 2 - BOARD_SIZE / 2, BOARD_SIZE, BOARD_CONFIG, 
                            pieces={
                                'p': {'pattern': ClassicPiecesMovement.pawn_movement, 'sprite': None, 'worth': 1},
                                'r': {'pattern': ClassicPiecesMovement.rook_movement, 'sprite': None, 'worth': 5},
                                'n': {'pattern': ClassicPiecesMovement.knight_movement, 'sprite': None, 'worth': 3},
                                'b': {'pattern': ClassicPiecesMovement.bishop_movement, 'sprite': None, 'worth': 3},
                                'q': {'pattern': ClassicPiecesMovement.queen_movement, 'sprite': None, 'worth': 9},
                                'k': {'pattern': ClassicPiecesMovement.king_movement, 'sprite': None, 'worth': 0}
                            },
                            perspective="black")
    
    while True:
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                _pygame.quit()
                _exit()
            
            if event.type == _pygame.MOUSEBUTTONDOWN:
                mouse_pos = _pygame.mouse.get_pos()
                chessboard.handle_click(mouse_pos)

        # Updates
        chessboard.update()

        # Drawing the screen
        screen.fill(BLACK)
        chessboard.draw(screen)
        
        _pygame.display.flip()
        clock.tick(FRAME_RATE)