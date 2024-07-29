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
from objects.game_pause_message import GamePauseMessage
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.object import Object
from objects.score import Score

# Inicializar o Pygame e configurar a tela
pygame.init()
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Configurações iniciais
column_create_event = pygame.USEREVENT
running = True
game_over = False
game_started = False
game_paused = False
selected_time = 3000
original_timer = selected_time  # Armazena o intervalo original do temporizador
special_mode = False

# Carregar assets e criar grupo de sprites
assets.load_sprites()
assets.load_audios()
sprites = pygame.sprite.LayeredUpdates()


def create_background_and_floor():
    """Cria e retorna as instâncias de fundo e chão."""
    back_a = Background(0, sprites)
    back_b = Background(1, sprites)
    floor_a = Floor(0, sprites)
    floor_b = Floor(1, sprites)
    return back_a, back_b, floor_a, floor_b


def create_menu_screen():
    """Configura a tela de menu (antes do jogo começar)."""
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    return Bird(sprites), GameStartMessage(sprites), Score(sprites)


def create_game_screen():
    """Configura a tela inicial do jogo."""
    back_a, back_b, floor_a, floor_b = create_background_and_floor()
    bird = Bird(sprites)
    game_start_message = GameStartMessage(sprites)
    score = Score(sprites)
    return bird, game_start_message, score, back_a, back_b, floor_a, floor_b


def create_column_and_coin():
    """Cria e retorna as instâncias de coluna e moeda."""
    return Column(sprites), Coin(sprites)  #, Object(sprites)


# Inicializar o jogo
bird, game_start_message, score, back_a, back_b, floor_a, floor_b = create_game_screen()


# column_init, coin_init = create_column_and_coin()


def handle_events():
    """Lida com eventos do Pygame."""
    global running, game_started, game_over, game_paused, column_create_event, bird

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == column_create_event and not game_paused:
            create_column_and_coin()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and game_paused:
                Object(sprites)
            if event.key == pygame.K_SPACE:
                if not game_started and not game_over:
                    start_game()
                elif game_started and not game_over:
                    bird.fly_event(event)
            elif event.key == pygame.K_ESCAPE:
                if game_over:
                    reset_game()
                elif game_started:
                    toggle_pause()
    return True


def start_game():
    """Inicia o jogo e configura o timer para criar colunas."""
    global game_started, game_over
    game_started = True
    game_start_message.kill()
    pygame.time.set_timer(column_create_event, selected_time)


def reset_game():
    """Reinicia o jogo após a tela de game over."""
    global game_started, game_over, game_paused, sprites, bird, game_start_message, score, back_a, back_b, floor_a, floor_b, special_mode
    game_over = False
    game_started = False
    game_paused = False
    special_mode = False
    sprites.empty()
    bird, game_start_message, score, back_a, back_b, floor_a, floor_b = create_game_screen()
    pygame.time.set_timer(column_create_event, selected_time)


def toggle_pause():
    """Alterna entre pausar e despausar o jogo."""
    global game_paused, original_timer, game_pause_message

    game_paused = not game_paused

    # Pausar ou retomar os objetos
    for sprite in sprites:
        if hasattr(sprite, 'pause'):
            sprite.pause()

    # Pausar ou retomar o temporizador
    if game_paused:
        pygame.time.set_timer(column_create_event, 0)
        assets.stop_audio("game")
        assets.play_audio("smw_pause")
        game_pause_message = GamePauseMessage(sprites)

    else:
        pygame.time.set_timer(column_create_event, original_timer)
        assets.play_audio("smw_pause")
        game_pause_message.kill()


def update_game():
    """Atualiza o estado do jogo e verifica colisões."""
    global game_over, game_over_message, special_mode, game_pause_message
    if bird.check_collision(sprites) and not game_over and not special_mode:
        assets.stop_audio('game')
        assets.play_audio('loose')
        game_over_message = GameOverMessage(sprites)
        game_over = True
        pygame.time.set_timer(column_create_event, 0)

    if bird.check_collision_coin(sprites) and not game_over:
        score.value += 1
        assets.play_audio('coin')

    if bird.check_collision_object(sprites) and not game_over:
        score.value += 10
        # if score.value >= 3:
        # special_mode = True
        # bird.change_skin('red')
        # assets.stop_audio('game')
        #
        # assets.play_audio('monster')
        # assets.play_audio('rock')

        assets.play_audio('sinister-laugh')

    for sprite in sprites:
        if isinstance(sprite, Column) and sprite.is_passed():
            score.value += 1
            assets.play_audio('point')


def main():
    global game_started, game_over, special_mode
    pygame.display.set_caption('Flappy World')
    while running:

        if not handle_events():
            break

        if not game_started and not game_over:
            assets.play_audio('intro')
            assets.stop_audio('game')

        elif game_started and not game_over and not game_paused:
            if not special_mode:
                assets.play_audio('game')
            assets.stop_audio('intro')

            if not game_paused:
                sprites.update()

        update_game()
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(configs.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
