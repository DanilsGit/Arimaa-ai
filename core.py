import pygame
from configs import WIDTH, HEIGHT, WHITE, SQ_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT
from draw_logic import create_board, draw_board, draw_pieces, draw_pass_turn_button, create_board_moviment, draw_possible_moves, draw_turn_moves, draw_waiting_for_IA
from mensaje import show_winner_message
# Inicialización de pygame
pygame.init()

# Crear la ventana
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arimaa Game")

TEAM1 = [1,2,3,4,5,6]
TEAM2 = [7,8,9,10,11,12]
TRAPS = [(2, 2), (2, 5), (5, 2), (5, 5)]
turn = 1 

def redraw_window(WIN, fall_in_trap, board, TRAPS, matrix_moviment, turn, moves, moving_piece=None, moving_pos=None, moving_from=None):
    board = fall_in_trap(board)
    WIN.fill(WHITE)
    draw_board(WIN, board, TRAPS)

    # Tablero temporal para omitir la pieza en movimiento
    if moving_from:
        temp_board = [row.copy() for row in board]
        temp_board[moving_from[0]][moving_from[1]] = 0
        draw_pieces(WIN, temp_board)  # Dibuja sin la pieza en movimiento
    else:
        draw_pieces(WIN, board)

    # Dibuja la pieza en movimiento
    if moving_piece and moving_pos:
        WIN.blit(moving_piece, moving_pos)

    draw_possible_moves(WIN, matrix_moviment)
    draw_pass_turn_button(WIN)
    draw_turn_moves(WIN, turn, moves)
    return board



# Función principal del juego
def main():
    from moving import fall_in_trap, get_cell_from_mouse, skip_turn, click_controller_steps, applly_one_animated_move
    from IA2 import minimax
    global turn
    global TRAPS
    board = create_board()
    matrix_moviment = create_board_moviment()

    clock = pygame.time.Clock()
    run = True
    moves = 4  # El contador de acciones por turno
    selected_piece = None
    piece_in_attack = None
    piece_to_attack = None
    winner = None

    while run:
        clock.tick(60)

        if winner is not None:
            show_winner_message(winner)
            run = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    if (turn != 1):
                        continue
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Verificar si se hizo clic en el botón "Pasar Turno"
                    pass_turn_button = pygame.Rect(WIDTH - BUTTON_WIDTH/2 - WIDTH/2, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
                    if pass_turn_button.collidepoint(mouse_pos):
                        moves, turn, winner = skip_turn(moves, board, turn)
                        continue
                    cell = get_cell_from_mouse(mouse_pos)
                    matrix_moviment, moves, selected_piece, board, piece_in_attack, piece_to_attack = click_controller_steps(matrix_moviment, cell, board, moves, selected_piece, piece_in_attack, piece_to_attack, turn)

        # redibujar el tablero antes de que la IA juegue
        board = redraw_window(WIN, fall_in_trap, board, TRAPS, matrix_moviment, turn, moves)
        pygame.display.update()
        if (turn == 2):
            draw_waiting_for_IA(WIN)
            pygame.time.wait(800)
            pygame.display.update()
            result = minimax(board, 1, True)
            best_sequence = result["moves"]
            for move in best_sequence:
                board = applly_one_animated_move(board, move, WIN, matrix_moviment, turn, moves)
                board = redraw_window(WIN, fall_in_trap, board, TRAPS, matrix_moviment, turn, moves)    
            moves = 0

        if moves == 0:
            moves, turn, winner = skip_turn(moves, board, turn)
            continue

        # Redibujar el tablero
        board = redraw_window(WIN, fall_in_trap, board, TRAPS, matrix_moviment, turn, moves)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
