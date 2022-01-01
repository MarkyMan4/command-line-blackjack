from deck.deck import Deck
import sys

# player object
# has cards they are holding and their current number of points
class Player:
    def __init__(self, initial_points=100):
        self._cards = [] # cards in the players hand
        self._points = initial_points # initial points available to bet

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

    # play the dealers hand and finish the round
    def end_round(self, player_busted=False):
        player_total = self.player.get_card_total()
        dealer_total = self.dealer.get_card_total()
        
        if player_busted:
            print('**You lost!**')
            print(f'Your total is {player_total}')
            print(f"The dealer's total is {dealer_total}")
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

            # compare the player's total to the dealer's and determine who won, then end the round
            player_total = self.player.get_card_total()
            dealer_total = self.dealer.get_card_total()
            dealer_busted = dealer_total > 21

            if player_total > dealer_total or dealer_busted:
                print('**You won!**')
                print(f'Your total is {player_total}')
                print(f"The dealer's total is {dealer_total}")
            elif not dealer_busted and (player_total < dealer_total or player_busted):
                print('**You lost!**')
                print(f'Your total is {player_total}')
                print(f"The dealer's total is {dealer_total}")
            else:
                print('Draw')

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
            # both dealer and player start with two cards
            for _ in range(2):
                self.player.give_card(self.deck.deal_card())
                self.dealer.give_card(self.deck.deal_card())
            
            self.show_dealer_hand()
            self.show_player_hand()

            self.round_in_progress = True
            
            while self.round_in_progress:
                command = input("What do you want to do? (type 'help' to see your options): ")
                self.handle_command(command.strip())


if __name__ == '__main__':
    game = Game()
    game.play()
