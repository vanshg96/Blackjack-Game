import random
from .card import Card

class Deck:
    def __init__(self):
        self.cards = []
        suits = ["spades", "clubs", "hearts", "diamonds"]
        ranks = [
            {"rank": "A",  "value": 11},
            {"rank": "2",  "value": 2},
            {"rank": "3",  "value": 3},
            {"rank": "4",  "value": 4},
            {"rank": "5",  "value": 5},
            {"rank": "6",  "value": 6},
            {"rank": "7",  "value": 7},
            {"rank": "8",  "value": 8},
            {"rank": "9",  "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "J",  "value": 10},
            {"rank": "Q",  "value": 10},
            {"rank": "K",  "value": 10},
        ]
        for s in suits:
            for r in ranks:
                self.cards.append(Card(s, r))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n=1):
        # returns a list of n Card objects
        return [self.cards.pop() for _ in range(n)]
