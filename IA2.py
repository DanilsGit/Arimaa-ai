import numpy as np
from victories import check_Victories
from moving import get_valit_moves
from core import TEAM1, TEAM2

def apply_move(board, move):
    board = board.copy()
    fromPiece, toPiece = move
    prevRow, prevCol = fromPiece
    newRow, newCol = toPiece
    board[newRow, newCol] = board[prevRow, prevCol]
    board[prevRow, prevCol] = 0
    return board


def get_AI_movements(board, maximizing_player, depth=0):
    """
    Obtiene los movimientos de la IA.
    turns -> array de steps [1:4]
    steps -> array de tuplas ((from), (to))
    from -> tupla (row, col)
    to -> tupla (row, col)
    """
    team = TEAM2 if maximizing_player else TEAM1
    turn = []

    def generate_moves(board, depth, current_moves):
        if depth == 4:
            turn.append(current_moves[:])
            return

        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row, col]
                if piece == team[5]:  # Filtrar piezas del equipo actual
                    valid_moves = get_moves_as_tuples(board, (row, col))
                    for move in valid_moves:
                        # Crear nuevas copias para evitar modificaciones no deseadas
                        new_current_moves = current_moves[:] + [move]
                        new_board = board.copy()
                        new_board = apply_move(new_board, move)
                        # Llamada recursiva con tablero actualizado y profundidad incrementada
                        generate_moves(new_board, depth + 1, new_current_moves, turn, team)

        # Si la profundidad es mayor que 0, agregar el turno parcial
        if depth > 0 and current_moves not in turn:
            turn.append(current_moves[:])
        
    generate_moves(board, depth, [])
    return turn
                









    

# Configuración inicial para Minimax con poda alfa-beta.
MAX_DEPTH = 3

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

    legal_moves = get_valit_moves(board, None)  # Obtener movimientos válidos.
    print("Movimientos legales:", legal_moves)

    if maximizing_player:
        max_eval = float("-inf")
        best_moves = []

        for turn in legal_moves:
            cloned_game = board.clone()  # Clonar el estado del juego.
            cloned_game.apply_moves(turn)  # Aplicar los movimientos.
            result = minimax(cloned_game, depth - 1, False, alpha, beta)

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
            cloned_game = board.clone()  # Clonar el estado del juego.
            cloned_game.apply_moves(turn)  # Aplicar los movimientos.
            result = minimax(cloned_game, depth - 1, True, alpha, beta)

            if result["score"] < min_eval:
                min_eval = result["score"]
                best_moves = turn

            beta = min(beta, min_eval)
            if beta <= alpha:
                break  # Corte por alfa.

        return {"score": min_eval, "moves": best_moves}


# Funciones auxiliares

def is_terminal(board):
    """Determina si el tablero está en un estado terminal."""
    return check_Victories(board) is not None

def evaluate_board(board):
    """Evalúa el tablero y devuelve una puntuación."""
    # Placeholder: define tu propia heurística
    return np.sum(board)

def get_all_possible_moves(board, is_maximizing):
    """Obtiene todos los movimientos válidos para el jugador actual."""
    # Placeholder: genera movimientos dependiendo del jugador
    moves = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row, col]
            if is_maximizing and piece > 0:  # Ejemplo: piezas del jugador MAX
                moves.extend(get_valit_moves(board, (row, col)))
            elif not is_maximizing and piece < 0:  # Ejemplo: piezas del jugador MIN
                moves.extend(get_valit_moves(board, (row, col)))
    return moves

def get_moves_as_tuples(board, fromPiece):
    """
    Convierte los movimientos válidos desde `get_valit_moves` en tuplas ((start_row, start_col), (end_row, end_col)).
    """
    row, col = fromPiece
    valid_moves_board = get_valit_moves(board, fromPiece)
    moves = []

    for r in range(len(valid_moves_board)):
        for c in range(len(valid_moves_board[r])):
            if valid_moves_board[r][c] == 1:  # Si es un movimiento válido
                moves.append(((row, col), (r, c)))

    return moves

def make_move(board, move):
    """
    Aplica un movimiento al tablero. 
    `move` debe ser una tupla de dos posiciones: (origen, destino).
    """
    if len(move) != 2:
        raise ValueError(f"Formato inválido para el movimiento: {move}")
    
    start, end = move
    start_row, start_col = start
    end_row, end_col = end

    # Verifica que las posiciones están dentro del tablero
    if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
        raise ValueError(f"Posición fuera del tablero: {move}")

    # Mueve la pieza
    piece = board[start_row][start_col]
    board[start_row][start_col] = 0
    board[end_row][end_col] = piece

    return board


# Ejemplo de inicialización del tablero
if __name__ == "__main__":
    board = np.array([
        [1, 2, 3, 3, 4, 4, 5, 5],
        [6, 6, 6, 6, 6, 6, 6, 6],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 7, 12],
        [7, 7, 7, 7, 7, 7, 7, 0],
        [8, 8, 9, 9, 10, 10, 11, 7]
    ])
    is_maximizing = True
    print(get_AI_movements(board, is_maximizing))
    print(len(get_AI_movements(board, is_maximizing)))
