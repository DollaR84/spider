"""
Module contain functions with check rules for playing cards.

Created on 26.10.2018

@author: Ruslan Dolovanyuk

"""

from constants import Cards


def change_color_suit(card1, card2):
    """Check change suit two cards."""
    if card1.suit in Cards.black_suits:
        return True if card2.suit in Cards.red_suits else False
    else:
        return True if card2.suit in Cards.black_suits else False


def equal_suit(card1, card2):
    """Check equal suit two cards."""
    return True if card1.suit == card2.suit else False


def change_color_suits(cards):
    """Check change suits cards."""
    for index, card in enumerate(cards):
        if (len(cards) - 1) > index:
            if not change_color_suit(card, cards[index + 1]):
                return False
    return True


def equal_suits(cards):
    """Check equal suits cards."""
    for index, card in enumerate(cards):
        if (len(cards) - 1) > index:
            if not equal_suit(card, cards[index + 1]):
                return False
    return True


def rate_down(cards):
    """Check down rate index cards."""
    for index, card in enumerate(cards):
        if (len(cards) - 1) > index:
            if cards[index + 1].rate_index != card.rate_index - 1:
                return False
    return True


def rate_up(cards):
    """Check up rate index cards."""
    for index, card in enumerate(cards):
        if (len(cards) - 1) > index:
            if cards[index + 1].rate_index != card.rate_index + 1:
                return False
    return True
