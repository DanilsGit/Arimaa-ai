import numpy as np
from victories import check_Victories
from moving import get_valit_moves, get_push_pull_moves, get_piece_to_attack, fall_in_trap
from core import TEAM1, TEAM2, TRAPS
import time

def applly_one_move(board, move):
    fromPiece, toPiece = move
    prevRow, prevCol = fromPiece
    newRow, newCol = toPiece
    board[newRow, newCol] = board[prevRow, prevCol]
    board[prevRow, prevCol] = 0
    board = fall_in_trap(board)
    return board


def aplly_moves(board, moves):
    for move in moves:
        board = applly_one_move(board, move)
    return board


def get_AI_movements(board, maximizing_player):
    """
    Obtiene los movimientos de la IA.
    turns -> array de steps [1:4]
    steps -> array de tuplas ((from), (to))
    from -> tupla (row, col)
    to -> tupla (row, col)
    """
    team = TEAM2 if maximizing_player else TEAM1
    turn = []

    def generate_moves(board, current_moves):
        if len(current_moves) == 4:
            turn.append(current_moves)
            return

        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row, col]
                if piece in team:
                    valid_moves = get_moves_as_tuples(board, (row, col))
                    pushes_moves, pulls_moves = get_pushes_pulls_as_tuples(board, (row, col))
                    for move in valid_moves:
                        # Crear nuevas copias para evitar modificaciones no deseadas
                        new_current_moves = current_moves[:] + [move]
                        new_board = board.copy()
                        new_board = applly_one_move(new_board, move)
                        # Llamada recursiva con tablero actualizado y profundidad incrementada
                        generate_moves(new_board, new_current_moves)
                    for push in pushes_moves:
                        if len(current_moves) > 2:
                            continue
                        to_move = [push[1]] + [push[0]]
                        new_current_moves = current_moves[:] + to_move
                        new_board = board.copy()
                        new_board = applly_one_move(new_board, push[1])
                        new_board = applly_one_move(new_board, push[0])
                        generate_moves(new_board, new_current_moves)
                    for pull in pulls_moves:
                        if len(current_moves) > 2:
                            continue
                        to_move = [pull[0]] + [pull[1]]
                        new_current_moves = current_moves[:] + to_move
                        new_board = board.copy()
                        new_board = applly_one_move(new_board, pull[0])
                        new_board = applly_one_move(new_board, pull[1])
                        generate_moves(new_board, new_current_moves)


        # Si la profundidad es mayor que 0, agregar el turno parcial
        if len(current_moves) > 0:
            turn.append(current_moves)
        
    generate_moves(board, [])
    # reverse turn para obtener jugadas sin devolverse
    # turn.reverse()
    return turn

# Configuración inicial para Minimax con poda alfa-beta.
def minimax(board, depth, maximizing_player, alpha=-float("inf"), beta=float("inf")):
    """
    Implementación del algoritmo Minimax con poda alfa-beta para Arimaa.
    
    Args:
        board: Matriz que representa el estado actual del juego.
        depth: Profundidad máxima de búsqueda.
        maximizing_player: Booleano que indica si es el turno del jugador maximizador.
        alpha: Valor alfa para la poda.
        beta: Valor beta para la poda.

    Returns:
        dict: Contiene el puntaje de la evaluación y los mejores movimientos como lista de tuplas ((fila_inicio, col_inicio), (fila_fin, col_fin)).
    """
    if depth == 0 or check_Victories(board) is not None:
        return {"score": evaluate_board(board), "moves": []}

    legal_moves = get_AI_movements(board, maximizing_player)

    if maximizing_player:
        max_eval = float("-inf")
        best_moves = []

        for turn in legal_moves:
            board_copy = board.copy()  # Clonar el estado del juego.
            board_copy = aplly_moves(board_copy, turn)  # Aplicar los movimientos.
            result = minimax(board_copy, depth - 1, False, alpha, beta)

            if result["score"] > max_eval:
                max_eval = result["score"]
                best_moves = turn

            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break  # Corte por beta.

        return {"score": max_eval, "moves": best_moves}
    else:
        min_eval = float("inf")
        best_moves = []

        for turn in legal_moves:
            board_copy = board.copy()  # Clonar el estado del juego.
            board_copy = aplly_moves(board_copy, turn)  # Aplicar los movimientos.
            result = minimax(board_copy, depth - 1, True, alpha, beta)

            if result["score"] < min_eval:
                min_eval = result["score"]
                best_moves = turn

            beta = min(beta, min_eval)
            if beta <= alpha:
                break  # Corte por alfa.

        return {"score": min_eval, "moves": best_moves}


# Funciones auxiliares
def get_moves_as_tuples(board, fromPiece):
    """
    Convierte los movimientos válidos desde `get_valit_moves` 
    en tuplas ((start_row, start_col), (end_row, end_col)).
                                (from, to)
    """
    row, col = fromPiece
    valid_moves_board = get_valit_moves(board, fromPiece)
    moves = []

    for r in range(len(valid_moves_board)):
        for c in range(len(valid_moves_board[r])):
            if valid_moves_board[r][c] == 1:  # Si es un movimiento válido
                moves.append(((row, col), (r, c)))

    return moves

def get_pushes_pulls_as_tuples(board, fromPiece):
    """
    Convierte los movimientos válidos desde `get_push_pull_moves` 
    en tuplas (((start_row, start_col), (end_row, end_col)), ((start_row, start_col), (end_row, end_col))).
                    ((fromPiece0, toPiece0), (fromPiece1, toPiece1))
    """
    row, col = fromPiece
    pieces_to_attack = []
    # Obtener las piezas que pueden atacar
    matrix_attack = get_piece_to_attack(board, fromPiece)
    for r in range(len(matrix_attack)):
        for c in range(len(matrix_attack[r])):
            if matrix_attack[r][c] == 4:
                pieces_to_attack.append((r, c))

    movesPush = []
    movesPull = []

    for piece in pieces_to_attack:
        valid_moves_board = get_push_pull_moves(board, fromPiece, piece)
        for r in range(len(valid_moves_board)):
            for c in range(len(valid_moves_board[r])):
                # Si es un movimiento de empuje
                if valid_moves_board[r][c] == 2:
                    movesPush.append((((row,col), piece), (piece, (r, c))))
                # Si es un movimiento de jalón
                elif valid_moves_board[r][c] == 3:
                    movesPull.append((((row,col), (r, c)), (piece, (row, col))))

    return movesPush, movesPull

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


# Funciones auxiliares
def evaluate_board(board):
    """Evalúa el tablero y devuelve una puntuación."""
    score_rabbit = 0
    count_my_pieces = 0
    count_enemy_pieces = 0
    trap_proximity_score = 0
    enemy_rabbit_score = 0
    enemy_piece_value_score = 0

    strong_pieces_in_middle = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row, col]
            if piece == 7:
                score_rabbit += (len(board) - row + 1)
            if piece in TEAM2:
                count_my_pieces += 1
                if piece >= 10 and (row == 3 or row == 4):
                    strong_pieces_in_middle += 1
            if piece in TEAM1:
                count_enemy_pieces += 1
                enemy_piece_value_score += piece  # Añadir el valor de la pieza enemiga
                if piece == 1:  # Si es un conejo enemigo
                    enemy_rabbit_score += row + 1
                for trap in TRAPS:
                    trap_row, trap_col = trap
                    distance_to_trap = abs(row - trap_row) + abs(col - trap_col)
                    if distance_to_trap == 1:
                        trap_proximity_score += 5
                    elif distance_to_trap == 2:
                        trap_proximity_score += 2

    # Entre menos piezas enemigas, mejor
    kill_score = len(TEAM1) - count_enemy_pieces

    heuristic = (strong_pieces_in_middle * 15) + (score_rabbit * 10) + (count_my_pieces * 5) + (kill_score * 20) + (trap_proximity_score * 5) - (enemy_rabbit_score * 10) - (enemy_piece_value_score * 10)

    return heuristic


# Ejemplo de inicialización del tablero
if __name__ == "__main__":
    board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 12, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 7, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ])
    # jala y empuja
    # board = np.array([
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 12, 1, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 1, 1, 1],
    #     [0, 0, 0, 0, 0, 0, 7, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    # ])
    # board2 = np.array([
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    # ])
    # board3 = np.array([
    #     [6, 5, 4, 4, 3, 3, 2, 2],
    #     [1, 1, 1, 1, 1, 1, 1, 1],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [7, 7, 7, 7, 7, 7, 7, 7],
    #     [12, 11, 10, 10, 9, 9, 8, 8],
    # ])
    is_maximizing = True
    # Obtener los movimientos de la IA uno a uno
    # turn = get_AI_movements(board, is_maximizing)
    
    # # Imprimir los movimientos
    # for i, moves in enumerate(turn):
    #     print(f"Turno {i + 1}: {moves}")
    startTime = time.time()
    # result = minimax(board3, 1, is_maximizing)
    # print(result["moves"])
    turn = get_AI_movements(board, is_maximizing)
    # Imprimir los movimientos
    # for i, moves in enumerate(turn):
    #     print(f"Turno {i + 1}: {moves}, len: {len(moves)}")
    endTime = time.time()
    print(f"Tiempo de ejecución: {endTime - startTime} segundos.")
