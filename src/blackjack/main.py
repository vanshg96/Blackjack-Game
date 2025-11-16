from blackjack.game import Game, loading_animation, load_stats, save_stats

def print_rules():
    print("""
Blackjack Rules:
- Get as close to 21 without going over.
- Aces count as 11 or 1 automatically.
- Dealer hits until 17 (Hard difficulty hits soft 17).
- Blackjack pays 1.5x.
""")

def main_menu():
    game = Game()
    while True:
        print("\n=== BLACKJACK MENU ===")
        print("1) Play")
        print("2) Rules")
        print("3) View saved Stats")
        print("4) Reset saved Stats")
        print("5) Exit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            diff = ""
            while diff not in ("1","2"):
                diff = input("Choose difficulty: 1) Easy  2) Hard : ").strip()
            difficulty = "hard" if diff == "2" else "easy"
            while True:
                try:
                    total = int(input("How many rounds do you want to play? "))
                    if total > 0:
                        break
                except ValueError:
                    pass
                print("Enter a positive integer.")
            loading_animation(0.6)
            game.session_play(rounds=total, difficulty=difficulty)
        elif choice == "2":
            print_rules()
        elif choice == "3":
            s = load_stats()
            print("\n=== SAVED STATS ===")
            print(f"Rounds: {s.get('rounds',0)} Wins: {s.get('wins',0)} Losses: {s.get('losses',0)} Ties: {s.get('ties',0)}")
            print(f"Chips: {s.get('chips',500)}")
        elif choice == "4":
            confirm = input('Type "RESET" to reset saved stats: ')
            if confirm == "RESET":
                save_stats({"rounds":0,"wins":0,"losses":0,"ties":0,"chips":500})
                print("Stats reset.")
            else:
                print("Cancelled.")
        elif choice == "5":
            print("Saving stats and exiting...")
            game.save()
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main_menu()
