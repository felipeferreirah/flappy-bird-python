import pygame.sprite
import assets
import configs
from layer import Layer


class Menu(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        # Carregar e escalar a imagem do menu
        self.image = pygame.transform.scale(assets.get_sprite("pause-game"),
                                            (configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.visible = False  # Controle de visibilidade do menu
        print('carregou')

        super().__init__(*groups)

    def update(self):
        if not self.visible:
            return
        # Atualize o menu aqui se necessário, por exemplo, animações ou verificações de estado

    def show(self):
        self.visible = True
        self.image = pygame.transform.scale(assets.get_sprite("pause-game"),
                                            (configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

    def hide(self):
        self.visible = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Lógica para lidar com o pressionamento da tecla ESC no menu
                print("Tecla ESC pressionada no menu")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse
                pos = event.pos
                if self.rect.collidepoint(pos):
                    print("Clique dentro do menu")
                    # Lógica para clicar no menu

