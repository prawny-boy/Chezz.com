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
HIGHLIGHT_RADIUS = 7.5
PIECE_SIZE = 50
BOARD_SIZE = 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = _pygame.Color('#b58863')
BEIGE = _pygame.Color('#f0d9b5')
HIGHLIGHT = _pygame.Color('#8877DD99')
MOVE_HIGHLIGHT = _pygame.Color('#5fa14460')
CAPTURE_HIGHLIGHT = _pygame.Color('#d42a2a60')

BOARD_CONFIG = [
    ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r']
]

# CLASSES
class BoardLocation:
    def __init__(self, rank:int, file:int):
        self.rank = rank
        self.file = file
    
    def offset(self, offset_rank:int, offset_file:int):
        self.rank += offset_rank

        self.file += offset_file
        return self
    
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

class MovementPattern:
    def __init__(self, name:str, movement:list[Move]):
        self.name = name
        self.movement = movement # list of tuples (x, y) of what to add to the current position (0, 0)
        self.current_moves = movement
        self.current_position = BoardLocation(0, 0)
    
    def update_to_position(self, location:BoardLocation): # this does not check for board limits or pieces in the way
        offset_rank = location.get_rank() - self.current_position.get_rank()
        offset_file = location.get_file() - self.current_position.get_file()
        for i in range(len(self.current_moves)):
            self.current_moves[i].offset(offset_rank, offset_file)
        self.current_position = location

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
                 movement:MovementPattern, 
                 square:BoardLocation, 
                 sprite:_pygame.Surface, 
                 worth:int,
                 special:str = None):
        self.name = name
        if sprite is None:
            sprite = self.create_placeholder_piece(BLACK if name.islower() else WHITE, name)
        else:
            sprite = _pygame.transform.scale(sprite, (PIECE_SIZE, PIECE_SIZE))
        self.sprite = sprite
        self.square = square
        self.worth = worth
        self.legal_moves = []
        self.movement = movement
        self.special = special # "normal", "king" can move into check,"jump" means ignore pieces in the way
    
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
        self.movement.update_to_position(self.square)
        # Update the legal moves of a piece
        self.legal_moves = []
        for move in self.movement.current_moves:
            if move.move.get_rank() >= 0 and move.move.get_rank() < 8 and move.move.get_file() >= 0 and move.move.get_file() < 8: # check if the move is within the board limits
                if move.type == "normal": # check if the move is not blocked by other pieces
                    self.legal_moves.append(move)
                elif move.type == "capture": # check if the move is onto a piece
                    for piece_location in all_pieces_locations:
                        if piece_location.get_rank() == move.move.get_rank() and piece_location.get_file() == move.move.get_file():
                            self.legal_moves.append(move)
                            break
                elif move.type == "jump": # this is if the piece can jump over other pieces
                    self.legal_moves.append(move)

    def move_to(self, new_square:BoardLocation):
        self.square = new_square
    
    def draw(self, screen:_pygame.Surface, coordinates:tuple[int, int]):
        self.sprite = _pygame.transform.scale(self.sprite, (PIECE_SIZE, PIECE_SIZE))
        screen.blit(self.sprite, (coordinates[0] - PIECE_SIZE / 2, coordinates[1] - PIECE_SIZE / 2))
        
    def draw_legal_moves(self, screen, coordinates:tuple[int, int]):
        pass

class ChessBoard:
    def __init__(self, 
                 x:int, y:int, 
                 size: int, 
                 screen:_pygame.Surface,
                 starting_configuration:list[list[str]] = BOARD_CONFIG,
                 pieces:dict[str, dict] = None,
                 dark: _pygame.Color = BROWN,
                 light: _pygame.Color = BEIGE): 
        self.x = x
        self.y = y
        self.size = size / 8
        self.all_pieces:list[Piece] = self.make_pieces(pieces, starting_configuration)
        self.dark = dark
        self.light = light
        self.ranks_locations, self.files_locations = self.calculate_positions()
        self.selected_square = None
    
    def calculate_positions(self):
        files = [int(self.y + (7 - i) * self.size + self.size / 2) for i in range(7, -1, -1)]
        ranks = [int(self.x + j * self.size + self.size / 2) for j in range(8)]
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

    def coordinates_to_square(self, coordinates:tuple[int, int]):
        return BoardLocation(self.ranks_locations.index(coordinates[0]), self.files_locations.index(coordinates[1]))

    def get_position(self):
        # Gets the position (as in chess position) of the board and returns it as how starting_configuration is
        pass

    def update(self):
        # update the pieces
        for piece in self.all_pieces:
            piece.update([piece.square for piece in self.all_pieces]) # get all the pieces locations
        # update selected square
        
    def draw(self, screen, perspective:str = "white", show_coordinates:bool = True):
        # draw the board
        for rank in range(8):
            for file in range(8):
                if perspective == "white":
                    rank, file = 7 - rank, 7 - file
                if (rank + file) % 2 == 0:
                    color = self.light
                else:
                    color = self.dark
                _pygame.draw.rect(screen, color, (self.x + rank * self.size, self.y + file * self.size, self.size + 1, self.size + 1))

                # draw the chess coordinates
                if show_coordinates:
                    font = _pygame.font.SysFont("Mono", 20)
                    if rank == 0:
                        text = font.render(str(file + 1), True, self.dark if (rank + file) % 2 == 0 else self.light)
                        screen.blit(text, (self.x + rank * self.size, self.y + file * self.size))
                    if file == 7:
                        text = font.render(chr(rank + 65), True, self.dark if (rank + file) % 2 == 0 else self.light)
                        screen.blit(text, (self.x + rank * self.size + self.size - text.size[0], self.y + file * self.size + self.size - text.size[1]))
        
        # draw the pieces
        for piece in self.all_pieces:
            if perspective == "white":
                coordinates = self.square_to_coordinates(BoardLocation(7 - piece.square.get_rank(), 7 - piece.square.get_file()))
            else:
                coordinates = self.square_to_coordinates(piece.square)
            piece.draw(screen, coordinates)

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
                                'p': {'movement': ClassicPiecesMovement.pawn_movement, 'sprite': None, 'worth': 1},
                                'r': {'movement': ClassicPiecesMovement.rook_movement, 'sprite': None, 'worth': 5},
                                'n': {'movement': ClassicPiecesMovement.knight_movement, 'sprite': None, 'worth': 3},
                                'b': {'movement': ClassicPiecesMovement.bishop_movement, 'sprite': None, 'worth': 3},
                                'q': {'movement': ClassicPiecesMovement.queen_movement, 'sprite': None, 'worth': 9},
                                'k': {'movement': ClassicPiecesMovement.king_movement, 'sprite': None, 'worth': 0}
                            })
    
    while True:
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                _pygame.quit()
                _exit()
            
            if event.type == _pygame.MOUSEBUTTONDOWN:
                mouse_pos = _pygame.mouse.get_pos()
        
        # Updates
        chessboard.update()

        # Drawing the screen
        screen.fill(BLACK)
        chessboard.draw(screen)
        
        _pygame.display.flip()
        clock.tick(FRAME_RATE)