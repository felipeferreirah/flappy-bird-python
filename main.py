import pygame
import random
import socket
from configs import HOST, PORT

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.coin import Coin
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.object import Object
from objects.score import Score


pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False
selected_time = 3300
stuning_point = False
assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()



def create_sprites_and_return_more():
    Background(0, sprites)
    Background(1, sprites)

    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(sprites), GameStartMessage(sprites), Score(sprites)


bird, game_start_message, score = create_sprites_and_return_more()

def add_column_coin():
    return Column(sprites), Coin(sprites)




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            column, coin = add_column_coin()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                # Object('mark', 4, sprites)
                gamestarted = True
                game_start_message.kill()
                pygame.time.set_timer(column_create_event, selected_time)

            if event.key == pygame.K_ESCAPE and gameover:
                gameover = False
                gamestarted = False
                sprites.empty()
                bird, game_start_message, score = create_sprites_and_return_more()

            if event.key == pygame.K_SPACE and gamestarted and not gameover:
                bird.handle_event(event)

    sprites.draw(screen)

    if not gamestarted and not gameover:
        assets.play_audio('intro')

    if gamestarted and not gameover:
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        assets.stop_audio('intro')
        assets.play_audio('loose')
        GameOverMessage(sprites)
        gameover = True
        gamestarted = False
        pygame.time.set_timer(column_create_event, 0)

    if bird.check_collision_coin(sprites) and not gameover:
        assets.play_audio('coin')

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audio('point')

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()
