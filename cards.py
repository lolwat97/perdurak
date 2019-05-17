from enum import Enum


class CardSuit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.value < other.value


class CardRank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.value < other.value


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return str(self.suit) + ' OF ' + str(self.rank)

    def __lt__(self, other):
        if (self.rank == other.rank):
            return (self.suit < other.suit)
        else:
            return (self.rank < other.rank)
