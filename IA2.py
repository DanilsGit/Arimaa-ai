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
            turn.append(current_moves[:])
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
                    # for push in pushes_moves:
                    #     if len(current_moves) < 2:
                    #         continue
                    #     to_move = [push[1]] + [push[0]]
                    #     new_current_moves = current_moves[:] + [to_move]
                    #     new_board = board.copy()
                    #     new_board = applly_one_move(new_board, push[1])
                    #     new_board = applly_one_move(new_board, push[0])
                    # for pull in pulls_moves:
                    #     if len(current_moves) < 2:
                    #         continue
                    #     to_move = [pull[1]] + [pull[0]]
                    #     new_current_moves = current_moves[:] + [to_move]
                    #     new_board = board.copy()
                    #     new_board = applly_one_move(new_board, pull[1])
                    #     new_board = applly_one_move(new_board, pull[0])
                    #     generate_moves(new_board, new_current_moves)


        # Si la profundidad es mayor que 0, agregar el turno parcial
        if len(current_moves) > 0:
            turn.append(current_moves[:])
        
    generate_moves(board, [])
    # reverse turn para obtener jugadas sin devolverse
    # turn.reverse()
    return turn

# Configuración inicial para Minimax con poda alfa-beta.
def minimax(board, depth, maximizing_player, alpha=-float("inf"), beta=float("inf")):
    """
    Implementación del algoritmo Minimax con poda alfa-beta para Arimaa.
    
    Args:
        board: Objeto que representa el estado actual del juego.
        depth: Profundidad máxima de búsqueda.
        maximizing_player: Booleano que indica si es el turno del jugador maximizador.
        alpha: Valor alfa para la poda.
        beta: Valor beta para la poda.

    Returns:
        dict: Contiene el puntaje de la evaluación y los mejores movimientos como lista de tuplas ((fila_inicio, col_inicio), (fila_fin, col_fin)).
    """
    if depth == 0 or check_Victories(board) is not None:
        return {"score": evaluate_board(board, maximizing_player), "moves": []}

    legal_moves = get_AI_movements(board, maximizing_player)

    if not maximizing_player:
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

# Funciones auxiliares
def evaluate_board(board, maximizing_player):
    """Evalúa el tablero y devuelve una puntuación."""
    # Sumatoria de las distancias de los conejos de MAX
    # Desde su posición hasta la meta.
    team = TEAM2 if maximizing_player else TEAM2
    my_rabbit = 7 if maximizing_player else 1
    count_enemy_team = 0
    count_ally_team = 0
    score_rabbit = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row, col]
            if piece == my_rabbit:
                score_rabbit += (len(board) - row)
            if piece not in team:
                count_enemy_team += 1
            if piece in team:
                count_ally_team += 1

    allys_no_killed = abs(count_ally_team - 8)

    heuristic = score_rabbit

    return heuristic

# Ejemplo de inicialización del tablero
if __name__ == "__main__":
    board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 12, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ])
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
