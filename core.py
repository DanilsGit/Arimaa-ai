import pygame
import numpy as np
from configs import WIDTH, HEIGHT, WHITE, SQ_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT
from draw_logic import create_board, draw_board, draw_pieces, draw_pass_turn_button, create_board_moviment, draw_possible_moves, draw_turn_moves

# Inicialización de pygame
pygame.init()

# Crear la ventana
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arimaa Game")

TEAM1 = [1,2,3,4,5,6]
TEAM2 = [7,8,9,10,11,12]
traps = [(2, 2), (2, 5), (5, 2), (5, 5)]
turn = 1 

def redraw_window(WIN, fall_in_trap, board, traps, matrix_moviment, turn, moves):
    board = fall_in_trap(board)
    WIN.fill(WHITE)
    draw_board(WIN, board, traps)
    draw_pieces(WIN, board)
    draw_possible_moves(WIN, matrix_moviment)
    draw_pass_turn_button(WIN)
    draw_turn_moves(WIN, turn, moves)
    return board

# Función principal del juego
def main():
    from moving import fall_in_trap, get_cell_from_mouse, skip_turn, click_controller_steps
    from IA import alpha_beta
    global turn
    global traps
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
            print(f"¡{winner} ha ganado!")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Verificar si se hizo clic en el botón "Pasar Turno"
                    pass_turn_button = pygame.Rect(WIDTH - BUTTON_WIDTH/2 - WIDTH/2, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
                    if pass_turn_button.collidepoint(mouse_pos):
                        moves, turn, winner = skip_turn(moves, board, turn)
                        continue
                    cell = get_cell_from_mouse(mouse_pos)
                    matrix_moviment, moves, selected_piece, board, piece_in_attack, piece_to_attack = click_controller_steps(matrix_moviment, cell, board, moves, selected_piece, piece_in_attack, piece_to_attack, turn)

        # redibujar el tablero antes de que la IA juegue
        board = redraw_window(WIN, fall_in_trap, board, traps, matrix_moviment, turn, moves)
        pygame.display.update()
        if (turn == 2):
            _, best_sequence = alpha_beta(board, 2, float('-inf'), float('inf'), True, 2, 4)
            for i, seq_board in enumerate(best_sequence):
                print(f"\n{seq_board}")
            for new_board in best_sequence:
                pygame.time.wait(100)
                pygame.display.update()
                board = redraw_window(WIN, fall_in_trap, new_board, traps, matrix_moviment, turn, moves)
                pygame.time.wait(100)
                pygame.display.update()
            turn = 1
            moves = 4
            continue

        if moves == 0:
            moves, turn, winner = skip_turn(moves, board, turn)
            continue

        # Redibujar el tablero
        board = redraw_window(WIN, fall_in_trap, board, traps, matrix_moviment, turn, moves)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
