# Book directions — Guess the Number

**Catalog #470** · Al Sweigart, *The Big Book of Small Python Projects* — **Guess the Number**

- Online chapter: [inventwithpython.com/bigbookpython/project70.html](https://inventwithpython.com/bigbookpython/project70.html) (chapter title on site)
- Upstream: [guessthenumber.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/guessthenumber.py)
- Local reference: [`reference/guessthenumber.py`](./reference/guessthenumber.py)
- Shared logic: [`guess_core.py`](./guess_core.py)

## What the book asks you to build

Pick a random secret from **1–100**. The player gets **7** tries; after each guess print whether the answer is too high or too low until they win or run out of guesses.

## Web version (`web/` — FastAPI, port **3010**)

- `GET /` — game UI with guess form and hint history
- `POST /api/new` — start a fresh round (server stores secret in memory)
- `POST /api/guess` — submit a guess; returns hints and remaining tries

Run from `web/`:

```text
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 3010
```
