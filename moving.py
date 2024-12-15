import numpy as np
from configs import SQ_SIZE, WHITE
from core import TEAM1, TEAM2, TRAPS, redraw_window
from victories import check_Victories
import pygame
weights = {
    1: 1,  # Conejo dorado
    2: 2,  # Gato dorado
    3: 3,  # Perro dorado
    4: 4,  # Caballo dorado
    5: 5,  # Camello dorado
    6: 6,  # Elefante dorado
    7: 1,  # Conejo plateado
    8: 2,  # Gato plateado
    9: 3,  # Perro plateado
    10: 4,  # Caballo plateado
    11: 5,  # Camello plateado
    12: 6  # Elefante plateado
}


def applly_one_animated_move(board, move, WIN, matrix_moviment, turn, moves):
    fromPiece, toPiece = move
    prevRow, prevCol = fromPiece
    newRow, newCol = toPiece

    cell_width = SQ_SIZE
    cell_height = SQ_SIZE

    start_x = prevCol * cell_width
    start_y = prevRow * cell_height
    end_x = newCol * cell_width
    end_y = newRow * cell_height

    steps = 20
    delta_x = (end_x - start_x) / steps
    delta_y = (end_y - start_y) / steps

    piece = board[prevRow, prevCol]

    # Cargar las imágenes de las piezas
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
    piece_image = piece_images.get(piece)

    for step in range(steps):
        current_x = start_x + delta_x * step
        current_y = start_y + delta_y * step

        # Actualiza la ventana omitiendo la posición original de la pieza
        redraw_window(WIN, fall_in_trap, board, TRAPS, matrix_moviment, turn, moves, moving_piece=piece_image, moving_pos=(current_x, current_y), moving_from=(prevRow, prevCol))
        pygame.display.update()
        pygame.time.delay(20)

    # Actualiza el tablero final
    board[newRow, newCol] = piece
    board[prevRow, prevCol] = 0
    board = fall_in_trap(board)
    return board





# get moves
def get_push_pull_moves(board, cell_in_attack, cell_to_attack):
    matrix_moviment = np.zeros((8, 8))
    # Si tiene un vecino enemigo más pesado, no puede moverse
    if has_neightbor_enemy_stronger(board, cell_in_attack) and not has_neightbor_team(board, cell_in_attack):
        return matrix_moviment
    # Movimientos de empuje, empujar cell_to_attack
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # Movimientos posibles: arriba, abajo, izquierda, derecha
        r, c = cell_to_attack[0] + i, cell_to_attack[1] + j
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] == 0:
            matrix_moviment[r, c] = 2
    # Movimientos de jalar, jalar cell_in_attack
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # Movimientos posibles: arriba, abajo, izquierda, derecha
        r, c = cell_in_attack[0] + i, cell_in_attack[1] + j
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] == 0:
            matrix_moviment[r, c] = 3
    return matrix_moviment

def get_valit_moves(board, selected_piece):
    global TRAPS
    row, col = selected_piece
    isGoldRabbit = board[row, col] == 1
    isSilverRabbit = board[row, col] == 7
    valid_moves = np.zeros((8, 8), dtype=int)
    # Si tiene un vecino enemigo más pesado, no puede moverse
    if has_neightbor_enemy_stronger(board, selected_piece) and not has_neightbor_team(board, selected_piece):
        return valid_moves
    # Movimientos posibles: arriba, abajo, izquierda, derecha
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r, c = row + i, col + j
        # Si está dentro de los límites y la celda está vacía
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] == 0:
            # Si es conejo dorado no puede moverse hacia atrás
            if isGoldRabbit and i == -1:
                continue
            # Si es conejo plateado no puede moverse hacia atrás
            if isSilverRabbit and i == 1:
                continue
            # Si el siguiente movimiento es una trampa, no se puede mover a menos que tenga un compañero cerca
            if (r, c) in TRAPS and not has_neightbor_team(board, (r, c), selected_piece):
                continue
            valid_moves[r, c] = 1
    return valid_moves

def get_pieces_can_attack(board, cell):
    enemy_team = TEAM1 if board[cell] in TEAM2 else TEAM2
    matrix_moviment = np.zeros((8, 8))
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # Movimientos posibles: arriba, abajo, izquierda, derecha
        r, c = cell[0] + i, cell[1] + j
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] in enemy_team:
            # Si la celda enemiga es más pesada que la celda actual
            if weights[board[r, c]] > weights[board[cell]]:
                matrix_moviment[r, c] = 4
    return matrix_moviment

def get_piece_to_attack(board, cell):
    enemy_team = TEAM1 if board[cell] in TEAM2 else TEAM2
    matrix_moviment = np.zeros((8, 8))
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # Movimientos posibles: arriba, abajo, izquierda, derecha
        r, c = cell[0] + i, cell[1] + j
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] in enemy_team:
            # Si la celda enemiga es más ligera que la celda actual
            if weights[board[r, c]] < weights[board[cell]]:
                matrix_moviment[r, c] = 4
    return matrix_moviment

# Neighbors
def has_neightbor_team(board, position, selected_piece=None):
    row, col = position
    myRow, myCol = selected_piece if selected_piece else (row, col)
    piece = board[myRow, myCol]

    # Determinar equipo basado en el valor de la ficha
    team = TEAM1 if piece in TEAM1 else TEAM2 if piece in TEAM2 else None
    if not team:  # Si no pertenece a ningún equipo, no tiene vecinos válidos
        return False

    # Verificar vecinos
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r, c = row + i, col + j
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] in team:
            # Si la ficha no soy yo mismo y está en mi equipo
            if (r, c) != (myRow, myCol):
                return True
    return False

def has_neightbor_enemy(board, position):
    row, col = position
    piece = board[row, col]
    enemy_team = TEAM1 if piece in TEAM2 else TEAM2 if piece in TEAM1 else None
    if not enemy_team:
        return False
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r, c = row + i, col + j
        # Si está dentro de los límites y la celda tiene una ficha del equipo contrario
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] in enemy_team:
            return True
    return False

def has_neightbor_enemy_stronger(board, position):
    row, col = position
    piece = board[row, col]
    enemy_team = TEAM1 if piece in TEAM2 else TEAM2 if piece in TEAM1 else None
    if not enemy_team:
        return False
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r, c = row + i, col + j
        # Si está dentro de los límites y la celda tiene una ficha del equipo contrario
        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] in enemy_team:
            # Si la ficha enemiga es más pesada que la celda actual
            if weights[board[r, c]] > weights[piece]:
                return True
    return False

# Movements
def move_piece(board, selected_piece, target_pos):
    row, col = selected_piece
    target_row, target_col = target_pos
    board[target_row, target_col] = board[row, col]
    board[row, col] = 0
    return board

def fall_in_trap(board):
    global TRAPS
    for trap in TRAPS:
        row, col = trap
        if board[row, col] != 0:
            if not has_neightbor_team(board, trap):
                board[row, col] = 0
    return board

def skip_turn(moves, board, turn):
    if moves == 4:
        print("No se han realizado movimientos. No se puede pasar el turno.")
        return moves, turn, None
    print(f"Turno pasado. Jugador {turn} cambia de turno.")
    turn = 2 if turn == 1 else 1  # Cambiar turn entre jugador 1 y 2
    moves = 4  # Reiniciar el contador de movimientos
    winner = check_Victories(board)  # Verificar si hay un ganador
    return moves, turn, winner

def push_piece(board, cell_to_move, cell_in_attack, cell_to_attack):
    board[cell_to_move] = board[cell_to_attack]
    board[cell_to_attack] = board[cell_in_attack]
    board[cell_in_attack] = 0
    return board

def pull_piece(board, cell_to_move, cell_in_attack, cell_to_attack):
    board[cell_to_move] = board[cell_in_attack]
    board[cell_in_attack] = board[cell_to_attack]
    board[cell_to_attack] = 0
    return board

# Función para calcular la celda del tablero desde las coordenadas del mouse
def get_cell_from_mouse(pos):
    x, y = pos
    row = y // SQ_SIZE
    col = x // SQ_SIZE
    return (row, col)

# Función para controlar los clicks del mouse
def click_controller_steps(matrix_moviment, cell, board, moves, selected_piece, piece_in_attack, piece_to_attack, turn):
    from draw_logic import create_board_moviment
    global TRAPS
    default_matrix = create_board_moviment()
    team = TEAM1 if turn == 1 else TEAM2
    enemy_team = TEAM2 if turn == 1 else TEAM1
    row, col = cell
    # Si el click fue a una pieza del equipo contrario es para
    # hacerle push o pull
    # Entonces si tiene vecinos enemigos (fichas de mi equipo)
    # Escoger con cual ficha se le hace push o pull
    if board[row, col] in enemy_team:
        if not piece_in_attack:
            if has_neightbor_enemy(board, cell):
                print("tiene vecinos enemigos")
                # Si tiene fichas de mi equipo, escoger con cual hacer push o pull
                matrix_moviment = get_pieces_can_attack(board, cell)
                piece_to_attack = cell
        return matrix_moviment, moves, selected_piece, board, piece_in_attack, piece_to_attack

    if np.array_equal(matrix_moviment, default_matrix):
        if board[row, col] == 0:
            print("No se ha seleccionado ninguna pieza")
            return matrix_moviment, moves, selected_piece, board, piece_in_attack, piece_to_attack
        matrix_moviment = get_valit_moves(board, cell)
        selected_piece = cell
    else:
        if matrix_moviment[cell] == 1:
            board = move_piece(board, selected_piece, cell)
            moves -= 1
            print(f"Clicked on cell: ({row}, {col}), Board value: {board[row, col]}")
            matrix_moviment = default_matrix
            selected_piece = None
        elif matrix_moviment[cell] == 2:
            if moves < 2:
                print("No hay suficientes movimientos para empujar")
                return matrix_moviment, moves, selected_piece, board, piece_in_attack, piece_to_attack
            print(f"Pushing piece from: {piece_to_attack} to: {cell}")
            board = push_piece(board, cell, piece_in_attack, piece_to_attack)
            moves -= 2
            print(f"Clicked on cell: ({row}, {col}), Board value: {board[row, col]}")
            matrix_moviment = default_matrix
            piece_in_attack = None
            piece_to_attack = None
        elif matrix_moviment[cell] == 3:
            if moves < 2:
                print("No hay suficientes movimientos para jalar")
                return matrix_moviment, moves, selected_piece, board, piece_in_attack, piece_to_attack
            print(f"Pulling piece from: {piece_in_attack} to: {cell}")
            board = pull_piece(board, cell, piece_in_attack, piece_to_attack)
            moves -= 2
            print(f"Clicked on cell: ({row}, {col}), Board value: {board[row, col]}")
            matrix_moviment = default_matrix
            piece_in_attack = None
            piece_to_attack = None
        elif matrix_moviment[cell] == 4:
            piece_in_attack = cell
            matrix_moviment = get_push_pull_moves(board, piece_in_attack, piece_to_attack)
            print(f"piece in attack: {piece_in_attack}")
        elif matrix_moviment[cell] == 0:
            print("No es un movimiento válido")
            piece_in_attack = None
            piece_to_attack = None
            matrix_moviment = default_matrix
        
    return matrix_moviment, moves, selected_piece, board, piece_in_attack, piece_to_attack
