# IMPORTS/DEPENDENCIES
import pygame
import chess
import os

# INITIASATIONS
pygame.init()
pygame.font.init()
pygame.mixer.init()

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
                filename = f"Assets/Sprites/{color}_{piece_char}.png"
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

def create_placeholder_piece(color, piece_char):
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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BrankN = pygame.Color('#b58863')
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
    ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'], 
    ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook']
    ]

RANKS = {1: 575, 2: 525, 3: 475, 4: 425, 5: 375, 6: 325, 7: 275, 8: 225}
FILES = {'a': 225, 'b': 275, 'c': 325, 'd': 375, 'e': 425, 'f': 475, 'g': 525, 'h': 575}

class ChessBoard:
    def __init__(self, x, y, length, dark, light):
        self.x = x + length / 2
        self.y = y + length / 2
        self.s_length = length / 8
        self.dark = dark
        self.light = light
        self.ranks_locations, self.files_locations = self.calculate_positions()

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
    def __init__(self, x, y, color, type):
        self.x = x
        self.y = y
        self.color = color
        self.type = type

    def draw(self, screen):
        if self.type == "pawn":
            screen.blit(icon_pawn, (self.x, self.y))


# FUNCTIONS
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

piece_sprites = load_piece_sprites()

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

chessboard = ChessBoard(x=0, y=0, length=400, dark=BROWN, light=BEIGE)
board = chess.Board()
piece = Piece(50, 50, "white", "pawn")

if __name__ == "__main__":
    #splash_screen([company_logo, logo])
    while True:
        clock.tick(FRAME_RATE)
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
        pygame.draw.rect(screen, GREEN, central_rect(FILES['a'], RANKS[1], 10, 10))
        pygame.display.flip()
        clock.tick(FRAME_RATE)