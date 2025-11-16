class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.dealer = dealer

    def add_card(self, cards):
        # cards is a list of Card objects
        self.cards.extend(cards)

    def value(self):
        total = sum(c.rank["value"] for c in self.cards)
        aces = sum(1 for c in self.cards if c.rank["rank"] == "A")
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self):
        return len(self.cards) == 2 and self.value() == 21

    def is_bust(self):
        return self.value() > 21

    def ascii_rows(self, hide_first=False):
        """Return list of 7 strings (rows) to print side-by-side."""
        arts = []
        for i, c in enumerate(self.cards):
            if hide_first and i == 0:
                arts.append([
                    "┌───────┐",
                    "|░░░░░░░|",
                    "|░░░░░░░|",
                    "|░░░░░░░|",
                    "|░░░░░░░|",
                    "|░░░░░░░|",
                    "└───────┘",
                ])
            else:
                arts.append(c.ascii_art())
        rows = []
        for r in range(7):
            rows.append(" ".join(a[r] for a in arts))
        return rows
