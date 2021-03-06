"""
Sound and music module for solitaires.

Created on 04.09.2018

@author: Ruslan Dolovanyuk

"""

import io
import time

import loader

import pygame


class Sound:
    """Sound class for solitaires."""

    def __init__(self, volume):
        """Initialize sound class."""
        self.__sounds = loader.sounds(volume)

    def get_sound_names(self):
        """Return names all sounds effects."""
        return list(self.__sounds.keys())

    def play(self, name):
        """Play sound by name."""
        self.__sounds[name].play()


class Music:
    """Music class for solitaires."""

    def __init__(self, volume):
        """Initialize music class."""
        self.__music = loader.music()
        pygame.mixer.music.set_volume(volume)

    def get_music_names(self):
        """Return names all musics in collect."""
        return list(self.__music.keys())

    def play(self, name):
        """Play music by name."""
        pygame.mixer.music.load(io.BytesIO(self.__music[name]))
        pygame.mixer.music.play()


def test_sounds(sounds):
    """Test sound system."""
    for name in sounds.get_sound_names():
        sounds.play(name)
        time.sleep(2)


def test_music(music):
    """Test music system."""
    name = music.get_music_names()[0]
    music.play(name)
    while pygame.mixer.music.get_busy():
        time.sleep(1)


if '__main__' == __name__:
    pygame.mixer.init()
    sounds = Sound(1)
    music = Music(0.5)
    test_sounds(sounds)
    test_music(music)
    test_music(music)
