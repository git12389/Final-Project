import random
import tkinter as tk
from tkinter import messagebox
from pygame import mixer

# Initialize pygame mixer for sound
mixer.init()

# Load sound file (Ensure you have a sound file in the working directory)
mixer.music.load("gameplay_sound.mp3")

# Correct deck creation using 'A' for Ace, 'J' for Jack, 'Q' for Queen, and 'K' for King
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']  # Correct representation of face cards
deck = [(value, suit) for value in values for suit in suits]

# Shuffle the deck
random.shuffle(deck)

# Define patterns for grade 3-5
patterns = {
    "All Even Numbers": lambda hand: all(isinstance(value, int) and value % 2 == 0 for value, suit in hand),
    "All Odd Numbers": lambda hand: all(isinstance(value, int) and value % 2 != 0 for value, suit in hand),
    "Sum of Values is Greater than 20": lambda hand: sum(value if isinstance(value, int) else 10 for value, suit in hand) > 20,  # Face cards count as 10
    "Two Red and Two Black Cards": lambda hand: len([suit for value, suit in hand if suit in ['Hearts', 'Diamonds']]) == 2 and len([suit for value, suit in hand if suit in ['Clubs', 'Spades']]) == 2,
    "All Cards of Different Suits": lambda hand: len(set(suit for value, suit in hand)) == 4,
    "Two Picture Cards (Jack, Queen, King)": lambda hand: len([value for value, suit in hand if value in ['J', 'Q', 'K']]) == 2,
    "Prime Numbers and a Face Card": lambda hand: any(value in [2, 3, 5, 7, 11] for value, suit in hand if isinstance(value, int)) and any(value in ['J', 'Q', 'K'] for value, suit in hand),
    "Two Cards Add Up to 10": lambda hand: any(hand[i][0] + hand[j][0] == 10 for i in range(len(hand)) for j in range(i + 1, len(hand)) if isinstance(hand[i][0], int) and isinstance(hand[j][0], int)),
    "All Cards Greater than 5": lambda hand: all(value > 5 for value, suit in hand if isinstance(value, int)),
    "One Card of Each Rank (1-10)": lambda hand: len(set(min(value, 10) if isinstance(value, int) else 10 for value, suit in hand)) == 4
}

# Keep score history
score_history = []

# Function to evaluate the art dealer's selection based on the chosen pattern
def evaluate_hand(hand, pattern_name):
    pattern = patterns.get(pattern_name)
    if pattern:
        return pattern(hand)
    return False

# Function for the Art Dealer (system) to pick cards
def art_dealer_pick(user_selected_cards, deck):
    remaining_deck = [card for card in deck if card not in user_selected_cards]  # Exclude user-picked cards for randomness
    art_dealer_hand = random.sample(remaining_deck + user_selected_cards, 4)

    # Count how many cards the art dealer picked from user-selected cards
    from_user = [card for card in art_dealer_hand if card in user_selected_cards]
    from_deck = [card for card in art_dealer_hand if card not in user_selected_cards]

    return art_dealer_hand, from_user, from_deck

# Function to simulate a game round
def play_game(selected_pattern, result_label, score_label, art_dealer_hand):
    # Now the user selects a pattern, and the system (art dealer) evaluates it against its hand
    if evaluate_hand(art_dealer_hand, selected_pattern):
        result_label.config(text=f"Correct! The Art Dealer's hand is: {art_dealer_hand}. You win!", fg="green")
        score_history.append("Win")
    else:
        result_label.config(text=f"Incorrect. The Art Dealer's hand is: {art_dealer_hand}. Try again!", fg="red")
        score_history.append("Loss")
    
    # Update score label
    score_label.config(text=f"Score History: {', '.join(score_history)}")

# Function to reset the game
def reset_game(selected_cards_label, art_dealer_label, art_dealer_info_label, selected_cards, result_label):
    selected_cards.clear()
    selected_cards_label.config(text="Your selected cards will appear here.")
    art_dealer_label.config(text="Art Dealer's hand will appear here.")
    art_dealer_info_label.config(text="Art Dealer's card selection information will appear here.")
    result_label.config(text="")

# Function to show score history
def show_score_history():
    messagebox.showinfo("Score History", f"Score History: {', '.join(score_history)}")

# Function to start the game
def start_game():
    mixer.music.play()

# GUI Setup
def main():
    # Create the main window
    root = tk.Tk()
    root.title("Art Dealer Game (Grades 3-5)")
    root.geometry("800x600")

    # Sections of the UI with different background colors
    top_frame = tk.Frame(root, bg="light green")
    top_frame.pack(fill="both", expand=True, padx=10, pady=10)

    middle_frame = tk.Frame(root, bg="light blue")
    middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

    bottom_frame = tk.Frame(root, bg="light yellow")
    bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Title label (Top Frame)
    title_label = tk.Label(top_frame, text="Welcome to the Art Dealer Game!", font=("Helvetica", 16), bg="light green")
    title_label.pack(pady=10)

    # Dropdown to select a pattern (Top Frame)
    pattern_var = tk.StringVar(root)
    pattern_var.set("Select a Pattern")
    pattern_menu = tk.OptionMenu(top_frame, pattern_var, *patterns.keys())
    pattern_menu.pack(pady=10)

    # Selected cards label (Middle Frame)
    selected_cards_label = tk.Label(middle_frame, text="Your selected cards will appear here.", font=("Helvetica", 12), bg="light blue")
    selected_cards_label.grid(row=5, column=0, columnspan=3, pady=10)

    # Art Dealer's cards label (Bottom Frame)
    art_dealer_label = tk.Label(bottom_frame, text="Art Dealer's hand will appear here.", font=("Helvetica", 12), bg="light yellow")
    art_dealer_label.pack(pady=5)

    # Art Dealer's selection information (Bottom Frame)
    art_dealer_info_label = tk.Label(bottom_frame, text="Art Dealer's card selection information will appear here.", font=("Helvetica", 12), bg="light yellow")
    art_dealer_info_label.pack(pady=5)

    # Result label (Bottom Frame)
    result_label = tk.Label(bottom_frame, text="", font=("Helvetica", 12), bg="light yellow")
    result_label.pack(pady=5)

    # Card selection variables
    selected_cards = []
    art_dealer_hand = []
    art_dealer_from_user = []
    art_dealer_from_deck = []

    # Drop-down lists for user to select 4 cards (Middle Frame)
    def card_selection():
        value1 = value_var1.get()
        suit1 = suit_var1.get()
        value2 = value_var2.get()
        suit2 = suit_var2.get()
        value3 = value_var3.get()
        suit3 = suit_var3.get()
        value4 = value_var4.get()
        suit4 = suit_var4.get()

        selected_cards.clear()
        selected_cards.append((value1, suit1))
        selected_cards.append((value2, suit2))
        selected_cards.append((value3, suit3))
        selected_cards.append((value4, suit4))

        # Show selected cards
        selected_cards_label.config(text=f"Selected Cards: {selected_cards}")

        # After selection, the art dealer picks cards and shows them
        nonlocal art_dealer_hand, art_dealer_from_user, art_dealer_from_deck
        art_dealer_hand, art_dealer_from_user, art_dealer_from_deck = art_dealer_pick(selected_cards, deck)
        #art_dealer_label.config(text=f"Art Dealer's Hand: {art_dealer_hand}")
        art_dealer_info_label.config(text=f"Art Dealer bought {len(art_dealer_from_user)} card(s) from you and {len(art_dealer_from_deck)} card(s) from the deck.")

    # Create drop-down lists for card values and suits (Middle Frame)
    value_var1 = tk.StringVar(root)
    value_var2 = tk.StringVar(root)
    value_var3 = tk.StringVar(root)
    value_var4 = tk.StringVar(root)

    suit_var1 = tk.StringVar(root)
    suit_var2 = tk.StringVar(root)
    suit_var3 = tk.StringVar(root)
    suit_var4 = tk.StringVar(root)

    # Set default values for the drop-downs
    value_var1.set(values[0])
    value_var2.set(values[0])
    value_var3.set(values[0])
    value_var4.set(values[0])

    suit_var1.set(suits[0])
    suit_var2.set(suits[0])
    suit_var3.set(suits[0])
    suit_var4.set(suits[0])

    # Organize drop-downs in grid layout for clarity (Middle Frame)
    tk.Label(middle_frame, text="Card 1:", bg="light blue").grid(row=0, column=0, padx=5)
    tk.OptionMenu(middle_frame, value_var1, *values).grid(row=0, column=1, padx=5)
    tk.OptionMenu(middle_frame, suit_var1, *suits).grid(row=0, column=2, padx=5)

    tk.Label(middle_frame, text="Card 2:", bg="light blue").grid(row=1, column=0, padx=5)
    tk.OptionMenu(middle_frame, value_var2, *values).grid(row=1, column=1, padx=5)
    tk.OptionMenu(middle_frame, suit_var2, *suits).grid(row=1, column=2, padx=5)

    tk.Label(middle_frame, text="Card 3:", bg="light blue").grid(row=2, column=0, padx=5)
    tk.OptionMenu(middle_frame, value_var3, *values).grid(row=2, column=1, padx=5)
    tk.OptionMenu(middle_frame, suit_var3, *suits).grid(row=2, column=2, padx=5)

    tk.Label(middle_frame, text="Card 4:", bg="light blue").grid(row=3, column=0, padx=5)
    tk.OptionMenu(middle_frame, value_var4, *values).grid(row=3, column=1, padx=5)
    tk.OptionMenu(middle_frame, suit_var4, *suits).grid(row=3, column=2, padx=5)

    # Button to confirm card selection (Middle Frame)
    select_button = tk.Button(middle_frame, text="Select Cards", font=("Helvetica", 12), command=card_selection, bg="light blue")
    select_button.grid(row=4, column=0, columnspan=3, pady=10)

    # Play Game button (Bottom Frame)
    play_button = tk.Button(bottom_frame, text="Play Game", font=("Helvetica", 12), 
                            command=lambda: play_game(pattern_var.get(), result_label, score_label, art_dealer_hand), bg="light yellow")
    play_button.pack(pady=10)

    # Reset button (Bottom Frame)
    reset_button = tk.Button(bottom_frame, text="Reset", font=("Helvetica", 12), 
                             command=lambda: reset_game(selected_cards_label, art_dealer_label, art_dealer_info_label, selected_cards, result_label), bg="light yellow")
    reset_button.pack(pady=10)

    # Score history button (Bottom Frame)
    score_button = tk.Button(bottom_frame, text="Score History", font=("Helvetica", 12), command=show_score_history, bg="light yellow")
    score_button.pack(pady=10)

    # Exit button (Bottom Frame)
    exit_button = tk.Button(bottom_frame, text="Exit", font=("Helvetica", 12), command=root.quit, bg="light yellow")
    exit_button.pack(pady=10)

    # Score label (Bottom Frame)
    score_label = tk.Label(bottom_frame, text="Score History: None", font=("Helvetica", 12), bg="light yellow")
    score_label.pack(pady=5)

    # Start the gameplay sound
    start_game()

    # Run the GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()
