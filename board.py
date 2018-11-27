"""
Board for spider.

Created on 27.11.2018

@author: Ruslan Dolovanyuk

"""

import random
import time
import xml.etree.ElementTree as etree

from card import Card

from constants import Cards

import loader

from zones import get_zones


class Board:
    """Board class for spider."""

    def __init__(self, config, screen, sounds):
        """Initialize board class."""
        self.config = config
        self.screen = screen
        self.sounds = sounds

        CARD_ROW = 5
        CARD_COL = 13
        self.card_x = self.config.getint('board', 'card_x')
        self.card_y = self.config.getint('board', 'card_y')

        self.deck = []
        etree.register_namespace("", "http://www.w3.org/2000/svg")
        etree.register_namespace("xlink", "http://www.w3.org/1999/xlink")
        self.svg = etree.parse('cards.svg')
        root = self.svg.getroot()
        viewBox = [float(param) for param in root.attrib['viewBox'].split(' ')]
        START_POS = (viewBox[0], viewBox[1])
        CARD_SIZE = (viewBox[2] / CARD_COL, viewBox[3] / CARD_ROW)
        prefix = "{http://www.w3.org/2000/svg}"
        cards_iter = root.iterfind('./' + prefix + 'g/')
        defs_iter = root.iterfind('./' + prefix + 'defs/')
        self.defs = {obj.attrib['id']: obj for obj in defs_iter}
        self.svg_cards = {card.attrib['id']: card for card in cards_iter}
        joker_addons = [elem for elem in self.svg_cards['joker_black'].findall('./') if prefix + 'g' == elem.tag]
        for addon in joker_addons:
            self.svg_cards['joker_red'].append(addon)
        self.textures = loader.textures(self.svg_cards, START_POS, CARD_SIZE, self.defs, self.card_x, self.card_y)

        self.create_zones()

    def create_deck(self):
        """Create all cards."""
        self.deck.clear()
        self.level = self.config.get('board', 'level')
        self.deck_count = 36 if 'half' == self.config.get('board', 'deck') else 52

        if 'hard' == self.level:
            suits = Cards.suits * 2
        elif ''middle' == self.level:
            suits = [Cards.black_suits[1]] * 4 + [Cards.red_suits[1]] * 4
        else:
            suits = [Cards.black_suits[1]] * 8

        for suit in suits:
            for rate in range(1, 14):
                if 36 == self.deck_count:
                    if 1 < rate < 6:
                        continue
                self.deck.append(Card(rate, suit, self.card_x, self.card_y, self.deck_count))

        for card in self.deck:
            card.tex_face = self.textures[card.tex_name]
            card.tex_back = self.textures['back']

        random.seed()
        random.shuffle(self.deck)

    def create_zones(self):
        """Create all gaming zones."""
        screen_x = self.config.getint('screen', 'size_x')
        offset_card_total = self.config.getint('board', 'offset_card_total')
        offset_card_open = self.config.getint('board', 'offset_card_open')
        offset_cols = self.config.getint('board', 'offset_cols')
        offset_card = (offset_card_total, offset_card_open)

        self.zones = []
        left = 0
        top = 0
        for index, zone in enumerate(get_zones()):
            self.zones.append(zone(left, top, (self.card_x, self.card_y), offset_card, offset_cols))
            if 0 == index:
                left += 2 * offset_cols + self.card_x + 51 * offset_card_total
            elif 1 == index:
                width = 11 * offset_cols + 10 * self.card_x + 10 * 6 * offset_card_total
                left = (screen_x - width) // 2
                top = 2 * offset_cols + self.card_y + 51 * offset_card_total

    def clear_zones(self):
        """Clear all zones card stack."""
        for zone in self.zones:
            zone.clear()

    def draw(self):
        """Draw method for board."""
        for zone in self.zones:
            zone.draw(self.screen)

    def distribution(self):
        """Distribution cards in new game."""
        while self.deck:
            card = self.deck.pop()
            card.status = False
            self.zones[0].cards.append(card)
            self.sounds.play('deal')
            time.sleep(0.05)

        row = 0
        for _ in range(54):
            self.zones[2].rows[row].append(self.zones[0].cards.pop())
            self.sounds.play('distrib')
            time.sleep(0.05)
            if row < len(self.zones[2].rows) - 1:
                row += 1
            else:
                row = 0

        for row in range(len(self.zones[2].rows)):
            self.zones[2].rows[row][-1].status = True
            self.sounds.play('open')
            time.sleep(0.05)
