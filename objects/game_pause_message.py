import pygame.sprite

import assets
import configs
from layer import Layer


class GamePauseMessage(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = pygame.transform.scale(assets.get_sprite("pause-game"),
                                            (configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(*groups)

    # def update(self):
