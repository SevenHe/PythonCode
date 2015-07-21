# Running in CodeSkulptor!

import simplegui
import random

CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

in_play = False
outcome = ""
tip = ""
index = 0                                # index for deck
score = 0

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
        
    def __str__(self):
        return " Card Suit=" + self.suit + " Card Rank=" + self.rank
      
    def get_suit(self):
        return self.suit
      
    def get_rank(self):
        return self.rank
      
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                  CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
     
    
class Hand:
    def __init__(self, identity):
        self.hand_cards = []
        self.identity = identity
        self.Aces = 0
      
    def __str__(self):
        return self.identity + "---Hand Cards: " + self.cards
      
    def add_card(self, card_append):
        self.hand_cards.append(card_append)
        if card_append.get_rank() == 'A':
            self.Aces += 1
    
    def get_value(self):
        value = 0
        for v in self.hand_cards:
            value += VALUES[v.get_rank()]
        if self.Aces >= 2:
            return value
        elif self.Aces == 1:
            if value + 10 <= 21:
                return value + 10
            else:
                return value
        else:
            return value
      
    def busted(self):
        value_in_busted = self.get_value()
        if value_in_busted > 21:
            return True
        elif value_in_busted >= 0:
            return False
        else:
            return "Error"
        
    def draw(self, canvas, p):
        i = 0
        while i < len(self.hand_cards):
            p[0] += i * 50
            if i == 0 and self.identity == 'Dealer' and in_play == True:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [p[0] + CARD_BACK_CENTER[0], p[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE) 
            else:
                self.hand_cards[i].draw(canvas, p)
            i += 1
        
class Deck:
    def __init__(self, deck_cards):
        self.deck_cards = deck_cards
    
    def shuffle(self):
        random.shuffle(self.deck_cards)
    
    # 2 actors for circling , and 1 for player, 0 for dealer 
    def deal_card(self, times, actor):
        global index
        i = 0
        if actor == 2:
            while i < times:
                if index % 2 == 0:
                    player.add_card(deck_cards[index])
                    print player.identity + " get a " + deck_cards[index].get_suit() + deck_cards[index].get_rank() 
                    index += 1
                else:
                    dealer.add_card(deck_cards[index])
                    print dealer.identity + " get a " + deck_cards[index].get_suit() + deck_cards[index].get_rank() 
                    index += 1
                i += 1
        elif actor == 1:
            while i < times:
                player.add_card(deck_cards[index])
                print player.identity + " get a " + deck_cards[index].get_suit() + deck_cards[index].get_rank() 
                index += 1
                i += 1
        elif actor == 0:
            while i < times:
                dealer.add_card(deck_cards[index])
                print dealer.identity + " get a " + deck_cards[index].get_suit() + deck_cards[index].get_rank() 
                index += 1
                i += 1
        else:
            print "Error!"
            
def init_player_and_dealer():
    global player, dealer, player_pos, dealer_pos
    player_pos = [100, 250]
    dealer_pos = [100, 450]
    player = Hand('Player')
    dealer = Hand('Dealer')
    
def init_deck():
    global deck_cards, deck
    deck_cards = []
    for s in SUITS:
        for r in RANKS:
            c = Card(s, r)
            deck_cards.append(c)
    deck = Deck(deck_cards)
    deck.shuffle()

# this button can take effect in any time , though it's in playing!(two times clicked)
def deal():
    global outcome, tip, in_play, score, index
    if in_play == True:
        outcome = "You lose."
        tip = "New deal?"
        score -= 1
        in_play = False
    elif in_play == False:
        outcome = ""
        tip = "Hit or Stand?"
        deck.shuffle()
        init_player_and_dealer()
        index = 0
        in_play = True
        print "New game begin..."
        deck.deal_card(4, 2)
    
def hit():
    global player, deck, outcome, tip, score, in_play
    if in_play == True:
        if not player.busted():
            deck.deal_card(1, 1)
            if player.busted():
                outcome = "You went busted and lose."
                tip = "New deal?"
                score -= 1
                in_play = False
    else:
        print "Invalid operation!"
    
def stand():
    global player, dealer, outcome, tip, score, in_play
    if player.get_value() == 21:
        outcome = "You win."
        tip = "New deal?"
        score += 1
        in_play = False
        return
    while player.get_value() > dealer.get_value() and not dealer.busted():
        deck.deal_card(1, 0)
    if player.get_value() > dealer.get_value() or dealer.busted():
        outcome = "You win."
        tip = "New deal?"
        score += 1
        in_play = False
    elif player.get_value() < dealer.get_value():
        outcome = "You lose."
        tip = "New deal?"
        score -= 1
        in_play = False

def draw(canvas):
    global outcome, tip, in_play, player_pos, dealer_pos
    canvas.draw_text("BlackJack", [200, 100], 30, 'Aqua')
    canvas.draw_text("Score " + str(score), [450, 100], 20, 'Black')
    canvas.draw_text("Dealer", [130, 200], 20, 'Black')
    canvas.draw_text('Player', [130, 400], 20, 'Black')
    canvas.draw_text(outcome, [300, 200], 20, 'Black')
    canvas.draw_text(tip, [300, 400], 20, 'Black')
    dealer.draw(canvas, dealer_pos)
    player.draw(canvas, player_pos)

frame = simplegui.create_frame("BlackJack", 600, 600)
frame.set_canvas_background("Green")

frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# Initializing.
init_deck()
init_player_and_dealer()

# Frame Starts!
frame.start()

# The next step to improve the program is encapsulating the win or lose changes and draws.
