"""Terminal version — Guess the Number (book-style loop)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from guess_core import MAX_GUESSES, MAX_NUMBER, MIN_NUMBER, apply_guess, new_game_state  # noqa: E402


def main() -> None:
    print("I am thinking of a number between 1 and 100.")
    state = new_game_state()

    while not state["won"] and not state["lost"]:
        remaining = MAX_GUESSES - state["guesses_used"]
        print(f"\nYou have {remaining} guess{'es' if remaining != 1 else ''} left.")
        raw = input("Enter your guess: ").strip()
        if not raw.isdecimal():
            print("Please enter a whole number.")
            continue

        guess = int(raw)
        try:
            state = apply_guess(state, guess)
        except ValueError as exc:
            print(exc)
            continue

        if state["last_hint"] == "low":
            print("Too low!")
        elif state["last_hint"] == "high":
            print("Too high!")
        else:
            print("You got it!")
            return

        if state["lost"]:
            print(f"Out of guesses. The number was {state['secret']}.")
            return


if __name__ == "__main__":
    main()
