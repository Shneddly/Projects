'''
A program written to practice using loops, class objects, and user interfaces to create a simple game of blackjack
'''

from IPython.display import clear_output
import random

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# Card Class
class Card():
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __repr__(self):
        return self.rank + " of " + self.suit
    
# Deck Class
class Deck():
    
    def __init__(self):
        
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                # Create Card Object
                self.all_cards.append(Card(suit,rank))
    
    def shuffle(self):
        
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        
        return self.all_cards.pop()

# Chip Class
class Chip():
    # Chip needs to have a balance attribute
    
    def __init__(self,name,balance=0):
        
        self.name = name
        self.balance = balance
        
    def bet_placed(self,bet_amount):
        
        self.balance -= bet_amount
        print(f"You have bet ${bet_amount} on this hand.")
            
    def bet_won(self,bet_amount):
        
        self.balance += 2*bet_amount
        print(f"You have won ${bet_amount} from this hand!")
        
    def blackjack(self,bet_amount):
        
        self.balance += 2.5*bet_amount
        print(f"You have won ${1.5*bet_amount} from this hand!")
        
    def bet_tie(self,bet_amount):
        
        self.balance += bet_amount
        print(f"It was a tie. ${bet_amount} has been returned to you.")
        
    def __str__(self):
        
        return f"{self.name}\'s current chip count is ${self.balance}."
        
class Hand():
    
    def __init__(self,name):
        
        self.name = name
        self.hand = []
        self.value = 0
        self.aces = 0
        
    def hand_hit(self,new_card):
        # Adds a new card to the hand
        self.hand.append(new_card)
        self.value += new_card.value
        
        if new_card.rank == 'Ace':
            self.aces += 1
            
    def ace_change(self):
        # Checks if there is an ace in the hand. If there is, changes the value from 11 to 1
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
        
    def __str__(self):
        
        return f'{self.name}\'s hand contains {self.hand}'
    
def ask_new_hand():
    # Could shorten this to the input line and if else statements, assume anything not a y/Y is a no
    choice = 'placeholder'
    while choice not in ['Y','N']:
        choice = input("Play another hand? (Y or N) ").upper()
        if choice not in ['Y','N']:
            print("Sorry, I don\'t understand, please choose Y or N")

    if choice == "Y":
        
        return True
    
    else:
        
        return False
    
def ask_hit():
    # Could shorten this to the input line and if else statements, assume anything not a y/Y is a no
    choice = 'placeholder'
    while choice not in ['Y','N']:
        choice = input("Would you like to hit? (Y or N) ").upper()
        if choice not in ['Y','N']:
            print("Sorry, I don\'t understand, please choose Y or N")

    if choice == "Y":
        
        return True
    
    else:
        
        return False
    
def show_some(player,dealer):
    print(f"{player}, with a sum of {player.value}.")
    print(f"Dealer's hand contains [{dealer.hand[0]},???].")
    
def show_all(player,dealer):
    print(f"{player}, with a sum of {player.value}.")
    print(f"{dealer}, with a sum of {dealer.value}.")
    
def hit(hand,deck,player):
    hand.hand_hit(deck.deal_one())
    print(f"{player} hits!")
    # if sum of hand > 21 AND one of the cards is an Ace, change value of Ace to 1
    hand.ace_change()


    # Game logic
    # Game Setup
player_chips = Chip('Player',100)

game_on = True

count = 0
# Game Logic
# Game while loop
while game_on == True:
    # Hand setup
    clear_output()
    print("Welcome to Monty Python's Blackjack!")
    new_deck = Deck()
    new_deck.shuffle()
    count += 1
    hand_over = False
    player_hand = Hand('Player')
    dealer_hand = Hand('Dealer')
    print(f"Current hand: {count}")
    # Bet step
    print(player_chips)
    valid_bet = False
    while valid_bet == False:
        # try, except, else statements address if the input happens to be a string
        try:
            bet_amount = int(input("Bet amount: "))
        except:
            print("Not a real number!")
            #continue
        else:
            # identical if else statements because the over-bet handling happens in the Chips class object
            if bet_amount > player_chips.balance:
                print("Sorry, you can\'t bet that much!")
            else:
                player_chips.bet_placed(bet_amount)
                valid_bet = True
    while hand_over == False:
        # Deal step, dealing 2 cards each to the player and dealer
        for x in range (2):
            player_hand.hand_hit(new_deck.deal_one())
            dealer_hand.hand_hit(new_deck.deal_one())
        # Show hands step
            # if the player happens to have two aces, it will change the value of an ace to 1
        player_hand.ace_change()
        dealer_hand.ace_change()
        show_some(player_hand,dealer_hand)
        if player_hand.value == 21:
            # if the sum of the player's hand is 21, ie an ace and a value 10 card, it's an auto win
            print("Blackjack!")
            player_chips.blackjack(bet_amount)
            hand_over = True
            break
        # Hit or Stay while loop
        player_stay = False
        while player_stay == False:
            if ask_hit() == True:
                hit(player_hand,new_deck,'Player')
                show_some(player_hand,dealer_hand)
                if player_hand.value > 21:
                    player_stay = True
                    break
                else:
                    pass
            else:
                player_stay = True
        if player_hand.value > 21:
            # if sum of hand > 21, player loses
            print("Oops! Over 21! House wins.")
            hand_over = True
            break
        show_all(player_hand,dealer_hand)
        dealer_stay = False
        while dealer_stay == False:
            # while loop for dealer's turn to hit
            if dealer_hand.value < 17:
                # if the sum of hand < 17, then the dealer will draw a card
                hit(dealer_hand,new_deck,'Dealer')
                show_all(player_hand,dealer_hand)
                if dealer_hand.value > 21:
                    dealer_stay = True
                    break
                else:
                    pass
            else:
                dealer_stay = True
                
        # Final comparison
        if dealer_hand.value > 21:
            # if sum of hand > 21, dealer loses
            print("House is over 21. You win!")
            player_chips.bet_won(bet_amount)
            hand_over = True
            #break
        elif dealer_hand.value == player_hand.value:
            # if hand.dealer == hand.player, tie, player is returned bet amount
            player_chips.bet_tie(bet_amount)
            hand_over = True
            #break
        elif dealer_hand.value > player_hand.value:
            # if hand.dealer > hand.player, player loses
            print("House has won.")
            hand_over = True
            #break
        else:
            # if hand.dealer < hand.player, player wins, add double bet to player account
            print("You win!")
            player_chips.bet_won(bet_amount)
            hand_over = True
            #break
            
    # Play again query
    print(player_chips)
    if not ask_new_hand() == True:
        print("Goodbye!")
        game_on = False
