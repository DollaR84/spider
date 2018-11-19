"""
Main module for running spider game.

Created on 16.11.2018

@author: Ruslan Dolovanyuk

"""

import pickle
import random
import time

import pygame

from configparser import ConfigParser

from audio import Music
from audio import Sound

from board import Board

from constants import Colors

from player import Actions
from player import Player

from speech import Speech


class Game:
    """Main running class for game."""

    def __init__(self):
        """Initialize running class."""
        self.config = ConfigParser()
        self.config.read('settings.ini')
        self.size_x = self.config.getint('screen', 'size_x')
        self.size_y = self.config.getint('screen', 'size_y')

        with open('languages.dat', 'rb') as lang_file:
            self.phrases = pickle.load(lang_file)[self.config.get('total', 'language')]

        self.speech = Speech(self.config)
        self.speech.speak(self.phrases['start'])

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption(self.phrases['title'])

        self.music = Music(self.config.getfloat('audio', 'music_volume'))
        self.sounds = Sound(self.config.getfloat('audio', 'sound_volume'))

        self.board = Board(self.config, self.screen, self.sounds)
        self.player = Player(self.board, self.speech, self.phrases)
        self.game_over = True
        self.win = False

        self.STOPPED_PLAYING = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.STOPPED_PLAYING)
        self.fontObj = pygame.font.SysFont('arial', 50)
        self.clock = pygame.time.Clock()

        random.seed()
        self.music_play()
        self.new_game()

    def mainloop(self):
        """Run main loop game."""
        self.running = True
        while self.running:
            self.handle_events()
            self.draw()

            self.clock.tick(15)
            pygame.display.flip()

        self.speech.speak(self.phrases['finish'])
        self.speech.finish()
        pygame.quit()

    def handle_events(self):
        """Check all game events."""
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                self.running = False
            if self.STOPPED_PLAYING == event.type:
                self.music_play()
            elif pygame.KEYDOWN == event.type:
                if pygame.K_ESCAPE == event.key:
                    self.running = False
                elif pygame.K_F1 == event.key:
                    self.help()
                elif pygame.K_F2 == event.key:
                    self.turn_music()
                elif pygame.K_F3 == event.key:
                    self.change_level()
                elif pygame.K_F4 == event.key:
                    self.change_deck()
                elif pygame.K_F5 == event.key:
                    self.new_game()
                elif pygame.K_F9 == event.key:
                    self.change_language()
                elif pygame.K_TAB == event.key and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeZoneDown)
                elif pygame.K_TAB == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeZoneUp)
                elif pygame.K_LEFT == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeRowDown)
                elif pygame.K_RIGHT == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeRowUp)
                elif pygame.K_UP == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeCardUp)
                elif pygame.K_DOWN == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeCardDown)
                elif pygame.K_SPACE == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.Take)
                        self.check_win()

    def draw(self):
        """Main draw function."""
        self.screen.fill(Colors.DARKGREEN)
        self.board.draw()
        if self.game_over:
            if self.win:
                textSurfaceObj = self.fontObj.render(self.phrases['win'], True, Colors.GREEN)
            else:
                textSurfaceObj = self.fontObj.render(self.phrases['game_over'], True, Colors.RED)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (self.size_x//2, self.size_y//2)
            self.screen.blit(textSurfaceObj, textRectObj)
        else:
            self.player.draw()

    def music_play(self):
        """Change music play."""
        if self.config.getboolean('audio', 'music'):
            name = random.choice(self.music.get_music_names())
            self.music.play(name)

    def check_win(self):
        """Check win game."""
        all_kings = 0
        for row in self.board.zones[1].rows:
            if row and 'king' == row[-1].rate:
                all_kings += 1
        if 8 == all_kings:
            self.game_over = True
            self.win = True
            self.speech.speak(self.phrases['win'])

    def new_game(self):
        """Start new game."""
        self.speech.speak(self.phrases['new_game'])
        self.game_over = False
        self.win = False
        self.board.create_deck()
        self.board.clear_zones()
        self.board.distribution()
        self.player.reset()
        self.player.speak()

    def help(self):
        """Speak help for keys control game."""
        language = self.config.get('total', 'language')
        with open('help.dat', 'rb') as help_file:
            data = pickle.load(help_file)
            for line in [line for line in data[language] if '\n' != line]:
                self.speech.speak(line)
                time.sleep(0.1)

    def turn_music(self):
        """On or off music in game."""
        if self.config.getboolean('audio', 'music'):
            self.config.set('audio', 'music', 'false')
            pygame.mixer.music.stop()
            self.speech.speak(self.phrases['music_off'])
        else:
            self.config.set('audio', 'music', 'true')
            self.music_play()
            self.speech.speak(self.phrases['music_on'])
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)

    def change_level(self):
        """Change level: begin, middle, hard."""
        if 'begin' == self.config.get('board', 'level'):
            self.config.set('board', 'level', 'middle')
            self.speech.speak(self.phrases['middle'])
        elif 'middle' == self.config.get('board', 'level'):
            self.config.set('board', 'level', 'hard')
            self.speech.speak(self.phrases['hard'])
        else:
            self.config.set('board', 'level', 'begin')
            self.speech.speak(self.phrases['begin'])
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)

    def change_deck(self):
        """Change deck on game: 52 or 36."""
        if 'half' == self.config.get('board', 'deck'):
            self.config.set('board', 'deck', 'full')
            self.speech.speak(self.phrases['52_cards'])
        else:
            self.config.set('board', 'deck', 'half')
            self.speech.speak(self.phrases['36_cards'])
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)

    def change_language(self):
        """Change language for phrases."""
        if 'ru' == self.config.get('total', 'language'):
            self.config.set('total', 'language', 'en')
            with open('languages.dat', 'rb') as lang_file:
                self.phrases = pickle.load(lang_file)['en']
        else:
            self.config.set('total', 'language', 'ru')
            with open('languages.dat', 'rb') as lang_file:
                self.phrases = pickle.load(lang_file)['ru']
        self.player.phrases = self.phrases
        self.speech.speak(self.phrases['language'])
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)
