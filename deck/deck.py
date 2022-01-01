from deck.card import Card
import random

# TODO: keep track of discard pile, so if the deck is reset while some cards are still in play, it won't duplicate those cards
class Deck:
    _suits = [
        'spades',
        'hearts',
        'diamonds',
        'clubs'
    ]

    # default to blackjack card values
    _ranks_and_values = {
        'ace': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'jack': 10,
        'queen': 10,
        'king': 10
    }

    # the caller has the option to pass a custom set of custom suits, ranks and values for the cards
    def __init__(self, ranks_and_values=None):
        if ranks_and_values:
            self._ranks_and_values = ranks_and_values
        
        self.reset_deck()

    def reset_deck(self):
        # create a deck of cards
        cards = []
        for suit in self._suits:
            for rank in self._ranks_and_values:
                cards.append(Card(suit, rank, self._ranks_and_values[rank]))

        self._cards = cards

    @property
    def cards(self):
        return self._cards

    def shuffle(self):
        random.shuffle(self._cards)

    # remove a card from the deck
    # return None if the deck is empty. The caller can use reset_deck() to get a full deck again
    def deal_card(self):
        card = None

        if len(self._cards) > 0:
            card = self._cards.pop()
        
        return card
