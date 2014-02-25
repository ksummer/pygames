# Playing Cards
# Demonstrates combining objects

class Card(object):
    """ A playing card. """
    RANKS = ["A","9","10","J","Q","K"]
    SUITS = ["c","d","h","s"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        rep = self.rank + self.suit
        return rep

    def getSuit(self):
        rep = self.suit
        return rep

    def getRank(self):
        rep = self.rank
        return rep

class Hand(object):
    """ A hand of playing cards. """

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + "  "
        else:
            rep = "<empty>"
        return rep

    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def top(self):
        rep = self.cards[0]
        return rep

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)

class Deck(Hand):
    """ A deck of playing cards. """
    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank,suit))

    def shuffle(self):
        import random
        random.shuffle(self.cards)
        
    def top(self):
        rep = self.cards[0]
        return rep

    def deal(self, hands, per_hand = 1):
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card, hand)
                else:
                    print("Can't continue deal. Out of cards!")

# main

# introduction
print("Welcome to Euchre!")

# variables
trump = ""
names = []

# deciding number of human players (4 total, unused players will be automated)
playStr = input("\nPlease enter the number players (up to 4): ")
players = int(playStr)

i = 1
print("\nPlease enter the name of each player.\n")
while players > 0:
    name = input("\tPlayer " + str(i) + ": ")
    names.append(name)
    i = i + 1
    players = players - 1

i = 1
while len(names) < 4:
    temp = "Comp" + str(i)
    names.append(temp)
    i = i + 1

# print team members
print("\nThe teams have been decided!")
print("\nTeam 1: " + names[0] + " & " + names[1])
print("Team 2: " + names[2] + " & " + names[3])

# deck creation and shuffling
deck1 = Deck()
deck1.populate()
deck1.shuffle()

# deck testing
print("\nShuffled the deck.")
print("Deck:")
print(deck1)

# create hands and deal 4 cards per hand
hand1 = Hand()
hand2 = Hand()
hand3 = Hand()
hand4 = Hand()
hands = [hand1, hand2, hand3, hand4]

deck1.deal(hands, per_hand = 4)

print("\nThe cards have been dealt!")

# testing dealt cards
i = 0
while i < 4:
    print("Hand " + str(i + 1) + ": " + str(hands[i]))
    i = i + 1
print("Deck:")
print(deck1)

# deciding trump
players = int(playStr)
i = 0
trumpTry = 0
while players > 0:
    players = players - 1
    print("\nTop card is: " + str(deck1.top()))
    print("\nPlayer " + names[i] + ", please decide if this card should be used as trump.")
    i = i + 1
    trumpDecide = input ("Should this card's suit be the trump suit? [Y/N]: ")
    if trumpDecide == "N":
        print("Passing decision to next player.")
    elif trumpDecide == "Y":
        players = 0
        trumpTry = 1
        trump = str(deck1.top().getSuit())
        if trump == "s":
            trump = "Spades"
        elif trump == "c":
            trump == "Clubs"
        elif trump == "h":
            trump = "Hearts"
        else:
            trump = "Diamonds"
while trumpTry == 0:
    print("\nNo player decided to use top card of deck as trump. \nPlayer " + names[0] + " gets to decide trump.")
    trump = input("\nPlease choose the trump suit [C, D, H, S]: ")
    if trump == "C":
        trump = "Clubs"
        trumpTry = 1
    elif trump == "D":
        trump = "Diamonds"
        trumpTry = 1
    elif trump == "H":
        trump = "Hearts"
        trumpTry = 1
    elif trump == "S":
        trump = "Spades"
        trumpTry = 1
    else:
        print("Not a valid trump suit choice. Please try again.")
print("\nTrump suit is " + trump + ".")
    



input("\n\nPress the Enter key to exit.")










