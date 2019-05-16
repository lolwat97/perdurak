import itertools
import random
from enum import Enum

class CardSuit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3

    def __str__(self):
        return self.name


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


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return str(self.suit) + ' OF ' + str(self.rank)


class Deck:
    def __init__(self, fullDeck = True):
        self.cards = self.shuffleCards(fullDeck)
        self.trump = self.cards.pop()

    def shuffleCards(self, fullDeck):
        if fullDeck:
            cardRange = range(2, 15)
        else:
            cardRange = range(6, 15)

        deck = [Card(x, y) for x, y in itertools.product(CardRank, CardSuit)]
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

    def dealCards(self, cardsEach = 6):
        for substate in self.substates:
            substate.takeCard(self.deck, cardsEach)


class PerdurakSubState:
    def __init__(self):
        self.cards = list()
        self.isActive = False

    def takeCard(self, deck, number = 1):
        for i in range(number):
            self.cards.append(deck.cards.pop())


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
        self.drawPlayerCards(state, 0)

    def drawTrump(self, state):
        print(state.deck.trump)

    def drawPlayerCards(self, state, playerNumber):
        for card in state.substates[playerNumber].cards.sort():
            print(card)



class PerdurakApp:
    def __init__(self, screenParams = (50, 50)):
        self.perdurakScreen = PerdurakScreen(screenParams)
        self.perdurakState = PerdurakState(humanPlayers = True, players = 3)

    def run(self):
        self.perdurakState.dealCards(6)
        self.perdurakScreen.draw(self.perdurakState)
