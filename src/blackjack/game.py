import json
import time
import sys
from pathlib import Path

from .deck import Deck
from .hand import Hand

# stats.json file lives next to this module
STATS_FILE = Path(__file__).parent / "stats.json"
DEFAULT_STATS = {"rounds": 0, "wins": 0, "losses": 0, "ties": 0, "chips": 500}

def load_stats():
    if STATS_FILE.exists():
        try:
            with STATS_FILE.open("r", encoding="utf8") as f:
                data = json.load(f)
            # ensure keys
            for k, v in DEFAULT_STATS.items():
                data.setdefault(k, v)
            return data
        except Exception:
            return DEFAULT_STATS.copy()
    else:
        return DEFAULT_STATS.copy()

def save_stats(stats):
    try:
        with STATS_FILE.open("w", encoding="utf8") as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        print("Could not save stats:", e)

def loading_animation(seconds=1.0):
    suits = ["♠","♥","♦","♣"]
    end = time.time() + seconds
    i = 0
    while time.time() < end:
        sys.stdout.write("\rLoading " + suits[i % len(suits)] + " ")
        sys.stdout.flush()
        time.sleep(0.12)
        i += 1
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()

class Game:
    def __init__(self):
        self.stats = load_stats()
        self.chips = int(self.stats.get("chips", 500))

    def _panel(self):
        s = self.stats
        print("\n" + "-" * 54)
        print(f"Chips: {self.chips} | Rounds: {s.get('rounds',0)} Wins: {s.get('wins',0)} Losses: {s.get('losses',0)} Ties: {s.get('ties',0)}")
        print("-" * 54)

    def _place_bet(self):
        while True:
            try:
                bet = int(input(f"You have {self.chips} chips. Place your bet (1 - {self.chips}): ").strip())
                if 1 <= bet <= self.chips:
                    return bet
                print("Invalid bet amount.")
            except ValueError:
                print("Please enter a valid integer.")

    # Dealer easy: hit until <17. Hard: hit on soft 17 as well.
    def _dealer_play_easy(self, deck, dealer_hand):
        while dealer_hand.value() < 17:
            dealer_hand.add_card(deck.deal(1))

    def _dealer_play_hard(self, deck, dealer_hand):
        def has_soft_17(h):
            total = sum(c.rank["value"] for c in h.cards)
            aces = sum(1 for c in h.cards if c.rank["rank"] == "A")
            # total==17 but an ace present means it may be soft 17
            return total == 17 and aces >= 1
        while dealer_hand.value() < 17 or has_soft_17(dealer_hand):
            dealer_hand.add_card(deck.deal(1))

    def play_round(self, difficulty="easy"):
        deck = Deck(); deck.shuffle()
        player = Hand()
        dealer = Hand(dealer=True)
        bet = self._place_bet()

        player.add_card(deck.deal(2))
        dealer.add_card(deck.deal(2))

        print("\nDealing cards...")
        loading_animation(0.8)

        print("\nDealer:")
        for r in dealer.ascii_rows(hide_first=True):
            print(r)
        print("\nPlayer:")
        for r in player.ascii_rows():
            print(r)
        print("Player value:", player.value())

        # immediate blackjack checks
        if player.is_blackjack() or dealer.is_blackjack():
            if player.is_blackjack() and dealer.is_blackjack():
                print("Both have Blackjack! Push.")
                self.stats["ties"] = self.stats.get("ties",0) + 1
                return 0
            if player.is_blackjack():
                print("Blackjack! You win 1.5x the bet.")
                self.stats["wins"] = self.stats.get("wins",0) + 1
                self.chips += int(1.5 * bet)
                return 1
            if dealer.is_blackjack():
                print("Dealer has Blackjack. You lose.")
                self.stats["losses"] = self.stats.get("losses",0) + 1
                self.chips -= bet
                return -1

        # Player turn
        while True:
            if player.is_bust():
                print("\nYou busted!")
                self.stats["losses"] = self.stats.get("losses",0) + 1
                self.chips -= bet
                return -1
            choice = input("Hit or Stand? (H/S): ").strip().lower()
            if choice.startswith("h"):
                player.add_card(deck.deal(1))
                for r in player.ascii_rows():
                    print(r)
                print("Player value:", player.value())
                continue
            elif choice.startswith("s"):
                break
            else:
                print("Please enter H or S.")

        # Dealer reveal & play
        print("\nDealer reveals:")
        for r in dealer.ascii_rows(hide_first=False):
            print(r)

        if difficulty == "hard":
            self._dealer_play_hard(deck, dealer)
        else:
            self._dealer_play_easy(deck, dealer)

        print("\nDealer final:")
        for r in dealer.ascii_rows():
            print(r)
        print("Dealer value:", dealer.value())

        # Resolve
        p = player.value()
        d = dealer.value()

        if d > 21:
            print("Dealer busted. You win!")
            self.stats["wins"] = self.stats.get("wins",0) + 1
            self.chips += bet
            return 1
        if p > d:
            print("You win!")
            self.stats["wins"] = self.stats.get("wins",0) + 1
            self.chips += bet
            return 1
        if p < d:
            print("Dealer wins.")
            self.stats["losses"] = self.stats.get("losses",0) + 1
            self.chips -= bet
            return -1
        print("Push (tie).")
        self.stats["ties"] = self.stats.get("ties",0) + 1
        return 0

    def save(self):
        # update stats dict and save
        self.stats["chips"] = self.chips
        save_stats(self.stats)

    # interactive session runner (menu is in main)
    def session_play(self, rounds=1, difficulty="easy"):
        for i in range(rounds):
            print(f"\n--- ROUND {i+1} ---")
            result = self.play_round(difficulty=difficulty)
            self.stats["rounds"] = self.stats.get("rounds",0) + 1
            self._panel()
            if self.chips <= 0:
                print("You're out of chips! Session ended.")
                break
        self.save()
