import random

#  Card 
class Card:
    # ANSI colors for suits
    RED = "\033[91m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

    SUIT_SYMBOL = {"spades": "♠", "clubs": "♣", "hearts": "♥", "diamonds": "♦"}

    def __init__(self, suit, rank):
        self.suit = suit          # "spades" | "clubs" | "hearts" | "diamonds"
        self.rank = rank          # dict: {"rank": "A"/"2"... "K", "value": 11/2..10}

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


# ===== Deck =====
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

    def deal(self, n):
        return [self.cards.pop() for _ in range(n)]


# ===== Hand =====
class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.dealer = dealer

    def add_card(self, cards):
        self.cards.extend(cards)

    def value(self):
        total = sum(c.rank["value"] for c in self.cards)
        # adjust Aces 11->1 as many times as needed
        aces = sum(1 for c in self.cards if c.rank["rank"] == "A")
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self):
        return len(self.cards) == 2 and self.value() == 21

    def _hidden_card(self):
        return [
            "┌───────┐",
            "|░░░░░░░|",
            "|░░░░░░░|",
            "|░░░░░░░|",
            "|░░░░░░░|",
            "|░░░░░░░|",
            "└───────┘",
        ]

    def display(self, show_all=False, show_value_for_player=True):
        print("\nDealer's hand:" if self.dealer else "\nYour hand:")
        arts = []
        for i, c in enumerate(self.cards):
            if self.dealer and i == 0 and not show_all and not self.is_blackjack():
                arts.append(self._hidden_card())
            else:
                arts.append(c.ascii_art())
        for row in range(7):
            print(" ".join(a[row] for a in arts))
        if not self.dealer and show_value_for_player:
            print("Value:", self.value())


# ===== Game =====
class Game:
    def __init__(self):
        self.stats = {
            "rounds": 0,
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "player_blackjacks": 0,
            "dealer_blackjacks": 0,
        }

    def _print_scoreboard(self):
        s = self.stats
        print("\n" + "-" * 40)
        print(f"Rounds: {s['rounds']} | Wins: {s['wins']} | Losses: {s['losses']} | Ties: {s['ties']}")
        print(f"Blackjacks → You: {s['player_blackjacks']} | Dealer: {s['dealer_blackjacks']}")
        print("-" * 40)

    def check_winner(self, player, dealer, final=False):
        pv, dv = player.value(), dealer.value()

        if not final:
            if pv > 21:
                print("You busted. Dealer wins!")
                self.stats["losses"] += 1
                return True
            if dv > 21:
                print("Dealer busted. You win!")
                self.stats["wins"] += 1
                return True
            if player.is_blackjack() and dealer.is_blackjack():
                print("Both players have blackjack! Tie!")
                self.stats["ties"] += 1
                self.stats["player_blackjacks"] += 1
                self.stats["dealer_blackjacks"] += 1
                return True
            if player.is_blackjack():
                print("Blackjack! You win!")
                self.stats["wins"] += 1
                self.stats["player_blackjacks"] += 1
                return True
            if dealer.is_blackjack():
                print("Dealer has blackjack. Dealer wins!")
                self.stats["losses"] += 1
                self.stats["dealer_blackjacks"] += 1
                return True
            return False

        # final comparison
        if pv > dv:
            print("You win!")
            self.stats["wins"] += 1
        elif pv < dv:
            print("Dealer wins!")
            self.stats["losses"] += 1
        else:
            print("Tie!")
            self.stats["ties"] += 1
        return True

    def play(self):
        games_to_play = 0
        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except:
                print("You must enter a number.")

        for game_no in range(1, games_to_play + 1):
            self.stats["rounds"] += 1
            deck = Deck(); deck.shuffle()
            player, dealer = Hand(), Hand(dealer=True)

            for _ in range(2):
                player.add_card(deck.deal(1))
                dealer.add_card(deck.deal(1))

            print("\n" + "*" * 40)
            print(f"Game {game_no} of {games_to_play}")
            print("*" * 40)

            player.display()
            dealer.display()

            if self.check_winner(player, dealer):  # early end cases
                self._print_scoreboard()
                continue

            choice = ""
            while player.value() < 21 and choice not in ("s", "stand"):
                choice = input("Hit or Stand? (H/S): ").lower()
                while choice not in ("h", "s", "hit", "stand"):
                    choice = input("Please enter 'Hit' or 'Stand' (H/S): ").lower()
                if choice in ("h", "hit"):
                    player.add_card(deck.deal(1))
                    player.display()

            if self.check_winner(player, dealer):
                self._print_scoreboard()
                continue

            while dealer.value() < 17:
                dealer.add_card(deck.deal(1))
            dealer.display(show_all=True)

            if self.check_winner(player, dealer):
                self._print_scoreboard()
                continue

            print("\nFinal results")
            print("Your hand:", player.value())
            print("Dealer's hand:", dealer.value())
            self.check_winner(player, dealer, final=True)
            self._print_scoreboard()

        print("\nThanks for playing!")


if __name__ == "__main__":
    Game().play()
