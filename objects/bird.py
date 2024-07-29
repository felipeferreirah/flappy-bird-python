import pygame.sprite
import assets
import configs
from layer import Layer
from objects.coin import Coin
from objects.column import Column
from objects.floor import Floor
from objects.object import Object


class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.PLAYER
        self.paused = False

        # Definindo os conjuntos de imagens
        self.skins = {
            'blue': self.skin_blue(),
            'red': self.skin_red(),  # Novo conjunto de imagens
            # Adicione mais conjuntos de imagens conforme necessário
        }

        # Definindo o conjunto de imagens atual
        self.current_skin = 'blue'
        self.images = self.skins[self.current_skin]

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(-50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.flap = 0

        super().__init__(*groups)

    def skin_blue(self):
        return [
            assets.get_sprite("bluebird-downflap"),
            assets.get_sprite("bluebird-midflap"),
            assets.get_sprite("bluebird-upflap"),
        ]

    def skin_red(self):
        return [
            assets.get_sprite("redbird-downflap"),
            assets.get_sprite("redbird-midflap"),
            assets.get_sprite("redbird-upflap"),
        ]

    def update(self):
        if not self.paused:
            self.images.insert(0, self.images.pop())
            self.image = self.images[0]

            self.flap += configs.GRAVITY
            self.rect.y += self.flap

            # Levar o bird da posição 0 (escondida) até a posição 50
            if self.rect.x <= 50:
                self.rect.x += 2

    def fly_event(self, event):
        if not self.paused:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.flap = 0
                self.flap -= 5
                assets.play_audio('wing')

    def check_collision(self, sprites):
        for sprite in sprites:
            if ((type(sprite) is Column or type(sprite) is Floor)
                    and sprite.mask.overlap(self.mask, (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y))
                    or self.rect.bottom < 0):
                return True
        return False

    def check_collision_coin(self, sprites):
        for sprite in sprites:
            if (type(sprite) is Coin) and sprite.mask.overlap(self.mask, (
            self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)):
                sprite.kill()
                return True
        return False

    def check_collision_object(self, sprites):
        for sprite in sprites:
            if (type(sprite) is Object) and sprite.mask.overlap(self.mask, (
            self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)):
                sprite.kill()
                return True
        return False

    def pause(self):
        self.paused = not self.paused

    def change_skin(self, new_skin):
        if new_skin in self.skins:
            self.current_skin = new_skin
            self.images = self.skins[new_skin]
            self.image = self.images[0]
