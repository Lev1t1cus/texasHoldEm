import random
import time
import operator
from os import system, name
from math import floor

class Card:
    """
    Each card has a value: 0-13.
        0: Joker.
        14: Ace.
        2-10: numbers.
        11: Jack.
        12: Queen.
        13: King.
    Each card has a suit:
        0: Spades.        ♠
        1: Hearts.        ♥
        2: Clubs.         ♣
        3: Diamonds.      ♦
    Each card has a color:
        0: black
        1: red
    """
    def __init__(
        self,
        value=0,
        suit=0,
        color=0
    ):
        self.value = value
        self.suit = suit
        self.color = color
class Dealer:
    """
    money: the money currently in the pot.
    deck:  the full deck.
    discard: cards removed from play.
    hand: the current cards available to purchase.
    """
    money = 0
    deck = []
    discard = []
    hand = []
    callBet = 0

    @staticmethod
    def buildDeck():
        """creates main deck."""
        cards = []
        for i in range(2, 15):
            for j in range(0, 4):
                cards.append(Card(i, j))
        for card in cards:
            if card.suit % 2 == 0:
                card.color = 0
            else:
                card.color = 1
        # create two jokers?
        return cards

    def drawCard(self):
        """draw the card on top of the deck."""
        self.hand.append(self.deck.pop(-1))

    def burn(self):
        """discard the top card of the deck."""
        self.discard.append(self.deck.pop(-1))

    def shuffleDeck(self):
        """this function randomly shuffles the player's deck."""
        tempDeck = []
        for i in range(0, len(self.deck)):
            ran = random.randint(0, len(self.deck)-1)
            tempDeck.append(self.deck[ran])
            del self.deck[ran]
        self.deck = tempDeck

    def shuffleDiscard(self):
        for i in range(len(self.discard)-1, -1, -1):
            self.deck.append(self.discard[i])
            del self.discard[i]
class Player:
    """
    name: the player's name.
    money: player's money.
    hand: the player's current hand.
    score: the player's score, based on hand, high valued cards, and tiebreaker.
    playing: currently playing the round or not.
    """
    def __init__(self):
        self.name = ""
        self.money = 0
        self.hand = []
        self.score = 0
        self.playing = True

    def drawCard(self, dealer):
        self.hand.append(dealer.deck.pop(-1))

    def discardCard(self, dealer):
        dealer.discard.append(self.hand.pop(-1))


# Global Functions
SHOWDOWN = 1000000
POWER = 10000

def GETSHOWDOWN(score):
    """get first digit of score"""
    score -= score % SHOWDOWN
    score /= SHOWDOWN
    return score
def GETPOWER(score):
    """get second and third digit of score"""
    score = score % SHOWDOWN
    score -= score % POWER
    score /= POWER
    return score
def GETBONUS(score):
    """ get last digit of score """
    return score % POWER

def clear():
    if name == 'nt':        # for windows
        _ = system('cls')
    else:                   # for mac and linux(here, os.name is 'posix')
        _ = system('clear')

def suitCheck(card):
    if card.suit == 0:
        return "♠"
    elif card.suit == 1:
        return "♥"
    elif card.suit == 2:
        return "♣"
    else:
        return "♦"
def colorCheck(card):
    if card.color == 0:
        return "black"
    else:
        return "red"
def valueCheck(card):
    switcher = {
        14: "Ace",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "Jack",
        12: "Queen",
        13: "King"
        # 0: "Joker"
    }
    return switcher.get(card.value, "Joker")

def placeBet(player, dealer):
    print("\nYou can call the current bet at $" + str(dealer.callBet) + " or raise it.")
    print("Type '0' to fold, or type '*' to all in.")
    bet = input("Place your bet, " + player.name + ": $")
    try:
        if bet == '*':
            print("\n" + player.name + " is all in.")
            player.playing = 2
            dealer.money += player.money
            dealer.callBet = player.money
            player.money = 0
            return True
        bet = int(bet)
        if bet == 0:
            print("\n" + player.name + " has folded.")
            player.discardCard(dealer)
            player.discardCard(dealer)
            player.playing = False
            return True
        if bet <= player.money & player.money > dealer.callBet:  # if the call is > player.money, they can go into debt.
            if bet >= dealer.callBet:
                print("\n" + player.name + " bet $" + str(bet) + ".")
                player.money -= bet
                dealer.money += bet
                dealer.callBet = bet
                return True
            else:
                print("\nYou must at least call the current bet.")
                return False
        else:
            print("\nYou don't have enough money.")
            return False
    except ValueError:
        print("\nInvalid input.")
        return False

def printCard(card):
    """handles card display"""
    color = 30
    if colorCheck(card) == "red":
        color = 31
    # 47m is white

    print(
        "\033[1;" + str(color) + ";40m " +
        valueCheck(card).ljust(7, " ") +
        suitCheck(card).ljust(4, " ") +
        "\033[1;37;40m"
    )
def printTable(player, dealer):
    """displays table's current state."""
    clear()
    print("Board:                                " + "current pot: $" + str(dealer.money))
    for card in dealer.hand:
        printCard(card)
    print("\nYour Hand:                            " + "your money:  $" + str(player.money))
    for card in player.hand:
        printCard(card)

def playerTurn(players, playerCount, dealer):
    for i in range(0, playerCount):
        while True:
            if not players[i].playing:
                break
            printTable(players[i], dealer)
            if players[i].playing == 2 | players[i].money <= 0:
                print("\n" + players[i].name + " is all in.")
                time.sleep(1.5)
                break
            if placeBet(players[i], dealer):
                time.sleep(.5)
                break
            time.sleep(.5)

def flush(hand, player):
    """5 cards same suit, not consecutive"""
    flushCheck = {0: 0, 1: 0, 2: 0, 3: 0}
    comboHand = []
    for card in hand:               # count up the suit of each card
        flushCheck[card.suit] += 1
    for key in flushCheck:          # check if any suit >= 5
        if flushCheck[key] >= 5:
            for card in hand:       # if true, create a "hand" containing only the 5 played cards.
                if card.suit == key:
                    comboHand.append(card)
            player.score = getHighestCard(comboHand)*POWER
            return True
    return False

def straight(hand, player):
    """5 consecutive, Ace can be high or low"""
    if straightHelper(hand, player):    # Test for straights, aces are high
        return True
    for card in hand:                   # Set Aces to value of 1 temporarily
        if card.value == 14:
            card.value = 1
    s = straightHelper(hand, player)    # Test for straights, aces are low
    for card in hand:                   # Reset Aces to 14
        if card.value == 14:
            card.value = 1
    return s
def straightHelper(hand, player):
    """does the bulk of the actual work testing for straights."""
    sortedHand = sorted(hand, key=operator.attrgetter('value'))
    counter = 0
    prev = -1
    s = False
    for card in sortedHand:             # Check aces are low
        if card.value == (prev + 1):    # check against last card
            counter += 1                # counter goes up if they are consecutive
        elif card.value != prev:        # if value = previous, don't do anything
            counter = 0                 # reset counter; not consecutive
        prev = card.value
        if counter >= 4:                # 4 consecutive cards after the first; it's a straight.
            player.score = prev*POWER
            s = True                    # We don't return True right away in the first counter check because in
                                        # certain cases (e.g. 1,2,3,4,5,6,7) it would return 1-5 as the straight
                                        # which is strictly worse than 3-7. By instead leaning on a "straight" var,
                                        # we can tell if we had a straight at some point, and we know what straight
                                        # by the player..score val.
    return s

def straightFlush(hand, player):
    """
    imagine a hand:
    1-0, 2-0, 3-0, 4-0, 9-0, 5-1, Any, Any
    would say straight flush
    its not
    its a straight and a flush
    but not a straight flush

    note: straight flushes (currently) always use the top value of the straight, not the flush.

    i imagine one way to fix this would be:
    we need another function.
    it uses straight and flush, but cuts off anything in the hand not pertaining to the straight.
    needs to be greedy; 1,2,3,4,5,6,7 should keep all 7 then test as it goes through.
    bc 1-5 might be a straight flush, 3-7 is just a straight, and it would miss it if it only kept 3-7.
    """
    # lines copied from flush
    flushCheck = {0: 0, 1: 0, 2: 0, 3: 0}
    comboHand = []
    for card in hand:                       # count up the suit of each card
        flushCheck[card.suit] += 1
    for key in flushCheck:                  # check if any suit >= 5
        if flushCheck[key] >= 5:
            for card in hand:               # if true, create a "hand" containing only the 5 played cards.
                if card.suit == key:
                    comboHand.append(card)
            return straight(comboHand, player)      # this line is the only one that differs
    return False

def royalFlush(hand):
    """straight flush consisting of \"A K Q J 10\""""
    if getHighestCard(hand) == 14:
        return True
    return False

def twoOfAKind(hand, player):
    """two cards with matching values."""
    if ofAKind(hand, 2, player):
        return True
    return False
def threeOfAKind(hand, player):
    """three cards with matching values."""
    if ofAKind(hand, 3, player):
        return True
    return False
def fourOfAKind(hand, player):
    """four cards with matching values."""
    if ofAKind(hand, 4, player):
        return True
    return False
def ofAKind(hand, match, player):
    """does the bulk of the work for all \"of a kind\" functions."""
    values = []
    extraHand = []
    for card in hand:
        values.append(card.value)
    for i in range(14, 1, -1):
        if values.count(i) == match:
            player.score = i*POWER
            for card in hand:
                if card.value != i:
                    extraHand.append(card)
            ofAKindTiebreaker(extraHand, match, player)
            return True
    return False

def ofAKindTiebreaker(hand, match, player):
    """handles grabbing the tiebreaker from the cards not in the user's hand."""
    for i in range(match, 5):               # performs loop thrice for 2pair, twice for 3pair, once for 4pair
        high = getHighestCard(hand)
        player.score += high * ((512 * 8**2) / (8**i))    # each successive loop gives less points for card
        for card in hand:
            if card.value == high:
                hand.remove(card)

def fullHouse(hand, player):
    """three of a kind + two of a kind."""
    if twoOfAKind(hand, player):
        double = GETPOWER(player.score)         # remove bonus points - get 2nd & 3rd digit
        comboHand = []
        for card in hand:                       # create a hand not including the found pair
            if card.value != double:
                comboHand.append(card)
        ret = threeOfAKind(comboHand, player)
        if ret:
            player.score = GETPOWER(player.score)*POWER     # remove bonus points
            player.score += double                          # add value of double if threeOfAKind succeeded
        return ret
    return False

def twoPair(hand, player):
    """two separate pairs (two cards of matching value."""
    if twoOfAKind(hand, player):
        first = GETPOWER(player.score)          # remove bonus points - get 2nd & 3rd digit
        comboHand = []
        finalHand = []
        for card in hand:                       # create a hand not including the found pair
            if card.value != first:
                comboHand.append(card)
        ret = twoOfAKind(comboHand, player)
        if ret:
            second = GETPOWER(player.score)     # value of the second twoOfAKind
            mx = max(first, second)             # compare both values to see which pair takes priority
            mn = min(first, second)
            player.score = mx * POWER           # 2nd/3rd digits take the higher pair
            player.score += mn * 8              # the smaller becomes: bonus points * 8
            for card in comboHand:              # remove the second pair from the current hand
                if card.value != second:
                    finalHand.append(card)
            final = getHighestCard(finalHand)   # find the highest card in the remaining 3 cards
            player.score += final               # this is the final tiebreaker
        return ret
    return False

def highCard(hand, player):
    """returns a score of all 5 cards in hand, assuming none fall into any other combinations."""
    h = getHighestCard(hand)                # first we search for the highest card
    player.score = h * POWER                # this is the main piece of our score
    print(h)
    for card in hand:
        if card.value == h:
            hand.remove(card)
    multi = 512                             # score multiplier
    for i in range(0, 4):                   # now we loop through to build our tiebreakers
        h = getHighestCard(hand)
        player.score += h * multi           # multiplier should go 512 -> 64 -> 8 -> 1
        multi /= 8
        for card in hand:                   # remove card if its the card, since we don't want repeat high cards.
            if card.value == h:
                hand.remove(card)
    return True
def getHighestCard(hand):
    """returns highest card value in hand."""
    mx = 0
    for card in hand:
        if card.value > mx:
            mx = card.value
    return mx

def cardCombos(player, dealer):
    """
    Royal Flush:     A K Q J 10 same suit                           perfect hand
    Straight Flush:  Five cards consecutive same suit (e.g. 1-5)    top card value matters
    Four of a Kind:  title.                                         value matters
    Full House:      Three of a kind + Two of a kind.               value matters, three takes priority.
    Flush:           5 cards same suit, not consecutive.            top card value matters
    Straight:        5 consecutive, Ace can be high or low          top card value matters
    Three of a Kind: Title.                                         value matters
    Two Pairs:       Two separate pairs.                            top pair value matters
    Pair:            Title.                                         value matters
    High Card:       No combinations.                               highest card value matters.

    Ties can be broken with the highest value of cards not in the combination.
    """
    tempHand = []                           # creates a temporary "hand"
    for card in player.hand:                # that contains both cards in player's hand
        tempHand.append(card)
    for card in dealer.hand:                # and all five cards on the board.
        tempHand.append(card)
    # test for best combination
    if straightFlush(tempHand, player):     # strongest hand
        if royalFlush(tempHand):            # test if hand is perfect
            return "royal flush"            # 1st place
        return "straight flush"             # 2nd place
    if fourOfAKind(tempHand, player):       # 3rd place
        return "four of a kind"
    if fullHouse(tempHand, player):         # 4th place
        return "full house"
    if flush(tempHand, player):             # 5th place
        return "flush"
    if straight(tempHand, player):          # 6th place
        return "straight"
    if threeOfAKind(tempHand, player):      # 7th place
        return "three of a kind"
    if twoPair(tempHand, player):           # 8th place
        return "two pair"
    if twoOfAKind(tempHand, player):        # 9th place
        return "two of a kind"
    highCard(tempHand, player)              # 10th place
    return "high card"                      # default return

def startGame():
    clear()             # init system
    print("\033[1;37;40m" + "Texas Hold Em.\n")

    dealer = Dealer()   # init main deck
    dealer.deck = dealer.buildDeck()
    dealer.shuffleDeck()

    players = []        # create players
    while True:
        try:
            playerCount = int(input("Enter number of players (max 20): "))
            if playerCount > 20:
                print("Too many; max 20 players.")
            else:
                break
        except ValueError:
            print("Please enter a number.")

    startMoney = 100
    ante = 1

    for i in range(0, playerCount):                                      # For each player...
        players.append(Player())                                         # first, add them to the list of players
        players[i].name = input("enter player " + str(i) + "'s name: ")  # ask for player's name
        if players[i].name == "":
            players[i].name = "Player " + str(i)
        players[i].money += startMoney                                   # add startMoney
        print(players[i].name + " joined the game.\n")
    time.sleep(.6)
    gamePlayLoop(players, playerCount, dealer, ante)

def gamePlayLoop(players, playerCount, dealer, ante):
    # Main Gameplay Loop
    while True:
        for i in range(0, playerCount):
            players[i].drawCard(dealer)      # draw two cards
            players[i].drawCard(dealer)
            players[i].money -= ante         # ante up
            dealer.money += ante
            print(players[i].name + " anted up $" + str(ante) + ".")
            time.sleep(.1)

        time.sleep(.5)
        dealer.callBet = ante

        # initial round of bets
        playerTurn(players, playerCount, dealer)

        # round one, the "flop"
        clear()
        print("Here's the flop.")
        time.sleep(1)
        dealer.burn()
        dealer.drawCard()
        dealer.drawCard()
        dealer.drawCard()
        dealer.callBet = ante
        playerTurn(players, playerCount, dealer)

        # round two, the "turn"
        clear()
        print("Here's the turn.")
        time.sleep(1)
        dealer.burn()
        dealer.drawCard()
        dealer.callBet = ante
        playerTurn(players, playerCount, dealer)

        # round three, the "river"
        clear()
        print("Here's the river.")
        time.sleep(1)
        dealer.burn()
        dealer.drawCard()
        dealer.callBet = ante
        playerTurn(players, playerCount, dealer)

        # the showdown
        for i in range(0, playerCount):
            combo = cardCombos(players[i], dealer)
            showdownSwitch = {
                "royal flush"       : SHOWDOWN*9,
                "straight flush"    : SHOWDOWN*8,
                "four of a kind"    : SHOWDOWN*7,
                "full house"        : SHOWDOWN*6,
                "flush"             : SHOWDOWN*5,
                "straight"          : SHOWDOWN*4,
                "three of a kind"   : SHOWDOWN*3,
                "two pair"          : SHOWDOWN*2,
                "two of a kind"     : SHOWDOWN*1,
                "high card"         : SHOWDOWN*0
            }
            players[i].score += showdownSwitch.get(combo)

        # scoring works on a tiered basis, using the format: 0 00 0000
        # the first digit, 0-9, is the "showdown" digit. As this is the highest degree
        # digit, it's guaranteed to take priority. The hand determines this digit, so a
        # better hand should always win.
        # the second and third digit, 1-14, are the "value" digits. This determines the
        # strength of the hand, in the event of a tie.
        # the last four digits, 0-7521, are the "bonus points" digits. They act as the
        # final tiebreaker in the case two players have the same valued hands. They use
        # multiples of 8 to determine order (since 2*8 > 14). Using highCard as an example:
        # Hand is: 14, 13, 12, 11, 9. No hand could be played. So:
        # digit 2/3 are set to 14, for the highest card.
        # we add 13 * 512 for bonus points.
        # we add 12 * 64 for bonus points.
        # we add 11 * 8 for bonus points.
        # we add 9 * 1 for bonus points.
        # in this way, 14 takes priority over 13, which takes priority of 12, etc.
        # scores are compared, and the highest score wins.
        # in the unlikely event that two players have exactly the same score, they tie and
        # both players get a share of the pot.

        # who wins?
        mx = 0
        winners = []
        for i in range(0, playerCount):                 # find highest score
            if players[i].score > mx:
                mx = players[i].score
                winners.clear()
                winners.append(players[i])              # current winner
        for i in range(0, playerCount):                 # now see if there are any ties
            if players[i].score == mx:
                if players[i] != winners[0]:            # don't count ties between the same person
                    winners.append(players[i])          # a tie was found

        # perform a show to see who wins
        clear()
        print("Time for the showdown.")
        time.sleep(1)
        stringDict = {}

        for i in range(0, playerCount):
            s = GETSHOWDOWN(players[i].score)
            p = GETPOWER(players[i].score)
            input("\n" + players[i].name + ", show your hand:")
            showdownSwitch = {
                9: "Royal Flush",
                8: "Straight Flush ",
                7: "Four ",
                6: "Full House ",
                5: "Flush ",
                4: "Straight to the ",
                3: "Three of a kind - ",
                2: "Two pair - ",
                1: "Pair of ",
                0: "high "
            }                      # grabs name of hand
            valueSwitch = {
                2: "Two",
                3: "Three",
                4: "Four",
                5: "Five",
                6: "Six",
                7: "Seven",
                8: "Eight",
                9: "Nine",
                10: "Ten",
                11: "Jack",
                12: "Queen",
                13: "King",
                14: "Ace"
            }                         # grabs value of hand
            main = showdownSwitch.get(s)
            append = valueSwitch.get(p)
            if main == "Royal Flush":                   # prints out unique formatting quirks per hand
                append = ""
            elif (main == "Four ") | (main == "Pair of "):
                append += "s"
            elif main == "Three of a kind - ":
                append += "s up"
            elif main == "Two pair - ":
                append += " high"
            elif main == "Full House ":
                append += "-to-" + str(valueSwitch.get(GETBONUS(players[i].score)))

            stringDict[players[i]] = main + append      # we save the full string to stringDict for future comparison
            print("\n" + str(players[i].name) + " reveals: ")
            time.sleep(1)
            print("\t" + stringDict.get(players[i]) + "!")
            time.sleep(.5)
        time.sleep(.5)
        clear()
        print("\n The winner is...")
        time.sleep(2)
        #see if there are any intermediate ties
        #iterate through stringDict
        #also add dealer npc??? Guaranteed player

        if len(winners) == 1:
            print("\n\t" + winners[0].name + " with a " + stringDict.get(winners[0]) + "!")
        else:
            print("Oh! There's a tie between:")
            for player in winners:
                print("\t" + player.name + " with a " + stringDict.get(player))
        time.sleep(3)

        # distribute money
        clear()
        div = floor(dealer.money / len(winners))        # divide pot among winners
        dealer.money = 0
        for player in winners:
            player.money += div
            print("\n" + player.name + " is payed out $" + str(div) + ".")
            time.sleep(.1)
        time.sleep(2)

        # cleanup
        clear()
        for i in range(0, playerCount):                 # discard player's hands
            if players[i].playing:
                players[i].discardCard(dealer)
                players[i].discardCard(dealer)
                players[i].score = 0
            else:
                players[i].playing = True
            if players[i].money <= 0:                   # player is out of the game

                players[i].playing = False              # currently irreversible, could be fixed later

        for i in range(len(dealer.hand) - 1, -1, -1):   # return board to deck
            dealer.deck.append(dealer.hand[i])
            del dealer.hand[i]
        dealer.shuffleDiscard()                         # return discard pile to deck
        dealer.shuffleDeck()

def debug():
    """let's debug!"""
    dealer = Dealer()
    dealer.deck = dealer.buildDeck()
    hand = []
    player = Player()

    while True:
        hand.clear()
        hand.append(Card(1, 0))
        hand.append(Card(2, 0))
        hand.append(Card(3, 0))
        hand.append(Card(4, 0))
        hand.append(Card(5, 0))
        hand.append(Card(6, 2))
        hand.append(Card(7, 3))
        # assert flush(hand, player)             # working
        # assert straight(hand, player)          # working
        # assert straightFlush(hand, player)     # working
        # assert royalFlush(hand)                # working
        # assert fourOfAKind(hand, player)       # working
        # assert threeOfAKind(hand, player)      # working
        # assert twoOfAKind(hand, player)        # working
        # assert fullHouse(hand, player)         # working
        # assert twoPair(hand, player)           # working
        # assert highCard(hand, player)          # working
        print(player.score)
        player.score = 0
        time.sleep(3)


# Start Game
# debug()
startGame()
