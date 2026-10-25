# Guess the Number

Browser demo: narrow down a secret number from 1–100 with higher/lower hints and seven guesses.

## Run the web app

```powershell
cd c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\guess-the-number\web
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 3010
```

Open http://localhost:3010

## Run the terminal reference

```powershell
cd c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\guess-the-number
python reference\guessthenumber.py
```

Book provenance and steps: [`BOOK_DIRECTIONS.md`](./BOOK_DIRECTIONS.md).
