import tkinter as tk
from tkinter import messagebox
import pygame

def show_winner_message(winner):
    # Crear una nueva ventana de Tkinter
    root = tk.Tk()
    root.title("¡Juego Terminado!")  # Título de la ventana
    root.geometry("400x250")  # Tamaño de la ventana
    root.config(bg="#4C9D9B")  # Color de fondo de la ventana
    root.resizable(False, False)
    # Asegurarse de que la ventana se muestre centrada en la pantalla
    window_width = 400
    window_height = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Etiqueta para mostrar el mensaje
    label = tk.Label(root, text=f"¡{winner} ha ganado!", font=("Helvetica", 24, "bold"), bg="#4C9D9B", fg="white")
    label.pack(expand=True)  # Expandir la etiqueta para que se centre verticalmente y horizontalmente

    # Función para cerrar la ventana y el juego
    def close_game():
        pygame.quit()  # Cerrar la ventana del juego de Pygame
        root.destroy()  # Cerrar la ventana de Tkinter

    # Botón para cerrar la ventana y el juego
    button = tk.Button(root, text="Cerrar", command=close_game, font=("Helvetica", 14), bg="#FF6347", fg="white", relief="raised", bd=5)
    button.pack(pady=20)  # Agregar el botón con un poco de espacio abajo

    # Ejecutar el loop de la ventana de Tkinter
    root.mainloop() 




# Configuración inicial de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prueba del mensaje")


#para probar el mensaje XD
def main():
    run = True
    winner = None
    clock = pygame.time.Clock()

    while run:
        WIN.fill((0, 0, 0))  
        font = pygame.font.Font(None, 50)
        text = font.render("Presiona ESPACIO para mostrar el mensaje", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WIN.blit(text, text_rect)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    winner = "Jugador 1"
                    show_winner_message (winner)

    pygame.quit()

if __name__ == "__main__":
    main()