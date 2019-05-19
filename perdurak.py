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

class Table:
    def __init__(self):
        self.cards = []

    def onOffenseCardPut(self, card):
        tableCard = TableCard.fromCard(card, isCovered = False)
        self.cards.append(tableCard)

    def onDefenseCardPut(self, card, coveredTableCard):
        tableCard = TableCard.fromCard(card, isCovered = True)
        self.cards.append(TableCard)
        coveredTableCard.isCovered = True

class TableCard(Card):
    def __init__(self, suit, rank, isCovered = False):
        Card.__init__(self, suit, rank)
        self.isCovered = isCovered

    def fromCard(card, isCovered = False):
        return TableCard(card.suit, card.rank, isCovered)

    def __str__(self):
        return str(self.suit) + ' OF ' + str(self.rank) + (" [X]" if self.isCovered else " [ ]")

class PerdurakState:
    def __init__(self, humanPlayers = True, players = 4):
        self.substates = list()
        self.deck = Deck(fullDeck = True)
        self.table = Table()
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

    def takeTableCards(self, table):
        for card in table.cards:
            self.cards.append(Card.fromTableCard(card))
            table.cards.remove(card)

    def putCard(self, table, card):
        table.onOffenseCardPut(card)
        self.cards.remove(card)

    def defendWithCard(self, table, card, coveredCard):
        table.onDefenseCardPut(card, coveredCard)
        self.cards.remove(card)


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
        for playerNumber in range(len(state.substates)):
            self.drawSpacer()
            self.drawPlayerCards(state, playerNumber)
        self.drawSpacer()
        self.drawTableCards(state)

    def drawTrump(self, state):
        print("The trump is")
        print(state.deck.trump)

    def drawPlayerCards(self, state, playerNumber):
        print("Player " + str(playerNumber) + "'s cards are")
        for card in state.substates[playerNumber].cards:
            print(card)

    def drawTableCards(self, state):
        print("Cards on table:")
        for card in state.table.cards:
            print(card)

    def drawSpacer(self):
        print("------------------")



class PerdurakApp:
    def __init__(self, screenParams = (50, 50)):
        self.perdurakScreen = PerdurakScreen(screenParams)
        self.perdurakState = PerdurakState(humanPlayers = True, players = 3)

    def run(self):
        self.perdurakState.dealCards(6)
        self.perdurakState.substates[0].putCard(self.perdurakState.table, self.perdurakState.substates[0].cards[0])
        self.perdurakState.substates[0].takeTableCards(self.perdurakState.table)
        self.perdurakScreen.draw(self.perdurakState)
