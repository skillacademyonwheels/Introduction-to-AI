# tic_tac_toe.py
# A simple console Tic-Tac-Toe with an AI opponent (minimax).
# Play modes: Human vs AI, or Human vs Human.
# Author: You :)

from typing import List, Optional, Tuple

# -------- Board Representation --------
# We'll represent the board as a list of 9 characters: [" ", " ", ..., " "]
# Index mapping (0-based):
#  0 | 1 | 2
# ---+---+---
#  3 | 4 | 5
# ---+---+---
#  6 | 7 | 8
#
# The player symbols are 'X' and 'O'.


def print_board(board: List[str]) -> None:
    """Pretty-print the 3x3 board."""
    rows = [
        f" {board[0]} | {board[1]} | {board[2]} ",
        "---+---+---",
        f" {board[3]} | {board[4]} | {board[5]} ",
        "---+---+---",
        f" {board[6]} | {board[7]} | {board[8]} ",
    ]
    print("\n".join(rows))


def print_positions_guide() -> None:
    """Show users how to choose cells with numbers 1..9."""
    guide = [
        "Use these numbers to choose a cell:",
        " 1 | 2 | 3 ",
        "---+---+---",
        " 4 | 5 | 6 ",
        "---+---+---",
        " 7 | 8 | 9 ",
    ]
    print("\n".join(guide))


def available_moves(board: List[str]) -> List[int]:
    """Return list of indices that are empty."""
    return [i for i, cell in enumerate(board) if cell == " "]


def winner(board: List[str]) -> Optional[str]:
    """Return 'X' or 'O' if there is a winner, or None otherwise."""
    win_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    for a, b, c in win_lines:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: List[str]) -> bool:
    """True if the board is full and no winner."""
    return winner(board) is None and all(cell != " " for cell in board)


# -------- Human Input Handling --------

def get_human_move(board: List[str], current_player: str) -> int:
    """
    Prompt the user for a move (1..9), convert to 0-based index,
    and validate it's available.
    """
    while True:
        try:
            raw = input(f"Player {current_player}, enter your move (1-9): ").strip()
            pos = int(raw)
            if pos < 1 or pos > 9:
                print("Please enter a number from 1 to 9.")
                continue
            idx = pos - 1
            if board[idx] != " ":
                print("That cell is taken. Choose another.")
                continue
            return idx
        except ValueError:
            print("Please enter a valid number (1-9).")


# -------- Minimax AI --------
# Minimax tries all possible moves, assuming optimal play from both sides.
# Score convention:
#   +1 if AI wins, -1 if Human wins, 0 for draw.
#
# We’ll allow the AI to play as 'O' by default (but you can invert easily).

def minimax(board: List[str], ai: str, human: str, maximizing: bool) -> Tuple[int, Optional[int]]:
    """
    Return (score, best_move_index) from current board.
    - 'maximizing' indicates if it's AI's turn (maximize score) or human's (minimize).
    """
    win = winner(board)
    if win == ai:
        return (1, None)
    if win == human:
        return (-1, None)
    if is_draw(board):
        return (0, None)

    best_move = None
    if maximizing:
        best_score = -10  # lower than minimum possible
        for move in available_moves(board):
            board[move] = ai
            score, _ = minimax(board, ai, human, False)
            board[move] = " "
            if score > best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)
    else:
        best_score = 10  # higher than maximum possible
        for move in available_moves(board):
            board[move] = human
            score, _ = minimax(board, ai, human, True)
            board[move] = " "
            if score < best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)


def get_ai_move(board: List[str], ai: str, human: str) -> int:
    """Compute the best move for the AI using minimax."""
    _, move = minimax(board, ai, human, maximizing=True)
    # Fallback (shouldn't happen) in case minimax returns None
    if move is None:
        moves = available_moves(board)
        return moves[0]
    return move


# -------- Game Loop --------

def play_game(vs_ai: bool = True, ai_symbol: str = "O", human_symbol: str = "X") -> None:
    """
    Core game loop.
    - vs_ai=True → Human vs AI
    - vs_ai=False → Human vs Human
    - By default, Human is 'X' (starts), AI is 'O'.
    """
    board = [" "] * 9
    current = "X"  # 'X' always starts
    print_positions_guide()
    print_board(board)

    while True:
        if vs_ai and current == ai_symbol:
            print(f"AI ({ai_symbol}) is thinking...")
            move = get_ai_move(board, ai_symbol, human_symbol)
        else:
            move = get_human_move(board, current)

        board[move] = current
        print_board(board)

        # Check end conditions
        win = winner(board)
        if win:
            print(f"Player {win} wins! 🎉")
            break
        if is_draw(board):
            print("It's a draw. 🤝")
            break

        # Switch player
        current = "O" if current == "X" else "X"


def choose_mode_and_start() -> None:
    """Simple menu to select game mode and who starts."""
    print("Welcome to Tic-Tac-Toe!")
    while True:
        mode = input("Play vs (1) AI or (2) Human? Enter 1 or 2: ").strip()
        if mode in ("1", "2"):
            break
        print("Please type 1 or 2.")

    if mode == "1":
        # Ask who starts
        while True:
            first = input("Who starts? (X starts) Enter 'me' or 'ai': ").strip().lower()
            if first in ("me", "ai"):
                break
            print("Please type 'me' or 'ai'.")

        if first == "me":
            # Human is X (starts), AI is O
            play_game(vs_ai=True, ai_symbol="O", human_symbol="X")
        else:
            # Let AI be X (starts)
            play_game(vs_ai=True, ai_symbol="X", human_symbol="O")
    else:
        play_game(vs_ai=False)


if __name__ == "__main__":
    choose_mode_and_start()
