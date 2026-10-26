const guessesLeftEl = document.getElementById("guesses-left");
const lastHintEl = document.getElementById("last-hint");
const feedbackEl = document.getElementById("feedback");
const errorEl = document.getElementById("error-text");
const formEl = document.getElementById("guess-form");
const inputEl = document.getElementById("guess-input");
const endPanelEl = document.getElementById("end-panel");
const endMessageEl = document.getElementById("end-message");
const btnNewEl = document.getElementById("btn-new");
const btnGuessEl = document.getElementById("btn-guess");

let gameId = null;

function showError(message) {
  if (!message) {
    errorEl.hidden = true;
    errorEl.textContent = "";
    return;
  }
  errorEl.hidden = false;
  errorEl.textContent = message;
}

function hintLabel(hint) {
  if (hint === "low") return "Too low";
  if (hint === "high") return "Too high";
  if (hint === "correct") return "Correct";
  return "—";
}

function applyState(state) {
  guessesLeftEl.textContent = String(state.guesses_left);
  lastHintEl.textContent = hintLabel(state.last_hint);
  lastHintEl.className = "stat-value " + (state.last_hint ? `hint-${state.last_hint}` : "hint-neutral");

  const over = state.won || state.lost;
  formEl.hidden = over;
  endPanelEl.hidden = !over;
  btnGuessEl.disabled = over;
  inputEl.disabled = over;

  if (state.won) {
    endMessageEl.textContent = `You got it in ${state.guesses_used} guess${state.guesses_used === 1 ? "" : "es"}!`;
    feedbackEl.textContent = "";
  } else if (state.lost) {
    endMessageEl.textContent = `Out of guesses. The number was ${state.secret}.`;
    feedbackEl.textContent = "";
  } else if (state.last_hint === "low") {
    feedbackEl.textContent = "Try a higher number.";
  } else if (state.last_hint === "high") {
    feedbackEl.textContent = "Try a lower number.";
  } else {
    feedbackEl.textContent = "Make your first guess.";
  }
}

async function apiNew() {
  const res = await fetch("/api/new", { method: "POST" });
  if (!res.ok) throw new Error("Could not start a new game.");
  return res.json();
}

async function apiGuess(guess) {
  const res = await fetch("/api/guess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id: gameId, guess }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Guess failed.");
  return data;
}

async function startGame() {
  showError("");
  try {
    const state = await apiNew();
    gameId = state.game_id;
    applyState(state);
    inputEl.value = "";
    inputEl.focus();
  } catch (err) {
    showError(err.message || "Something went wrong.");
  }
}

formEl.addEventListener("submit", async (event) => {
  event.preventDefault();
  showError("");
  const guess = Number(inputEl.value);
  if (!Number.isInteger(guess)) {
    showError("Enter a whole number.");
    return;
  }
  try {
    const state = await apiGuess(guess);
    applyState(state);
    if (!state.won && !state.lost) {
      inputEl.value = "";
      inputEl.focus();
    }
  } catch (err) {
    showError(err.message || "Something went wrong.");
  }
});

btnNewEl.addEventListener("click", () => startGame());

document.querySelectorAll("[data-help-jump]").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.getElementById("help-heading")?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });
});

startGame();
