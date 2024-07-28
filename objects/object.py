import pygame.sprite
import random
import assets
import configs
from layer import Layer 

object_size = (70,70)


class Object(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.OBJECT
        self.images = [
            pygame.transform.scale(assets.get_sprite("boqueta"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (1)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (2)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (3)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (4)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (5)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (6)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (7)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (8)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (9)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (10)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (11)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (12)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (13)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (14)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (15)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (16)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (17)"), object_size),
            # pygame.transform.scale(assets.get_sprite("mumia (18)"), object_size),
        ]

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH + 100, random.uniform(50,300)))
        #
        # if random.uniform(0,10) <= 3:
        #     self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH + 100, random.uniform(50,300)))
        # else:
        #     self.rect = self.image.get_rect(topleft=(0,configs.SCREEN_HEIGHT - 60))

        self.mask = pygame.mask.from_surface(self.image)

        self.flap = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.current_frame = 0

        super().__init__(*groups)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            # Atualizar o tempo
            self.last_update = now

            # Atualizar a imagem
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.rect = self.image.get_rect(topleft=self.rect.topleft)  # Manter a posição

            # Atualizar máscara
            self.mask = pygame.mask.from_surface(self.image)

        self.rect.x -= 1
