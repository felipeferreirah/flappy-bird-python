import os.path

import imageio
import pygame

sprites = {}
audios = {}  # Dicionário para armazenar os objetos pygame.mixer.Sound
channels = {}  # Dicionário para armazenar os canais pygame.mixer.Channel


def load_sprites():
    path = os.path.join("assets", "sprites")
    for file in os.listdir(path):
        sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))


def get_sprite(name):
    return sprites[name]


def load_audios():
    global audios
    path = os.path.join("assets", "audio")
    for file in os.listdir(path):
        audios[file.split('.')[0]] = pygame.mixer.Sound(os.path.join(path, file))
        if file == 'intro.mp3':
            audios[file.split('.')[0]].set_volume(0.1)

        if file == 'loose.mp3':
            audios[file.split('.')[0]].set_volume(0.1)

        if file == 'point.wav':
            audios[file.split('.')[0]].set_volume(0.4)

        if file == 'wing.wav':
            audios[file.split('.')[0]].set_volume(0.2)

        if file == 'coin.mp3':
            audios[file.split('.')[0]].set_volume(1)

def play_audio(name):
    global channels
    if name in channels:  # Verifica se já existe um canal para este som
        channels[name].play(audios[name])  # Reproduz no canal existente
    else:
        channel = pygame.mixer.Channel(len(channels))  # Cria um novo canal
        channels[name] = channel  # Associa o canal ao som no dicionário
        channel.play(audios[name])  # Reproduz o som no novo canal


def stop_audio(name):
    global channels
    if name in channels:  # Verifica se o som está associado a um canal
        channels[name].stop()  # Para a reprodução do som


def is_audio_playing(name):
    global channels
    if name in channels:  # Verifica se o som está associado a um canal
        return channels[name].get_busy()  # Verifica se o canal está ocupado (reproduzindo áudio)
    return False  # Retorna False se o som não estiver associado a nenhum canal
