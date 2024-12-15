import numpy as np
from victories import check_Victories
from moving import get_valit_moves
from core import TEAM1, TEAM2
import time

def apply_move(board, move):
    fromPiece, toPiece = move
    prevRow, prevCol = fromPiece
    newRow, newCol = toPiece
    board[newRow, newCol] = board[prevRow, prevCol]
    board[prevRow, prevCol] = 0
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
                    for move in valid_moves:
                        # Crear nuevas copias para evitar modificaciones no deseadas
                        new_current_moves = current_moves[:] + [move]
                        new_board = board.copy()
                        new_board = apply_move(new_board, move)
                        # Llamada recursiva con tablero actualizado y profundidad incrementada
                        generate_moves(new_board, new_current_moves)

        # Si la profundidad es mayor que 0, agregar el turno parcial
        if len(current_moves) > 0:
            turn.append(current_moves[:])
        
    generate_moves(board, [])
    # reverse turn para obtener jugadas sin devolverse
    turn.reverse()
    return turn

def aplly_moves(board, moves):
    for move in moves:
        board = apply_move(board, move)
    return board

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

# Funciones auxiliares
def evaluate_board(board):
    """Evalúa el tablero y devuelve una puntuación."""
    # Sumatoria de las distancias de los conejos de MAX
    # Desde su base hasta la posición actual (de cada conejo)
    score_rabbit = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row, col]
            if piece == 7:
                score_rabbit += (len(board) - row)
    return score_rabbit

# Ejemplo de inicialización del tablero
if __name__ == "__main__":
    # board = np.array([
    #     [1, 2, 3, 3, 4, 4, 5, 5],
    #     [6, 6, 6, 6, 6, 6, 6, 6],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 7],
    #     [0, 0, 0, 0, 0, 0, 7, 12],
    #     [7, 7, 7, 7, 7, 7, 7, 0],
    #     [8, 8, 9, 9, 10, 10, 11, 7]
    # ])
    board2 = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 1, 12],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ])
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
    turn = get_AI_movements(board2, is_maximizing)
    # Imprimir los movimientos
    for i, moves in enumerate(turn):
        print(f"Turno {i + 1}: {moves}, len: {len(moves)}")
    endTime = time.time()
    print(f"Tiempo de ejecución: {endTime - startTime} segundos.")
