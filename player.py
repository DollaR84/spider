"""
Player for spider.

Created on 27.11.2018

@author: Ruslan Dolovanyuk

"""

import enum

import checker

from constants import Colors

import pygame


Actions = enum.Enum('Actions', 'ChangeZoneUp ChangeZoneDown ChangeRowUp ChangeRowDown ChangeCardUp ChangeCardDown Take')


class Player:
    """Player class for spider."""

    def __init__(self, board, speech, phrases):
        """Initialize player class."""
        self.board = board
        self.speech = speech
        self.phrases = phrases
        self.color = Colors.BLUE
        self.__actions = [self.__change_zone, self.__change_row, self.__change_card, self.__take]

    def reset(self):
        """Reset current variables."""
        self.current_zone = 0
        self.__took = False
        self.take_card = None

    def draw(self):
        """Draw method for player."""
        zone = self.board.zones[self.current_zone]
        if zone.if_empty():
            left, top = zone.get_coord_zero(zone.current_row)
        else:
            left, top = zone.get_coord_card(zone.current_row, zone.current_card)
        pygame.draw.rect(zone.zone, self.color, (left, top, self.board.card_x, self.board.card_y), 1)

    def speak(self):
        """Speak information for moving cell."""
        name = self.phrases[self.board.zones[self.current_zone].NAME]
        row = ''
        if self.board.zones[self.current_zone].if_rows:
            row = self.phrases['column'] + ' ' + str(self.board.zones[self.current_zone].current_row + 1)
        self.speech.speak(' '.join((name, row)))
        self.__speak_card()

    def __speak_card(self, card=None):
        """Speak additionaly information for card."""
        if card is None:
            if not self.board.zones[self.current_zone].if_empty():
                card = self.board.zones[self.current_zone].get_card(self.board.zones[self.current_zone].current_card)
        if self.board.zones[self.current_zone].if_empty() and card is None:
            self.speech.speak(self.phrases['empty'])
        else:
            if card.status:
                if 52 == self.board.deck_count:
                    rate = str(card.rate_index) if 1 < card.rate_index < 11 else self.phrases[card.rate]
                else:
                    rate = str(card.rate_index) if card.rate_index < 11 else self.phrases[card.rate]
                    if 'ace' == card.rate:
                        rate = self.phrases[card.rate]
                self.speech.speak(' '.join((rate, self.phrases[card.suit])))
            else:
                self.speech.speak(self.phrases['close'])

    def actions(self, action):
        """Run actions in zones."""
        zone = self.board.zones[self.current_zone]
        for method_action in self.__actions:
            method_action(action, zone)

    def __change_zone(self, action, zone):
        """Change zone up or down."""
        if Actions.ChangeZoneUp == action:
            if 2 == self.current_zone:
                self.current_zone = 0
            else:
                self.current_zone += 1
            self.speak()
        elif Actions.ChangeZoneDown == action:
            if 0 == self.current_zone:
                self.current_zone = 2
            else:
                self.current_zone -= 1
            self.speak()

    def __change_row(self, action, zone):
        """Change row in zone up or down."""
        if Actions.ChangeRowUp == action:
            if zone.if_rows:
                if len(zone.rows) == zone.current_row + 1:
                    self.speech.speak(self.phrases['border'])
                    self.__speak_card()
                else:
                    zone.current_row += 1
                    zone.current_card = -1
                    self.speak()
        elif Actions.ChangeRowDown == action:
            if zone.if_rows:
                if 0 == zone.current_row:
                    self.speech.speak(self.phrases['border'])
                    self.__speak_card()
                else:
                    zone.current_row -= 1
                    zone.current_card = -1
                    self.speak()

    def __change_card(self, action, zone):
        """Change card in zone row up or down."""
        if Actions.ChangeCardUp == action and 2 == self.current_zone:
            if not zone.if_empty():
                if zone.get_card(0) == zone.get_card(zone.current_card):
                    self.speech.speak(self.phrases['border'])
                    self.__speak_card()
                elif zone.get_card(zone.current_card - 1).status:
                    zone.current_card -= 1
                    self.speak()
                else:
                    self.speech.speak(self.phrases['close'])
                    self.__speak_card()
        elif Actions.ChangeCardDown == action and 2 == self.current_zone:
            if not zone.if_empty():
                if zone.get_card(-1) == zone.get_card(zone.current_card):
                    self.speech.speak(self.phrases['border'])
                    self.__speak_card()
                else:
                    zone.current_card += 1
                    self.speak()

    def __take(self, action, zone):
        """Took or put card in zone row."""
        if Actions.Take == action:
            result_deck = self.__drop_deck(action, zone)
            if not result_deck:
                if zone.if_empty() and not self.__took:
                    return
                if self.__took:
                    if 'columns' == zone.NAME:
                        result = self.board.zones[2].take(self.__take_cards, self.__take_cards_list)
                        if result and len(self.__take_cards_list) > 0:
                            self.__open_card(self.__take_cards_list[-1])
                    self.__took = False
                    self.take_card.take = False
                    self.__drops()
                else:
                    cards = zone.rows[zone.current_row] if zone.if_rows else zone.cards
                    card = zone.get_card(zone.current_card)
                    self.__take_cards = cards[cards.index(card):]
                    if checker.equal_suits(self.__take_cards) and checker.rate_down(self.__take_cards):
                        self.__take_cards_list = cards
                        self.__took = True
                        self.take_card = card
                        self.take_card.take = True
                self.board.sounds.play('take')
                self.__speak_card()

    def __drop_deck(self, action, zone):
        """Dropped cards from deck."""
        if 0 == self.current_zone:
            if zone.if_empty():
                self.__speak_card()
                return True
            for row in self.board.zones[2].rows:
                row.append(self.board.zones[0].cards.pop())
                self.__open_card(row[-1])
            self.__speak_card()
            return True
        return False

    def __open_card(self, card, open_flag=True):
        """Open card or close if open_flag = False."""
        card.status = open_flag
        self.board.sounds.play('open')
        if open_flag:
            self.__speak_card(card)

    def __drops(self):
        """Dropped cards from zone in house."""
        
