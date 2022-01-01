# Represents a card in a deck
# contains a suit (spade, heart, etc.), rank (two, three, ..., king, ace) and a value (1, 2, 3, or some number value tied to the card)
# value is optional since some games may not require it
class Card:
    def __init__(self, suit, rank, value=None):
        self._suit = suit
        self._rank = rank
        self._value = value

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        return self._value

    # able to change the value because this can change based on the context in some card games
    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return f'{self._rank} of {self._suit}'
