import pygame
import chess
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

logo = pygame.image.load("Assets/Sprites/logo.png")
icon = pygame.image.load("Assets/Sprites/icon.png")
company_logo = pygame.image.load("Assets/Sprites/company.png")

FRAME_RATE = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
HIGHLIGHT_RADIUS = 7.5
PIECE_SIZE = 50
BOARD_SIZE = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = pygame.Color('#b58863')
BEIGE = pygame.Color('#f0d9b5')
HIGHLIGHT = pygame.Color('#8877DD99')
MOVE_HIGHLIGHT = pygame.Color('#5fa14460')
CAPTURE_HIGHLIGHT = pygame.Color('#d42a2a60')

BOARD_CONFIG = [
    ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'], 
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
    ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R']
]

# FUNCTIONS
def load_piece_sprites():
    pieces = {}
    piece_types = {
        'p': chess.PAWN,
        'n': chess.KNIGHT,
        'b': chess.BISHOP,
        'r': chess.ROOK,
        'q': chess.QUEEN,
        'k': chess.KING
    }
    
    try:
        for color in ['w', 'b']:
            for piece_char, piece_type in piece_types.items():
                filename = f"Assets/Sprites/{color}{piece_char}.png"
                if os.path.exists(filename):
                    pieces[(chess.WHITE if color == 'w' else chess.BLACK, piece_type)] = pygame.image.load(filename)
                else:
                    pieces[(chess.WHITE if color == 'w' else chess.BLACK, piece_type)] = create_placeholder_piece(color, piece_char)
    except:
        for color in [chess.WHITE, chess.BLACK]:
            for piece_type in piece_types.values():
                pieces[(color, piece_type)] = create_placeholder_piece(
                    'w' if color == chess.WHITE else 'b',
                    next(k for k, v in piece_types.items() if v == piece_type)
                )
    
    return pieces

def create_placeholder_piece(color:pygame.Color, piece_char:str):
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    color_rgb = WHITE if color == 'w' else BLACK
    pygame.draw.circle(surf, color_rgb, (25, 25), 20)
    font = pygame.font.SysFont("Arial", 24, bold=True)
    text = font.render(piece_char.upper(), True, BLACK if color == 'w' else WHITE)
    text_rect = text.get_rect(center=(25, 25))
    surf.blit(text, text_rect)
    return surf

logo = pygame.image.load("Assets/Sprites/logo.png")
icon = pygame.image.load("Assets/Sprites/icon.png")
company_logo = pygame.image.load("Assets/Sprites/company.png")

FRAME_RATE = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
HIGHLIGHT_RADIUS = 7.5
PIECE_SIZE = 50
BOARD_SIZE = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = pygame.Color('#b58863')
BEIGE = pygame.Color('#f0d9b5')
HIGHLIGHT = pygame.Color('#8877DD99')
MOVE_HIGHLIGHT = pygame.Color('#5fa14460')
CAPTURE_HIGHLIGHT = pygame.Color('#d42a2a60')

BOARD_CONFIG = [
    ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'], 
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
    ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R']
]

def calculate_board_coordinates(board_x, board_y, board_size):
    square_size = board_size / 8
    ranks = {}
    files = {}
    
    for i in range(8):
        rank_num = 8 - i
        rank_y = board_y + (i + 0.5) * square_size
        ranks[rank_num] = rank_y
        
        file_letter = chess.FILE_NAMES[i]
        file_x = board_x + (i + 0.5) * square_size
        files[file_letter] = file_x
    
    return ranks, files

def square_to_coords(square):
    file_idx = chess.square_file(square)
    rank_idx = chess.square_rank(square)
    file_letter = chess.FILE_NAMES[file_idx]
    rank_number = rank_idx + 1
    return FILES[file_letter], RANKS[rank_number]

def coords_to_square(x, y):
    file_letter = None
    rank_number = None
    
    for file, file_x in FILES.items():
        if abs(x - file_x) < 25:
            file_letter = file
            break
    
    for rank, rank_y in RANKS.items():
        if abs(y - rank_y) < 25:
            rank_number = rank
            break
    
    if file_letter and rank_number:
        file_idx = chess.FILE_NAMES.index(file_letter)
        rank_idx = rank_number - 1
        return chess.square(file_idx, rank_idx)
    return None

# CLASSES
class BoardLocation:
    def __init__(self, rank:int, file:int):
        self.rank = rank
        self.file = file

class MovementPattern:
    def __init__(self, name:str, pattern:list[BoardLocation], movement_type:str):
        self.movement_type = movement_type # "normal", "king" can move into check,"jump" means ignore pieces in the way
        self.name = name
        self.pattern = pattern # list of tuples (x, y) of what to add to the current position (0, 0)
    
    def get_resulting_positions(self, location:BoardLocation): # this does not check for board limits or pieces in the way
        positions = []
        for move in self.pattern:
            new_rank = location.rank + move.rank
            new_file = location.file + move.file
            positions.append(BoardLocation(new_rank, new_file))
        return positions

    def get_movement_type(self):
        return self.movement_type

class ChessBoard:
    def __init__(self, x, y, length, dark, light):
        self.x = x
        self.y = y
        self.s_length = length / 8
        self.dark = dark
        self.light = light
    
    def calculate_positions(self):
        """Generate RANKS and FILES dictionaries based on board position."""
        ranks = {i + 1: int(self.y + (7 - i) * self.s_length + self.s_length / 2) for i in range(8)}
        files = {chr(97 + j): int(self.x + j * self.s_length + self.s_length / 2) for j in range(8)}
        return ranks, files
        
    def draw(self, screen):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = self.dark
                else:
                    color = self.light
                pygame.draw.rect(screen, color, (self.x + i * self.s_length, self.y + j * self.s_length, self.s_length, self.s_length))

class Piece:
    def __init__(self, chess_piece, sprite, rect, square):
        self.chess_piece = chess_piece
        self.colour = chess_piece.color
        self.type = chess_piece.piece_type
        self.sprite = sprite
        self.rect = rect
        self.square = square
        self.legal_moves = []
        self.is_selected = False
    
    def update_legal_moves(self, board:chess.Board):
        self.legal_moves = []
        for move in board.legal_moves:
            if move.from_square == self.square:
                self.legal_moves.append(move.to_square)
    
    def draw(self, screen:pygame.Surface):
        screen.blit(self.sprite, self.rect)
        
    def draw_legal_moves(self, screen, chessboard, board):
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, self.rect, 3)
            
            for square in self.legal_moves:
                x, y = square_to_coords(square)
                
                is_capture = board.piece_at(square) is not None
                
                # Check for en passant capture
                if self.type == chess.PAWN and not is_capture:
                    # Get the en passant square from the board
                    if board.ep_square is not None and square == board.ep_square:
                        is_capture = True
                
                if is_capture:
                    highlight_rect = central_rect(x, y, chessboard.s_length, chessboard.s_length)
                    pygame.draw.rect(screen, CAPTURE_HIGHLIGHT, highlight_rect)
                    pygame.draw.circle(screen, GREEN, (x, y), HIGHLIGHT_RADIUS)
                else:
                    highlight_rect = central_rect(x, y, chessboard.s_length, chessboard.s_length)
                    pygame.draw.rect(screen, MOVE_HIGHLIGHT, highlight_rect)
                    pygame.draw.circle(screen, GREEN, (x, y), HIGHLIGHT_RADIUS)
    
    def move_to(self, new_square, board):
        move = None
        
        if self.type == chess.PAWN:
            end_rank = chess.square_rank(new_square)
            if (self.colour == chess.WHITE and end_rank == 7) or \
               (self.colour == chess.BLACK and end_rank == 0):
                move = chess.Move(self.square, new_square, promotion=chess.QUEEN)
        
        if move is None:
            move = chess.Move(self.square, new_square)
        
        if move in board.legal_moves:
            # Check for en passant capture before making the move
            is_en_passant = self.type == chess.PAWN and board.ep_square == new_square
            
            en_passant_target = None
            if is_en_passant:
                # Calculate the square where the captured pawn is located
                if self.colour == chess.WHITE:
                    en_passant_target = new_square - 8  # Pawn is one rank below
                else:
                    en_passant_target = new_square + 8  # Pawn is one rank above
            
            # Make the move on the chess board
            board.push(move)
            self.square = new_square
            x, y = square_to_coords(new_square)
            self.rect = central_rect(x, y, self.rect.width, self.rect.height)
            self.update_legal_moves(board)
            
            try:
                if board.is_capture(move) or is_en_passant:
                    pygame.mixer.Sound("Assets/Sounds/capture.wav").play()
                else:
                    pygame.mixer.Sound("Assets/Sounds/move.wav").play()
            except:
                pass
                
            return True, en_passant_target
        return False, None

def splash_screen(icons_to_show:list[pygame.Surface]):
    alpha = 0
    dir = "+"
    icon_idx = 0
    for icon in icons_to_show:
        icons_to_show[icons_to_show.index(icon)] = pygame.transform.scale(icon, (200, 200))
    icon = icons_to_show[icon_idx]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
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
        pygame.display.flip()
        clock.tick(FRAME_RATE)

def central_rect(x, y, width, height):
    return pygame.Rect(x - width / 2, y - height / 2, width, height)

def create_pieces_from_board(board):
    pieces = []
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            x, y = square_to_coords(square)
            sprite = pygame.transform.scale(piece_sprites[(piece.color, piece.piece_type)], (PIECE_SIZE, PIECE_SIZE))
            pieces.append(
                Piece(
                    chess_piece=piece,
                    sprite=sprite,
                    rect=central_rect(x, y, PIECE_SIZE, PIECE_SIZE),
                    square=square
                )
            )
    
    for piece in pieces:
        piece.update_legal_moves(board)
    
    return pieces

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("Chezz.com")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

if __name__ == "__main__":
    splash_screen([company_logo, logo])

    # Create the chessboard and pieces
    piece_sprites = load_piece_sprites()
    chessboard = ChessBoard(x=100, y=100, length=BOARD_SIZE, dark=BROWN, light=BEIGE)
    RANKS, FILES = calculate_board_coordinates(100, 100, BOARD_SIZE)
    board = chess.Board()
    pieces = create_pieces_from_board(board)
    selected_piece = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                clicked_on_piece = False
                for piece in pieces:
                    if piece.rect.collidepoint(mouse_pos) and piece.colour == (chess.WHITE if board.turn == chess.WHITE else chess.BLACK):
                        if selected_piece:
                            selected_piece.is_selected = False
                        
                        piece.is_selected = True
                        selected_piece = piece
                        clicked_on_piece = True
                        break
                
                if not clicked_on_piece and selected_piece:
                    square = coords_to_square(*mouse_pos)
                    if square is not None and square in selected_piece.legal_moves:
                        captured_piece = None
                        for piece in pieces:
                            if piece.square == square:
                                captured_piece = piece
                                break
                        
                        # Move the piece and check if it was an en passant capture
                        move_successful, en_passant_target = selected_piece.move_to(square, board)
                        
                        if move_successful:
                            # Remove the captured piece if there was one
                            if captured_piece:
                                pieces.remove(captured_piece)
                            
                            # For en passant, remove the captured pawn
                            if en_passant_target is not None:
                                for piece in pieces[:]:  # Create a copy of the list to safely modify it
                                    if piece.square == en_passant_target:
                                        pieces.remove(piece)
                                        break
                            
                            # Update all pieces' legal moves
                            for piece in pieces:
                                piece.update_legal_moves(board)
                            
                            # Handle pawn promotion
                            if selected_piece.type == chess.PAWN:
                                rank = chess.square_rank(selected_piece.square)
                                if (selected_piece.colour == chess.WHITE and rank == 7) or \
                                   (selected_piece.colour == chess.BLACK and rank == 0):
                                    queen = chess.Piece(chess.QUEEN, selected_piece.colour)
                                    x, y = square_to_coords(selected_piece.square)
                                    new_queen = Piece(
                                        chess_piece=queen,
                                        sprite=pygame.transform.scale(piece_sprites[(queen.color, queen.piece_type)], (PIECE_SIZE, PIECE_SIZE)),
                                        rect=central_rect(x, y, PIECE_SIZE, PIECE_SIZE),
                                        square=selected_piece.square
                                    )
                                    pieces.remove(selected_piece)
                                    pieces.append(new_queen)
                                    new_queen.update_legal_moves(board)
                            
                            selected_piece.is_selected = False
                            selected_piece = None
                    elif selected_piece:
                        selected_piece.is_selected = False
                        selected_piece = None

        screen.fill(BLACK)
        chessboard.draw(screen)
        
        if selected_piece:
            selected_piece.draw_legal_moves(screen, chessboard, board)
        
        for piece in pieces:
            piece.draw(screen)
        
        font = pygame.font.SysFont("Arial", 24)
        turn_text = font.render("Turn: " + ("White" if board.turn == chess.WHITE else "Black"), True, WHITE)
        screen.blit(turn_text, (10, 10))
        
        if board.is_check():
            check_text = font.render("CHECK!", True, (255, 0, 0))
            screen.blit(check_text, (10, 40))
        
        if board.is_checkmate():
            end_text = font.render("CHECKMATE! " + ("Black" if board.turn == chess.WHITE else "White") + " wins!", True, (255, 0, 0))
            screen.blit(end_text, (SCREEN_WIDTH // 2 - 150, 10))
        elif board.is_stalemate():
            end_text = font.render("STALEMATE! Draw game.", True, (255, 0, 0))
            screen.blit(end_text, (SCREEN_WIDTH // 2 - 120, 10))
        
        pygame.display.flip()
        clock.tick(FRAME_RATE)