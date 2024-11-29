import random
import os



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


#game board empty
def create_board(size):
    return [['-' for _ in range(size)] for _ in range(size)]


#print board
def print_board(board):
    print("  " + " ".join([chr(65 + i) for i in range(len(board))]))
    for i, row in enumerate(board):
        print(str(i + 1).rjust(2) + " " + " ".join(row))


#ships places
def place_ships(board, ship_sizes):
    for size in ship_sizes:
        while True:
            orientation = random.randint(0, 1)
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board) - 1)
            if orientation == 0 and col + size <= len(board) and all(board[row][col + i] == '-' for i in range(size)):
                for i in range(size):
                    board[row][col + i] = 'S'
                break
            elif orientation == 1 and row + size <= len(board) and all(board[row + i][col] == '-' for i in range(size)):
                for i in range(size):
                    board[row + i][col] = 'S'
                break


# Function to handle player's shot
def handle_shot(board, visible_board, row, col):
    if board[row][col] == 'S':
        board[row][col] = 'X'
        visible_board[row][col] = 'H'
        # Check if the ship is sunk
        if all(board[r][c] != 'S' for r in range(len(board)) for c in range(len(board)) if visible_board[r][c] == 'H'):
            return "Sunk!"
        return "Hit!"
    elif visible_board[row][col] != '-':
        return "Already shot here!"
    else:
        visible_board[row][col] = 'M'
        return "Miss!"


# Main game function
def play_game():
    size = 7
    ship_sizes = [3, 2, 2, 1, 1, 1, 1]
    board = create_board(size)
    visible_board = create_board(size)
    place_ships(board, ship_sizes)

    shots = 0
    name = input("Enter your name: ")

    while any('S' in row for row in board):
        clear_screen()
        print_board(visible_board)
        print(f"\n{name}, it's your turn!")
        try:
            # Get player's shot
            shot = input("Enter your shot (e.g., B3): ").upper()
            col = ord(shot[0]) - 65
            row = int(shot[1:]) - 1
            if 0 <= row < size and 0 <= col < size:
                result = handle_shot(board, visible_board, row, col)
                print(result)
                shots += 1
            else:
                print("Invalid coordinates. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Try again.")
        input("Press Enter to continue...")

    clear_screen()
    print(f"Congratulations, {name}! You won in {shots} shots.")
    return shots


# Main loop to play multiple games
def function():
    scores = []
    while True:
        shots = play_game()
        scores.append(shots)
        again = input("Play again? (yes/no): ").lower()
        if again != 'yes':
            break

    # Display leaderboard
    print("\nLeaderboard:")
    for i, score in enumerate(sorted(scores), start=1):
        print(f"{i}. {score} shots")


function()
