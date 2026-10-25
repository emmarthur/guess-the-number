"""
Guess the Number — shared logic for CLI reference and FastAPI web app.

The computer picks a secret integer; the player has a limited number of guesses
and receives higher/lower hints after each try.
"""

from __future__ import annotations

import random
from copy import deepcopy
from typing import Any, Literal

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_GUESSES = 7

Hint = Literal["high", "low", "correct"]


def new_game_state() -> dict[str, Any]:
    return {
        "secret": random.randint(MIN_NUMBER, MAX_NUMBER),
        "guesses_used": 0,
        "won": False,
        "lost": False,
        "last_hint": None,
    }


def public_view(state: dict[str, Any]) -> dict[str, Any]:
    """Client-safe snapshot (secret only revealed after loss)."""
    reveal_secret = state["won"] or state["lost"]
    return {
        "min_number": MIN_NUMBER,
        "max_number": MAX_NUMBER,
        "max_guesses": MAX_GUESSES,
        "guesses_used": state["guesses_used"],
        "guesses_left": max(0, MAX_GUESSES - state["guesses_used"]),
        "won": state["won"],
        "lost": state["lost"],
        "last_hint": state["last_hint"],
        "secret": state["secret"] if reveal_secret else None,
    }


def apply_guess(state: dict[str, Any], guess: int) -> dict[str, Any]:
    if state["won"] or state["lost"]:
        raise ValueError("This round is over. Start a new game.")

    if not MIN_NUMBER <= guess <= MAX_NUMBER:
        raise ValueError(f"Pick a number from {MIN_NUMBER} to {MAX_NUMBER}.")

    next_state = deepcopy(state)
    next_state["guesses_used"] += 1

    if guess < next_state["secret"]:
        next_state["last_hint"] = "low"
    elif guess > next_state["secret"]:
        next_state["last_hint"] = "high"
    else:
        next_state["last_hint"] = "correct"
        next_state["won"] = True
        return next_state

    if next_state["guesses_used"] >= MAX_GUESSES:
        next_state["lost"] = True

    return next_state
