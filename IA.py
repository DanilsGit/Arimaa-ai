from moving import move_piece, push_piece, pull_piece, skip_turn, get_valit_moves, get_pieces_can_attack, get_push_pull_moves
from core import TEAM1, TEAM2, traps
import numpy as np
import copy

def generate_moves(board, turn, moves):
    """
    Genera una lista de posibles movimientos para un jugador en su turno actual.
    Retorna una lista de tuples con (nuevo_tablero, movimientos_restantes, nuevo_turno).
    """
    possible_moves = []
    team = TEAM1 if turn == 1 else TEAM2

    # Iterar sobre cada pieza del equipo actual
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row, col] in team:
                # Generar movimientos válidos básicos (mover)
                valid_moves = get_valit_moves(board, (row, col))
                for r, c in zip(*np.where(valid_moves == 1)):
                    # Crear una copia del tablero y simular el movimiento
                    new_board = copy.deepcopy(board)
                    move_piece(new_board, (row, col), (r, c))
                    possible_moves.append((new_board, moves - 1, turn))

                # Generar movimientos avanzados (empujar y jalar) si hay suficientes movimientos restantes
                if moves >= 2:
                    enemy_neighbors = get_pieces_can_attack(board, (row, col))
                    for enemy_r, enemy_c in zip(*np.where(enemy_neighbors == 4)):
                        # Simular Push
                        push_moves = get_push_pull_moves(board, (row, col), (enemy_r, enemy_c))
                        for pr, pc in zip(*np.where(push_moves == 2)):
                            new_board = copy.deepcopy(board)
                            push_piece(new_board, (pr, pc), (row, col), (enemy_r, enemy_c))
                            possible_moves.append((new_board, moves - 2, turn))
                        
                        # Simular Pull
                        pull_moves = get_push_pull_moves(board, (enemy_r, enemy_c), (row, col))
                        for pr, pc in zip(*np.where(pull_moves == 3)):
                            new_board = copy.deepcopy(board)
                            pull_piece(new_board, (pr, pc), (row, col), (enemy_r, enemy_c))
                            possible_moves.append((new_board, moves - 2, turn))

    # Incluir opción de pasar turno (si aplica)
    if moves == 4:
        _, new_turn, winner = skip_turn(moves, board, turn)
        if winner is None:  # Solo agregar si el juego no termina
            possible_moves.append((board, 4, new_turn))

    return possible_moves


from moving import weights

def evaluate_board(board, turn):
    """
    Evalúa el estado del tablero desde la perspectiva del jugador actual.
    Retorna un puntaje numérico donde valores positivos favorecen al jugador actual.
    """
    team = TEAM1 if turn == 1 else TEAM2
    opponent = TEAM2 if turn == 1 else TEAM1

    score = 0

    # 1. Sumar el peso de las piezas de cada equipo
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row, col]
            if piece in team:
                score += weights[piece]
            elif piece in opponent:
                score -= weights[piece]

    # 2. Proximidad de conejos al objetivo
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row, col]
            if piece == 1:  # Conejo dorado
                score += 7 - row  # Más cerca a la fila final, más puntos
            elif piece == 7:  # Conejo plateado
                score -= row  # Más cerca a la fila inicial, más puntos

    # 3. Control de trampas
    for trap in traps:
        trap_row, trap_col = trap
        if board[trap_row, trap_col] in team:
            score += 5  # Controlar una trampa es bueno
        elif board[trap_row, trap_col] in opponent:
            score -= 5  # Si el oponente controla la trampa

    # 4. Movilidad
    team_moves = 0
    opponent_moves = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row, col]
            if piece in team:
                team_moves += np.count_nonzero(get_valit_moves(board, (row, col)))
            elif piece in opponent:
                opponent_moves += np.count_nonzero(get_valit_moves(board, (row, col)))
    score += (team_moves - opponent_moves) * 0.5  # Movilidad tiene menor peso

    return score



from victories import check_Victories
def alpha_beta(board, depth, alpha, beta, maximizing_player, turn, moves):
    if depth == 0 or check_Victories(board):
        return evaluate_board(board, turn), []

    best_sequence = []  # Para almacenar la secuencia de movimientos
    if maximizing_player:
        max_eval = float('-inf')
        for new_board, new_moves, new_turn in generate_moves(board, turn, moves):
            eval, sequence = alpha_beta(new_board, depth - 1, alpha, beta, False, new_turn, new_moves)
            if eval > max_eval:
                max_eval = eval
                best_sequence = [new_board] + sequence  # Agregar el nuevo tablero a la secuencia
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_sequence
    else:
        min_eval = float('inf')
        for new_board, new_moves, new_turn in generate_moves(board, turn, moves):
            eval, sequence = alpha_beta(new_board, depth - 1, alpha, beta, True, new_turn, new_moves)
            if eval < min_eval:
                min_eval = eval
                best_sequence = [new_board] + sequence  # Agregar el nuevo tablero a la secuencia
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_sequence



# Tablero inicial
# board = np.array([
#     [1, 2, 3, 3, 4, 4, 5, 5],
#     [6, 6, 6, 6, 6, 6, 6, 6],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [7, 7, 7, 7, 7, 7, 7, 7],
#     [8, 8, 9, 9, 10, 10, 11, 12]
# ])

# # Corre el algoritmo alfa-beta
# score, best_sequence = alpha_beta(board, 2, float('-inf'), float('inf'), True, 1, 4)

# # Muestra resultados
# print("Mejor evaluación:", score)
# print("Secuencia de movimientos:")
# for i, seq_board in enumerate(best_sequence):
#     print(f"Movimiento {i + 1}:\n{seq_board}")
