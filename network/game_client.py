import pygame
import socket
import threading
import time

# Configurações da tela
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FONT_SIZE = 36
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50


class GameClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = None
        self.response = ""
        self.status_message = "Clique em 'Conectar' para tentar se conectar"
        self.connected = False
        self.lock = threading.Lock()

    def connect_to_server(self):
        if not self.connected:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.port))
                self.connected = True
                self.status_message = "Conectado!"
                threading.Thread(target=self.receive_messages, daemon=True).start()
            except Exception as e:
                self.status_message = f"Erro ao conectar: {e}"
                print(f"Error connecting to server: {e}")

    def disconnect_from_server(self):
        if self.connected:
            try:
                self.client_socket.close()
                self.connected = False
                self.status_message = "Desconectado"
            except Exception as e:
                print(f"Error disconnecting: {e}")
                self.status_message = "Erro ao desconectar"

    def send_message(self, message):
        if self.connected:
            try:
                self.client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")
                self.connected = False
                self.status_message = "Desconectado"
        else:
            self.status_message = "Desconectado"

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.response = message
                else:
                    self.connected = False
                    self.status_message = "Desconectado"
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.connected = False
                self.status_message = "Desconectado"


def draw_button(screen, font, text, x, y, width, height):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, (100, 200, 255), button_rect)  # Hover color
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, (50, 150, 255), button_rect)  # Normal color

    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface,
                (x + (width // 2 - text_surface.get_width() // 2), y + (height // 2 - text_surface.get_height() // 2)))
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Client")
    font = pygame.font.Font(None, FONT_SIZE)
    client = GameClient()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the connect button
        if draw_button(screen, font, "Conectar", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                       SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 - 60, BUTTON_WIDTH, BUTTON_HEIGHT):
            client.connect_to_server()

        # Draw the disconnect button
        if draw_button(screen, font, "Desconectar", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                       SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 + 60, BUTTON_WIDTH, BUTTON_HEIGHT):
            client.disconnect_from_server()

        # Render the status message
        status_text = font.render(client.status_message, True, (255, 255, 255))
        screen.blit(status_text, (20, 20))

        # Render the response text
        response_text = font.render(client.response, True, (255, 255, 255))
        screen.blit(response_text, (20, 60))

        # Update the display
        pygame.display.flip()

        # Small delay to reduce CPU usage
        time.sleep(0.1)

    pygame.quit()


if __name__ == "__main__":
    main()
