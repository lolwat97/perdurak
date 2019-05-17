import itertools
import random

from cards import CardSuit, CardRank, Card


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
        self.cards.sort()


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
        for card in state.substates[playerNumber].cards:
            print(card)



class PerdurakApp:
    def __init__(self, screenParams = (50, 50)):
        self.perdurakScreen = PerdurakScreen(screenParams)
        self.perdurakState = PerdurakState(humanPlayers = True, players = 3)

    def run(self):
        self.perdurakState.dealCards(6)
        self.perdurakScreen.draw(self.perdurakState)
