"""
FastAPI app — Guess the Number.

Endpoints:
  GET  /              HTML UI
  POST /api/new       Start a new game (returns game_id + public state)
  POST /api/guess     Submit a guess for an active game_id

Run: uvicorn main:app --reload --port 3010
"""

from __future__ import annotations

import sys
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from guess_core import (  # noqa: E402
    MAX_GUESSES,
    MAX_NUMBER,
    MIN_NUMBER,
    apply_guess,
    new_game_state,
    public_view,
)

app = FastAPI(title="Guess the Number")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

_games: dict[str, dict[str, Any]] = {}


class GuessRequest(BaseModel):
    game_id: str = Field(..., min_length=1)
    guess: int = Field(..., ge=MIN_NUMBER, le=MAX_NUMBER)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "min_number": MIN_NUMBER,
            "max_number": MAX_NUMBER,
            "max_guesses": MAX_GUESSES,
        },
    )


@app.post("/api/new")
async def api_new() -> JSONResponse:
    game_id = uuid.uuid4().hex
    _games[game_id] = new_game_state()
    return JSONResponse({"game_id": game_id, **public_view(_games[game_id])})


@app.post("/api/guess")
async def api_guess(body: GuessRequest) -> JSONResponse:
    state = _games.get(body.game_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Unknown game. Start a new round.")

    try:
        _games[body.game_id] = apply_guess(state, body.guess)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return JSONResponse({"game_id": body.game_id, **public_view(_games[body.game_id])})
