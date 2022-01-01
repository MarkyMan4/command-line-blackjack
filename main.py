from deck.deck import Deck
import sys

# player object
# has cards they are holding and their current number of points
class Player:
    def __init__(self, initial_points=100):
        self._cards = [] # cards in the players hand
        self._points = initial_points # initial points available to bet
        self._bet = 0 # initialize bet to 0, this will be set later

    # if the player is the dealer, the first card dealt will be face down, all other cards are face up
    # if the player is not the dealer, all cards are dealt face up
    def give_card(self, card):
        self._cards.append(card)

    def reset_cards(self):
        self._cards = []

    # calculate the total of the current cards in the players hand
    def get_card_total(self):
        total = 0

        for card in self._cards:
            # ace is worth 11 if it doesn't make the hand go over 21
            # otherwise it is worth 1 (it's default value according to the deck)
            if card.rank == 'ace':
                if total + 11 > 21:
                    total += 1
                else:
                    total += 11
            else:
                total += card.value

        return total

    @property
    def cards(self):
        return self._cards

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @property
    def bet(self):
        return self._bet

    @bet.setter
    def bet(self, bet):
        self._bet = bet

# handles creation of deck, players and main loop
class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player()
        self.dealer = Player()
        self.round_in_progress = False

    def show_player_hand(self):
        print('your hand')
        print('-----------')
        for card in self.player.cards:
            print(card)

        print()
        print(f'your hand total: {self.player.get_card_total()}')
        print()
    
    def show_dealer_hand(self):
        print('dealer hand')
        print('-----------')
        for i, card in enumerate(self.dealer.cards):
            if i == 0:
                print('-- face down --')
            else:
                print(card)

        print()

    def show_help(self):
        print('How to play:')
        print('    h - hit')
        print('    s - stay')
        print('    c - show the cards in your hand')
        print('    d - show the cards the dealer has')
        print('    q - quit the game')
        print()

    def handle_player_won_round(self):
        print('**You won!**')
        print(f'Your total is {self.player.get_card_total()}')
        print(f"The dealer's total is {self.dealer.get_card_total()}")

        # add double the amount of points bet since the bet has already been subtracted from points
        self.player.points += self.player.bet * 2

    def handle_player_lost_round(self):
        print('**You lost!**')
        print(f'Your total is {self.player.get_card_total()}')
        print(f"The dealer's total is {self.dealer.get_card_total()}")

    def handle_draw_round(self):
        print('Draw')

        # add the bet back to point total
        self.player.points += self.player.bet

    # play the dealers hand and finish the round
    def end_round(self, player_busted=False):
        player_total = self.player.get_card_total()
        dealer_total = self.dealer.get_card_total()
        
        if player_busted:
            self.handle_player_lost_round()
        else:
            # play the dealers hand and show their cards and score
            self.play_dealer_hand()
            print("dealer's final hand")
            print('-----------')
            for card in self.dealer.cards:
                print(card)
            
            print()
            print(f"dealer's hand total: {self.dealer.get_card_total()}")
            print()

            dealer_busted = dealer_total > 21

            if player_total > dealer_total or dealer_busted:
                self.handle_player_won_round()
            elif not dealer_busted and (player_total < dealer_total or player_busted):
                self.handle_player_lost_round()
            else:
                self.handle_draw_round()

        print()
        print(f'** You have {self.player.points} points **')
        print()

        input('Press enter the start the next round\n')

        self.round_in_progress = False

        # reset player and dealer hands
        self.player.reset_cards()
        self.dealer.reset_cards()

    def play_dealer_hand(self):
        # play the dealers hand
        # if their hand is 16 or less, they hit, otherwise stay
        while self.dealer.get_card_total() <= 16:
            self.dealer.give_card(self.deck.deal_card())

    def handle_command(self, command):
        print()

        if command == 'h':
            self.player.give_card(self.deck.deal_card())

            if self.player.get_card_total() > 21:
                print('You busted!\n')
                self.end_round(player_busted=True)
        elif command == 's':
            print('You have finished your turn, now the dealer will go.\n')
            self.end_round()
        elif command == 'c':
            self.show_player_hand()
        elif command == 'd':
            self.show_dealer_hand()
        elif command == 'q':
            sys.exit(0)
        elif command == 'help':
            self.show_help()
        else:
            print("Enter a valid command. Type 'help' to see your options.\n")

    def play(self):
        # main loop
        while True:
            print(f'** You have {self.player.points} points **\n')

            # both dealer and player start with two cards
            for _ in range(2):
                self.player.give_card(self.deck.deal_card())
                self.dealer.give_card(self.deck.deal_card())
            
            self.show_dealer_hand()
            self.show_player_hand()
            self.round_in_progress = True

            # make player enter a positive integer for the bet
            valid_bet = False

            while not valid_bet:
                bet = input(f'You have {self.player.points} points. Enter your bet: ')

                try:
                    bet = int(bet)

                    if bet > 0:
                        self.player.bet = bet
                        valid_bet = True
                    else:
                        print('Enter a positive whole number for your bet\n')
                except:
                    print('Enter a positive whole number for your bet\n')
                
            self.player.points -= self.player.bet
            print()
            
            while self.round_in_progress:
                command = input("What do you want to do? (type 'help' to see your options): ")
                self.handle_command(command.strip())


if __name__ == '__main__':
    game = Game()
    game.play()
