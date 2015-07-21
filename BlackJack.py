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
            if i == 0 and self.identity == 'Dealer':
                canvas.draw(card_back, CARD_BACK_SIZE, [p[0] + CARD_BACK_CENTER[0], p[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE) 
            else:
                self.hand_cards[i].draw(canvas, p)
            i += 1
        
class Deck:
    def __init__(self, deck_cards):
        self.deck_cards = deck_cards
    
    def shuffle(self):
        random.shuffle(self.deck_cards)
      
    def deal_card(self, circles):
        global index
        i = 0
        while i < circles * 2:
            if index % 2 == 0:
                player.add_card(deck_cards[index])
                print player.identity + " get a " + deck_cards[index].get_suit() + deck_cards[index].get_rank() 
                index += 1
            else:
                dealer.add_card(deck_cards[index])
                print dealer.identity + " get a " + deck_cards[index].get_suit() + deck_cards[index].get_rank() 
                index += 1
            i += 1

            
def init_player_and_dealer():
    global player, dealer, index, player_pos, dealer_pos
    player_pos = [100, 250]
    dealer_pos = [100, 450]
    player = Hand('Player')
    dealer = Hand('Dealer')
    deck.deal_card(2)
    
def init_deck():
    global deck_cards, deck
    deck_cards = []
    for s in SUITS:
        for r in RANKS:
            c = Card(s, r)
        deck_cards.append(c)
    deck = Deck(deck_cards)
    deck.shuffle()

# this button can take effect in any time , though it's in playing!
def deal():
    global outcome, in_play
    deck.shuffle()
    init_player_and_dealer()
    in_play = True

    
def hit():
    if in_play == True:
        pass
    
def stand():
    pass

def draw(canvas):
    pass

frame = simplegui.create_frame("BlackJack", 600, 600)
frame.set_canvas_background("Green")

frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


frame.start()

# Then next for the button handler, and Deck_class and draw_handler!
