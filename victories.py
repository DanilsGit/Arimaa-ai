from configs import ROWS
from core import TEAM1, TEAM2

def check_Victories(board):
    # Verificar victoria por alcanzar el objetivo
    victory = check_victory_by_goal(board)
    if victory:
        winner = "Player 1" if victory == TEAM1 else "Player 2" if victory == TEAM2 else None
        print(f"¡{winner} ha ganado por alcanzar el objetivo!")
        return True

    # Verificar victoria por piezas inmovilizadas
    victory = check_victory_by_immobilization(board)
    if victory:
        winner = "Player 1" if victory == TEAM1 else "Player 2" if victory == TEAM2 else None
        print(f"¡{winner} ha ganado por inmovilización de piezas!")
        return True

    # Verificar victoria por ausencia de piezas
    victory = check_victory_by_no_pieces(board)
    if victory:
        winner = "Player 1" if victory == TEAM1 else "Player 2" if victory == TEAM2 else None
        print(f"¡{winner} ha ganado por eliminación de todas las piezas del oponente!")
        return True

    return None

def check_victory_by_goal(board):
    # Revisar si el conejo de TEAM1 llegó a la última fila
    if 1 in board[ROWS-1]:
        return TEAM1
    # Revisar si el conejo de TEAM2 llegó a la primera fila
    if 7 in board[0]:
        return TEAM2
    return None


def check_victory_by_immobilization(board):
    from moving import get_valit_moves  # Usar la función `get_valit_moves`

    def has_moves(team):
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row, col] in team:
                    valid_moves = get_valit_moves(board, (row, col))
                    if valid_moves.any():  # Si hay algún movimiento válido
                        return True
        return False

    # Verificar si todas las piezas de TEAM1 están inmovilizadas
    if not has_moves(TEAM1):
        return TEAM2

    # Verificar si todas las piezas de TEAM2 están inmovilizadas
    if not has_moves(TEAM2):
        return TEAM1

    return None



def check_victory_by_no_pieces(board):
    # Verificar si no quedan piezas de TEAM1
    team1_exists = any(piece in TEAM1 for row in board for piece in row)
    if not team1_exists:
        return TEAM2

    # Verificar si no quedan piezas de TEAM2
    team2_exists = any(piece in TEAM2 for row in board for piece in row)
    if not team2_exists:
        return TEAM1

    return None
