# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
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
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []

    def __str__(self):
        result = "cards are: "
        if len(self.card_list) == 0:
                return "No cards yet"
        else:
            for card in self.card_list:
                result += card.__str__() + " "
        return result        
    
    def add_card(self, card):
        self.card_list.append(card)

    def get_value(self):
        value = 0
        for i in range(len(self.card_list)):
                value += VALUES[self.card_list[i].get_rank()]
    
        if [i.get_rank() for i in self.card_list if i.get_rank() == 'A'] and value + 10 <= 21:
            value += 10
        else:
            value
        return value
    
    def draw(self, canvas, pos):
        for card in self.card_list:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(i,j) for i in SUITS for j in RANKS]   

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        result = "Deck is: "
        for card in self.deck:
                result += card.__str__() + " "
        return result        



#define event handlers for buttons
def deal():
    global outcome, in_play, my_deck, player_hand, dealer_hand
    
    outcome = ""
    score = 0
    
    # your code goes here
    my_deck = Deck()
    my_deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(my_deck.deal_card())
    player_hand.add_card(my_deck.deal_card())
    
    dealer_hand = Hand()
    dealer_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    
    outcome = "Hit or stand?"
    
    ##################################x
    print my_deck
    print "Player " + str(player_hand)
    print "Player value: " + str(player_hand.get_value())
    print "Dealer " + str(dealer_hand)
    print "Dealer value: " + str(dealer_hand.get_value())
    ####################################
    
    in_play = True

def hit():
    global in_play, outcome, score
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(my_deck.deal_card())     
        if player_hand.get_value() > 21:
            outcome = "You've busted!"
            score -= 1
            in_play = False
            
    
    #################################x
    print "Player after hit " + str(player_hand)
    print "Player after hit value: " + str(player_hand.get_value())
    print outcome
    print score
    ######################################
       
def stand():
    global outcome, in_play, score
    if not in_play:
        outcome = "Hey, you've already busted!"
        return
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(my_deck.deal_card())
            
    if dealer_hand.get_value() > 21:
        outcome = "The dealer's busted, you've won!"
        score += 1
    elif dealer_hand.get_value() >= player_hand.get_value():
        outcome = "The dealer's won, you've lost!"
        score -= 1
    else:
        outcome = "You've won!"
        score += 1
        
    in_play = False
    
    ########################xx
    print "Dealer " + str(dealer_hand)
    print "Dealer value: " + str(dealer_hand.get_value())
    print outcome
    print score
    #########################x
    

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    player_hand.draw(canvas, [40, 440])
    dealer_hand.draw(canvas, [40, 240])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [40 + CARD_BACK_CENTER[0], 240 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)       
    
    #text
    canvas.draw_text('Blackjack', (20, 70), 60, 'Black', 'sans-serif')
    canvas.draw_text('Dealer:', (20, 230), 30, 'White', 'sans-serif')
    canvas.draw_text('You:', (20, 430), 30, 'White', 'sans-serif')
    canvas.draw_text(outcome, (40, 130), 25, 'Blue', 'sans-serif')
    canvas.draw_text("Score: " + str(score), (40, 155), 15, 'Yellow', 'sans-serif')


# initialization frame
frame = simplegui.create_frame("Blackjack", 450, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric