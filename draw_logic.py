import pygame
import numpy as np

from configs import ROWS, COLS, SQ_SIZE, WIDTH, BUTTON_WIDTH, BUTTON_HEIGHT, HEIGHT

# Crear la matriz del tablero
def create_board():
    board = np.zeros((ROWS, COLS), dtype=int)
    # 1 elefante, 1 camello, 2 caballos, 2 perros, 2 gatos, 8 conejos
    initial_pieces = [6, 5, 4, 4, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
    pieces = initial_pieces.copy()
    np.random.shuffle(pieces)
    # colocarse en la primera y segunda fila de cada jugador
    for i, row in enumerate([0, 1, 6, 7]):
        for col in range(COLS):
            board[row, col] = pieces.pop()
            if row >= 6:
                board[row, col] += 6
        if row == 1:
            pieces = initial_pieces.copy()
            np.random.shuffle(pieces)
    # test board
    # board = np.array([
    #     [6, 5, 4, 4, 3, 3, 2, 2],
    #     [1, 1, 1, 1, 1, 1, 1, 1],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [7, 7, 7, 7, 7, 7, 7, 7],
    #     [12, 11, 10, 10, 9, 9, 8, 8],
    # ])
    return board

def create_board_moviment():
    valid_moves = np.zeros((ROWS, COLS), dtype=int)
    return valid_moves

# Dibujar el tablero
def draw_board(win, board, traps):
    # Cargar y redimensionar imágenes
    celda_par = pygame.transform.scale(pygame.image.load("./images/celdapar.jpg"), (SQ_SIZE, SQ_SIZE))
    celda_impar = pygame.transform.scale(pygame.image.load("./images/celdaimpar.jpg"), (SQ_SIZE, SQ_SIZE))
    trampa = pygame.transform.scale(pygame.image.load("./images/trampa.jpg"), (SQ_SIZE, SQ_SIZE))

    for row in range(ROWS):
        for col in range(COLS):
            image = celda_par if (row + col) % 2 == 0 else celda_impar
            win.blit(image, (col * SQ_SIZE, row * SQ_SIZE))

    # Dibujar trampas
    for trap in traps:
        r, c = trap
        win.blit(trampa, (c * SQ_SIZE, r * SQ_SIZE))

# Dibujar las piezas
def draw_pieces(win, board):
    # Cargar y redimensionar imágenes de piezas
    piece_images = {
        6: pygame.transform.scale(pygame.image.load("./images/pieces/e0.png"), (SQ_SIZE, SQ_SIZE)),  # Elefante dorado
        5: pygame.transform.scale(pygame.image.load("./images/pieces/c0.png"), (SQ_SIZE, SQ_SIZE)),  # Camello dorado
        4: pygame.transform.scale(pygame.image.load("./images/pieces/h0.png"), (SQ_SIZE, SQ_SIZE)),  # Caballo dorado
        3: pygame.transform.scale(pygame.image.load("./images/pieces/d0.png"), (SQ_SIZE, SQ_SIZE)),  # Perro dorado
        2: pygame.transform.scale(pygame.image.load("./images/pieces/ca0.png"), (SQ_SIZE, SQ_SIZE)), # Gato dorado
        1: pygame.transform.scale(pygame.image.load("./images/pieces/r0.png"), (SQ_SIZE, SQ_SIZE)),  # Conejo dorado
        12: pygame.transform.scale(pygame.image.load("./images/pieces/e1.png"), (SQ_SIZE, SQ_SIZE)),  # Elefante plateado
        11: pygame.transform.scale(pygame.image.load("./images/pieces/c1.png"), (SQ_SIZE, SQ_SIZE)),  # Camello plateado
        10: pygame.transform.scale(pygame.image.load("./images/pieces/h1.png"), (SQ_SIZE, SQ_SIZE)),  # Caballo plateado
        9: pygame.transform.scale(pygame.image.load("./images/pieces/d1.png"), (SQ_SIZE, SQ_SIZE)), # Perro plateado
        8: pygame.transform.scale(pygame.image.load("./images/pieces/ca1.png"), (SQ_SIZE, SQ_SIZE)),# Gato plateado
        7: pygame.transform.scale(pygame.image.load("./images/pieces/r1.png"), (SQ_SIZE, SQ_SIZE))   # Conejo plateado
    }

    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row, col]
            if piece != 0:
                image = piece_images.get(piece)
                if image:
                    win.blit(image, (col * SQ_SIZE, row * SQ_SIZE))

# Función para dibujar el botón "Pasar Turno"
def draw_pass_turn_button(WIN):
    font = pygame.font.SysFont(None, 30)
    button_rect = pygame.Rect(WIDTH - BUTTON_WIDTH/2 - WIDTH/2, 0, BUTTON_WIDTH, BUTTON_HEIGHT)  # Ubicación en la esquina
    pygame.draw.rect(WIN, (0, 0, 255), button_rect)  # Color azul para el botón
    pygame.draw.rect(WIN, (0, 0, 0), button_rect, 3)  # Bordes del botón

    # Texto del botón
    text = font.render("Pasar Turno", True, (255, 255, 255))  # Color blanco para el texto
    WIN.blit(text, (button_rect.x + (BUTTON_WIDTH - text.get_width()) // 2, button_rect.y + (BUTTON_HEIGHT - text.get_height()) // 2))
    
    return button_rect

def draw_turn_moves(WIN, turn, moves):
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Turno del jugador: {turn} | Movimientos: {moves}", True, (0, 100, 250))
    # text_bg
    text_bg = pygame.Rect(WIDTH - text.get_width(), HEIGHT - text.get_height(), text.get_width(), text.get_height())
    pygame.draw.rect(WIN, (0, 0, 0), text_bg)
    # text
    WIN.blit(text, (WIDTH - text.get_width(), HEIGHT - text.get_height()))

def draw_waiting_for_IA(WIN):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Esperando a la IA...", True, (0, 100, 250))
    # text_bg
    text_bg = pygame.Rect(WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2, text.get_width(), text.get_height())
    pygame.draw.rect(WIN, (0, 0, 0), text_bg)
    # text
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

def draw_possible_moves(WIN, matrix_moviment):
    for row in range(ROWS):
        for col in range(COLS):
            # Si es moverse es verde con opacidad 50%
            if matrix_moviment[row, col] == 1:
                pygame.draw.rect(WIN, (0, 255, 0, 128), (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            # Si es empujar es rojo con opacidad 50%
            elif matrix_moviment[row, col] == 2:
                pygame.draw.rect(WIN, (255, 0, 0, 128), (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            # Si es jalar es azul con opacidad 50%
            elif matrix_moviment[row, col] == 3:
                pygame.draw.rect(WIN, (0, 0, 255, 128), (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            #  Si es escoger con quien atacar es amarillo con opacidad 50%
            elif matrix_moviment[row, col] == 4:
                pygame.draw.rect(WIN, (255, 255, 0, 128), (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))