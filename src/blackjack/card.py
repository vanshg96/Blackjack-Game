class Card:
    RED = "\033[91m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

    SUIT_SYMBOL = {"spades": "♠", "clubs": "♣", "hearts": "♥", "diamonds": "♦"}

    def __init__(self, suit, rank):
        # suit: "spades" | "clubs" | "hearts" | "diamonds"
        # rank: dict like {"rank":"A", "value":11}
        self.suit = suit
        self.rank = rank

    def _colored_suit(self):
        sym = self.SUIT_SYMBOL[self.suit]
        is_red = self.suit in ("hearts", "diamonds")
        return f"{self.RED if is_red else self.WHITE}{sym}{self.RESET}"

    def ascii_art(self):
        r = self.rank["rank"]
        suit = self._colored_suit()
        rL, rR = r.ljust(2), r.rjust(2)
        return [
            "┌───────┐",
            f"|{rL}     |",
            "|       |",
            f"|   {suit}   |",
            "|       |",
            f"|     {rR}|",
            "└───────┘",
        ]

    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"
