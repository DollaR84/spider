"""
Zones module for spider.

Created on 27.11.2018

@author: Ruslan Dolovanyuk

"""

from constants import Colors

import pygame


class ZoneBase:
    """Base zone class for spider."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize base class."""
        self.LEFT = left
        self.TOP = top
        self.card_size = card_size
        self.OFFSET = offset
        self.OFFSET_COLS = offset_cols
        self.color = Colors.YELLOW
        self.offset_zone = (self.LEFT, self.TOP)

    def clear(self):
        """Clear variable for new game."""
        self.current_row = 0
        self.current_card = -1


class ZoneDeck(ZoneBase):
    """Deck zone class for solitaires."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize deck class."""
        super().__init__(left, top, card_size, offset[0], offset_cols)
        self.NAME = 'deck'
        self.if_rows = False
        self.WIDTH = 2 * offset_cols + card_size[0] + 51 * offset[0]
        self.HEIGHT = 2 * offset_cols + card_size[1] + 51 * offset[0]
        self.zone = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.cards = []

    def draw(self, screen):
        """Draw zone on board."""
        left, top = self.get_coord_zero(0)
        self.zone.fill(Colors.DARKGREEN)
        pygame.draw.rect(self.zone, self.color, (left, top, self.card_size[0], self.card_size[1]), 1)
        for index, card in enumerate(self.cards):
            offset = self.get_coord_card(0, index)
            card.draw(self.zone, offset)
        screen.blit(self.zone, self.offset_zone)

    def get_coord_zero(self, index):
        """Return coord x and y empty row."""
        return (self.OFFSET_COLS, self.HEIGHT - self.OFFSET_COLS - self.card_size[1])

    def get_coord_card(self, row_index, index):
        """Return coord x and y card in row stack."""
        return (self.OFFSET_COLS + index * self.OFFSET, self.HEIGHT - self.OFFSET_COLS - self.card_size[1] - index * self.OFFSET)

    def clear(self):
        """Clear cards stack."""
        super().clear()
        self.cards.clear()

    def if_empty(self):
        """Check stack cards of empty."""
        return True if not self.cards else False

    def get_card(self, index):
        """Return card in current row for index."""
        try:
            result = self.cards[index]
        except:
            result = None
        finally:
            return result


class ZoneHouse(ZoneBase):
    """House zone class for solitaires."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize house class."""
        super().__init__(left, top, card_size, offset[0], offset_cols)
        self.NAME = 'house'
        self.if_rows = True
        self.WIDTH = 9 * offset_cols + 8 * card_size[0] + 8 * 12 * offset[0]
        self.HEIGHT = 2 * offset_cols + card_size[1] + 51 * offset[0]
        self.zone = pygame.Surface((self.WIDTH, self.HEIGHT))

        self.rows = []
        for _ in range(8):
            self.rows.append([])

    def draw(self, screen):
        """Draw zone on board."""
        self.zone.fill(Colors.DARKGREEN)
        for row_index, row in enumerate(self.rows):
            left, top = self.get_coord_zero(row_index)
            pygame.draw.rect(self.zone, self.color, (left, top, self.card_size[0], self.card_size[1]), 1)
            for index, card in enumerate(row):
                offset = self.get_coord_card(row_index, index)
                card.draw(self.zone, offset)
        screen.blit(self.zone, self.offset_zone)

    def get_coord_zero(self, index):
        """Return coord x and y empty row."""
        return (self.OFFSET_COLS + index * (self.card_size[0] + self.OFFSET_COLS), self.HEIGHT - self.OFFSET_COLS - self.card_size[1])

    def get_coord_card(self, row_index, index):
        """Return coord x and y card in row stack."""
        return (self.OFFSET_COLS + row_index * (self.card_size[0] + self.OFFSET_COLS) + index * self.OFFSET, self.HEIGHT - self.OFFSET_COLS - self.card_size[1] - index * self.OFFSET)

    def clear(self):
        """Clear cards stack."""
        super().clear()
        for row in self.rows:
            row.clear()

    def if_empty(self):
        """Check stack cards of empty."""
        return True if not self.rows[self.current_row] else False

    def get_card(self, index):
        """Return card in current row for index."""
        try:
            result = self.rows[self.current_row][index]
        except:
            result = None
        finally:
            return result


class ZoneColumns(ZoneBase):
    """Columns zone class for solitaires."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize columns class."""
        super().__init__(left, top, card_size, offset[0], offset_cols)
        self.NAME = 'columns'
        self.if_rows = True
        self.OFFSET_OPEN = offset[1]
        self.WIDTH = 11 * offset_cols + 10 * card_size[0] + 10 * 6 * offset[0]
        self.HEIGHT = 2 * offset_cols + card_size[1] + 7 * offset[0] + 12 * offset[1]
        self.zone = pygame.Surface((self.WIDTH, self.HEIGHT))

        self.rows = []
        for _ in range(10):
            self.rows.append([])

    def draw(self, screen):
        """Draw zone on board."""
        self.zone.fill(Colors.DARKGREEN)
        for row_index, row in enumerate(self.rows):
            left, top = self.get_coord_zero(row_index)
            pygame.draw.rect(self.zone, self.color, (left, top, self.card_size[0], self.card_size[1]), 1)
            for index, card in enumerate(row):
                offset = self.get_coord_card(row_index, index)
                card.draw(self.zone, offset)
        screen.blit(self.zone, self.offset_zone)

    def get_coord_zero(self, index):
        """Return coord x and y empty row."""
        return (self.OFFSET_COLS + index * (self.card_size[0] + self.OFFSET_COLS), self.OFFSET_COLS)

    def get_coord_card(self, row_index, index):
        """Return coord x and y card in row stack."""
        for index_first_open, card in enumerate(self.rows[row_index]):
            if card.status:
                break
        offset_close_cards = index_first_open * self.OFFSET
        if self.rows[row_index][index].status:
            offset = (self.OFFSET_COLS + row_index * (self.card_size[0] + self.OFFSET_COLS), self.OFFSET_COLS + offset_close_cards + (index - index_first_open) * self.OFFSET_OPEN)
        else:
            offset = (self.OFFSET_COLS + row_index * (self.card_size[0] + self.OFFSET_COLS), self.OFFSET_COLS + index * self.OFFSET)
        return offset

    def clear(self):
        """Clear cards stack."""
        super().clear()
        for row in self.rows:
            row.clear()

    def if_empty(self):
        """Check stack cards of empty."""
        return True if not self.rows[self.current_row] else False

    def get_card(self, index):
        """Return card in current row for index."""
        try:
            result = self.rows[self.current_row][index]
        except:
            result = None
        finally:
            return result

    def take(self, cards, old_list):
        """Check take card for put row."""
        if self.if_empty():
            for card in cards:
                self.rows[self.current_row].append(card)
                old_list.remove(card)
            return True
        elif cards[0].rate_index + 1 == self.get_card(-1).rate_index:
            for card in cards:
                self.rows[self.current_row].append(card)
                old_list.remove(card)
            return True
        return False


def get_zones():
    """Return all zones classes."""
    return (ZoneDeck, ZoneHouse, ZoneColumns)
