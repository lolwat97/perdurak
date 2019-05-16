import itertools
import random
from enum import Enum

class CardSuit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3


class CardRank(Enum):
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return str(self.suit) + ' of ' + str(self.rank)


class Deck:
    def __init__(self, fullDeck = True):
        self.cards = self.shuffleCards(fullDeck)
        self.trump = self.cards.pop()

    def shuffleCards(self, fullDeck):
        if fullDeck:
            cardRange = range(2, 15)
        else:
            cardRange = range(6, 15)

        deck = [Card(x, y) for x, y in itertools.product(cardRange, CardSuit)]
        random.shuffle(deck)
        
        return deck

class PerdurakState:
    def __init__(self, humanPlayers = True, players = 4):
        self.substates = list()
        self.deck = Deck(fullDeck = True)
        if humanPlayers:
            self.fillWithPlayers(players)

    def fillWithPlayers(self, players = 4):
        self.substates = [PerdurakPlayerSubState() for x in range(players)]


class PerdurakSubState:
    def __init__(self):
        self.cards = list()
        self.isActive = False


class PerdurakPlayerSubState(PerdurakSubState):
    def __init__(self):
        PerdurakSubState.__init__(self)
        self.isPlayer = True


class PerdurakComputerSubState(PerdurakSubState):
    def __init__(self):
        PerdurakSubState.__init__(self)
        self.isPlayer = False


class PerdurakScreen:
    def __init__(self, screenParams):
        width, height = screenParams
        self.width = width
        self.height = height

    def draw(self, state):
        self.drawTrump(state)

    def drawTrump(self, state):
        print(state.deck.trump)



class PerdurakApp:
    def __init__(self, screenParams = (50, 50)):
        self.perdurakScreen = PerdurakScreen(screenParams)
        self.perdurakState = PerdurakState(humanPlayers = True, players = 3)

    def run(self):
        self.perdurakScreen.draw(self.perdurakState)
