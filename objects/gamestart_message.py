import pygame.sprite
import assets
import configs
from layer import Layer

class GameStartMessage(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite("message")
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

        # Configurações dos botões
        self.button_width = 150
        self.button_height = 50
        self.button_margin = 20

        # Criar 3 botões na horizontal
        self.buttons = [
            {'rect': pygame.Rect(
                configs.SCREEN_WIDTH / 2 - (self.button_width * 1.5) - self.button_margin,
                configs.SCREEN_HEIGHT / 2 - self.button_height / 2,
                self.button_width,
                self.button_height
            ), 'text': 'Play'},
            {'rect': pygame.Rect(
                configs.SCREEN_WIDTH / 2 - self.button_width / 2,
                configs.SCREEN_HEIGHT / 2 - self.button_height / 2,
                self.button_width,
                self.button_height
            ), 'text': 'Options'},
            {'rect': pygame.Rect(
                configs.SCREEN_WIDTH / 2 + self.button_width / 2 + self.button_margin,
                configs.SCREEN_HEIGHT / 2 - self.button_height / 2,
                self.button_width,
                self.button_height
            ), 'text': 'Quit'}
        ]
        self.font = pygame.font.SysFont(None, 36)
        self.visible = True
        super().__init__(*groups)


    def draw(self):
        if not self.visible:
            return

        # Desenhar o fundo do menu
        surface = pygame.display.get_surface()
        surface.blit(self.image, self.rect.topleft)

        # Desenhar os botões
        for button in self.buttons:
            pygame.draw.rect(surface, (0, 0, 0), button['rect'])
            button_text = self.font.render(button['text'], True, (255, 255, 255))
            surface.blit(button_text, (
                button['rect'].x + (self.button_width - button_text.get_width()) // 2,
                button['rect'].y + (self.button_height - button_text.get_height()) // 2
            ))

    def handle_event(self, events):
        if not self.visible:
            return

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for button in self.buttons:
                    if button['rect'].collidepoint(pos):
                        self.on_button_click(button['text'])

    def on_button_click(self, button_text):
        global game_started, running

        if button_text == 'Play':
            game_started = True
            self.visible = False
        elif button_text == 'Options':
            print('Abrir opções')
            # Lógica para abrir o menu de opções
        elif button_text == 'Quit':
            running = False
            pygame.quit()
            exit()

    def update(self):
        # O método update pode ser usado para lógica adicional
        # Mas para o propósito atual, ele pode ficar vazio
        pass
