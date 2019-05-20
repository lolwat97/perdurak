import itertools
import random

import readchar

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

        deck = [Card(y, x) for x, y in itertools.product(CardRank, CardSuit)]
        random.shuffle(deck)
        
        return deck

class Table:
    def __init__(self):
        self.cards = []

    def allCardsAreCovered(self):
        return all(card.isCovered is True for card in self.cards)

    def getUncoveredCardsNumber(self):
        return len(list(filter(lambda card: card.isCovered, self.cards)))

    def onOffenseCardPut(self, card):
        tableCard = TableCard.fromCard(card, isCovered = False)
        self.cards.append(tableCard)

    def onDefenseCardPut(self, card, coveredTableCard):
        tableCard = TableCard.fromCard(card, isCovered = True)
        self.cards.append(tableCard)
        coveredTableCard.isCovered = True

class TableCard(Card):
    def __init__(self, suit, rank, isCovered = False):
        Card.__init__(self, suit, rank)
        self.isCovered = isCovered

    def fromCard(card, isCovered = False):
        return TableCard(card.suit, card.rank, isCovered)

    def __str__(self):
        return str(self.rank) + ' OF ' + str(self.suit) + (" [X]" if self.isCovered else " [ ]")

class PerdurakState:
    def __init__(self, humanPlayers = True, players = 4):
        self.substates = list()
        self.deck = Deck(fullDeck = True)
        self.table = Table()
        self.tableChangeFlag = False
        self.switchFlag = False
        if humanPlayers:
            self.fillWithPlayers(players)

    def fillWithPlayers(self, players = 4):
        self.substates = [PerdurakPlayerSubState() for x in range(players)]

    def dealCards(self, cardsEach = 6):
        for substate in self.substates:
            substate.takeCard(self.deck, cardsEach)

    def topUpCards(self, cardsEach = 6):
        for substate in self.substates:
            substate.takeCard(self.deck, cardsEach - len(substate.cards))


class PerdurakSubState:
    def __init__(self):
        self.cards = list()
        self.isActive = False

    def takeCard(self, deck, number = 1):
        try:
            for i in range(number):
                self.cards.append(deck.cards.pop())
            self.cards.sort()
        except IndexError:
            pass

    def takeTableCards(self, table):
        self.cards.extend([Card.fromTableCard(card) for card in table.cards])
        table.cards = []

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

    def draw(self, state, actingPlayerNumber, isInOffense = False):
        self.drawCardsLeft(state)
        self.drawSpacer()
        self.drawTrump(state)
        self.drawSpacer()
        self.drawPlayerCards(state, actingPlayerNumber)
        self.drawSpacer()
        self.drawTableCards(state)
        if isInOffense:
            self.drawSpacer()
            self.drawValidOffenseCards(state, actingPlayerNumber)

    def drawCardsLeft(self, state):
        print(str(len(state.deck.cards)) + " cards left in the deck")

    def drawTrump(self, state):
        print("The trump is")
        print(state.deck.trump)

    def drawPlayerCards(self, state, playerNumber):
        print("Player " + str(playerNumber) + "'s cards are")
        for card in state.substates[playerNumber].cards:
            print(str(state.substates[playerNumber].cards.index(card)) + ": " + str(card))

    def drawTableCards(self, state):
        print("Cards on the table:")
        for card in state.table.cards:
            print(str(state.table.cards.index(card)) + ": " + str(card))

    def drawSpacer(self):
        print("------------------")

    def drawValidDefenseCards(self, state, playerNumber, tableCardNumber):
        print("Valid defense cards")
        playerCards = state.substates[playerNumber].cards
        cards = MoveChecker.getValidDefenseCards(state.table.cards[tableCardNumber], state.deck.trump, playerCards)
        for card in cards:
            print(str(cards.index(card)) + ": " + str(card))

    def drawValidOffenseCards(self, state, playerNumber):
        print("Valid offense cards")
        playerCards = state.substates[playerNumber].cards
        cards = MoveChecker.getValidOffenseCards(state.table, state.deck.trump, playerCards)
        for card in cards:
            print(str(cards.index(card)) + ": " + str(card))


class MoveChecker:
    def getValidOffenseCards(table, trump, cards):
        return list(filter(lambda card: MoveChecker.checkOffenseCard(table, trump, card), cards))

    def getValidDefenseCards(coveredCard, trump, cards):
        return list(filter(lambda card: MoveChecker.checkDefenseCard(coveredCard, trump, card), cards))

    def checkDefenseCard(tableCard, trump, card):
        if (tableCard.suit == card.suit and tableCard.rank < card.rank) or (tableCard.suit != trump.suit and card.suit == trump.suit):
            return True
        return False

    def checkOffenseCard(table, trump, card):
        if table.cards == []:
            return True
        else:
            for tableCard in table.cards:
                if tableCard.rank == card.rank:
                    return True
            return False


class PerdurakApp:
    def __init__(self, screenParams = (50, 50)):
        self.perdurakScreen = PerdurakScreen(screenParams)
        self.perdurakState = PerdurakState(humanPlayers = True, players = 3)

    def run(self):
        self.perdurakState.dealCards(6)
        while self.perdurakState.deck.cards:
            for playerNumber in range(len(self.perdurakState.substates)):
                self.perdurakState.topUpCards(6)
                if not self.perdurakState.switchFlag:
                    self.perdurakState.table.cards = [] # поменять, если перевел
                    self.perdurakState.tableChangeFlag = True
                while self.perdurakState.tableChangeFlag == True:
                    self.perdurakState.tableChangeFlag = False
                    attackingPlayer = playerNumber
                    defendingPlayer = (attackingPlayer+1)%len(self.perdurakState.substates)
                    self.attackLoop(attackingPlayer, defendingPlayer)
                    if self.defendLoop(defendingPlayer):
                        break
                    for otherPlayerNumber in range(len(self.perdurakState.substates) - 2):
                        otherPlayer = (defendingPlayer + otherPlayerNumber + 1)%len(self.perdurakState.substates)
                        self.attackLoop(otherPlayer, defendingPlayer)
            # self.perdurakState.substates[0].putCard(self.perdurakState.table, self.perdurakState.substates[0].cards[0])
            # self.perdurakState.substates[0].takeTableCards(self.perdurakState.table)
            # self.perdurakScreen.draw(self.perdurakState)

    def attackLoop(self, attackingPlayerNumber, defendingPlayerNumber):
        userInput = None
        while self.perdurakState.table.getUncoveredCardsNumber() <= len(self.perdurakState.substates[defendingPlayerNumber].cards) and (userInput != "n" and MoveChecker.getValidOffenseCards(self.perdurakState.table, self.perdurakState.deck.trump, self.perdurakState.substates[attackingPlayerNumber].cards) or not self.perdurakState.table.cards):
            print("Player " + str(attackingPlayerNumber) + " is attacking player " + str(defendingPlayerNumber))
            self.perdurakScreen.draw(self.perdurakState, attackingPlayerNumber, isInOffense = True)
            userInput = input("Choose card to attack with, n to proceed")
            try:
                validCards = MoveChecker.getValidOffenseCards(self.perdurakState.table, self.perdurakState.deck.trump, self.perdurakState.substates[attackingPlayerNumber].cards)
                if int(userInput) < len(validCards):
                    self.perdurakState.substates[attackingPlayerNumber].putCard(self.perdurakState.table, validCards[int(userInput)])
                    self.perdurakState.tableChangeFlag = True
            except ValueError:
                pass
            except IndexError:
                print("Value is out of bounds.")

    def defendLoop(self, defendingPlayerNumber):
        userInput = None
        switchValidFlag = True
        while userInput != "n":
            if self.perdurakState.table.allCardsAreCovered():
                break
            print("Player " + str(defendingPlayerNumber) + " is defending.")
            validSwitchCards = MoveChecker.getValidOffenseCards(self.perdurakState.table, self.perdurakState.deck.trump, self.perdurakState.substates[defendingPlayerNumber].cards)
            if validSwitchCards:
                self.perdurakScreen.draw(self.perdurakState, defendingPlayerNumber, isInOffense = True)
            else:
                self.perdurakScreen.draw(self.perdurakState, defendingPlayerNumber, isInOffense = False)
            if switchValidFlag and validSwitchCards:
                userInput = input("Choose a card to defend against, n to take all cards, s to switch")
                if userInput == "s":
                    userInput = input("Choose a card to perform a switch: ")
                    try:
                        self.perdurakState.substates[defendingPlayerNumber].putCard(self.perdurakState.table, validSwitchCards[int(userInput)])
                        self.perdurakState.switchFlag = True
                        break
                    except ValueError:
                        pass
                    except IndexError:
                        print("Value is out of bounds.")
            else:
                userInput = input("Choose a card to defend against, n to take all cards")
            try:
                if int(userInput) < len(self.perdurakState.table.cards) and not self.perdurakState.table.cards[int(userInput)].isCovered:
                    coveredCard = int(userInput)
                    validCards = MoveChecker.getValidDefenseCards(self.perdurakState.table.cards[coveredCard], self.perdurakState.deck.trump, self.perdurakState.substates[defendingPlayerNumber].cards)
                    self.perdurakScreen.drawValidDefenseCards(self.perdurakState, defendingPlayerNumber, coveredCard)
                    userInput = input("Choose a card to defend with")
                    if int(userInput) < len(validCards):
                        coveringCard = int(userInput)
                        self.perdurakState.substates[defendingPlayerNumber].defendWithCard(self.perdurakState.table, validCards[int(userInput)], self.perdurakState.table.cards[coveredCard])
                        self.perdurakState.tableChangeFlag = True
                        switchValidFlag = False
            except ValueError:
                pass
            except IndexError:
                print("Value is out of bounds.")
        if self.perdurakState.switchFlag:
            return True
        if not self.perdurakState.table.allCardsAreCovered() and not self.perdurakState.switchFlag:
            self.perdurakState.substates[defendingPlayerNumber].takeTableCards(self.perdurakState.table)
            return True
        else:
            return False

