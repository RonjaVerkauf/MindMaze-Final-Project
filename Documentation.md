# MindMaze: Documentation

## Concept & Story
MindMaze is a short, terminal-based escape-room game. Your inputs, reaction time, and wrong attempts are condensed into a *mood*, which adapts hint strength and pacing.  
Rooms 1–3 are implemented in Python; **Room 4** is **loaded from a JSON file** (so new rooms can be added without code changes).

## Architecture Overview
- **main.py**: orchestrates rooms, mood, autosave/continue, and telemetry export
- **mood.py**:MoodEngine.observe(), aggregates signals, mood_state() -> hint_policy()
- **engine/**
  - inventory.py: simple inventory (add/list)
  - persistence.py: JSON save/load (saves/slot1.json)
  - telemetry.py: event logging -> CSV (reports/session_timeline.csv) + mood plot PNG (reports/mood_timeline.png)
  - config_room.py: runs rooms defined in data/rooms.json
- **data/rooms.json**: config-driven room(s) (title, prompts, answers, hints, texts)

**Flow (high level)**
Player input
   
-  MoodEngine.observe (text, seconds, correct, wrong_attempts)
         
 - mood_state + hint_policy
    
- Room logic (success/fail, inventory)

- Telemetry.log (room, event, input, correct, mood, timings)
-  Autosave after each successful room


## Modules & Responsibilities
- **room1.py, room2.py, room3.py:** classic rooms with their own puzzles and hints
- **engine/config_room.py:** generic runner for JSON-defined rooms
- **mood.py:** lexicon + timing + mistakes -> score -> state (stressed, focused, neutral, calm, excited)
- **engine/telemetry.py:** in-memory event list -> export to CSV; optional matplotlib plot

## Puzzles & Difficulty
- **Room 1:** Riddle (“echo”), progressive hints, gives an item to inventory
- **Room 2:** 4-digit logic code **5196**, structured rules, special message after 2nd wrong try
- **Room 3:** Caesar cipher with shift **6** (derived from Room 2)
- **Room 4 (JSON):** Riddle “shadow”, fully defined in data/rooms.json
- **Difficulty via Mood:** hint_policy() returns *soft / normal / strong* hints depending on mood

## MoodEngine (signals -> state)
Inputs considered in observe():
- Time spent answering (penalizes very long delays)
- Wrong attempts (cap and penalty)
- Correctness bonus (on success)
- Text heuristics (ALL CAPS ratio, exclamation marks, small lexicon for positive/negative words)

States:
- ≤ -1.2 = **stressed**
- ≤ -0.2 = **focused**
- ≥ 0.2 = **calm**
- ≥ 1.2 = **excited**
- else = **neutral**

## Telemetry & Artifacts
Each event (e.g., answer, hint, item_gain, escaped) is logged with:
- ts, room, event, input, correct, seconds, wrong_attempts, mood_score, mood_state, item (if applicable)

Artifacts generated on exit or game over:
- reports/session_timeline.csv
- reports/mood_timeline.png (requires matplotlib)

## Installation & Run (recap)
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- python main.py

Commands in-game: type `hint` for a clue. Autosave is stored at `saves/slot1.json`.

## Challenges & Solutions
- macOS Python (PEP 668) -> solved via project-local virtualenv
- Matplotlib install under Apple Silicon -> pinned via **requirements.txt**
- Consistent hint prompts & input normalization
- Config-driven room loader (robust JSON parse & graceful fallback)

## Future Work
- Add more JSON rooms / room packs without code changes
- Branching endings by mood/performance/items
- Sound cues or GUI front-end
- Localization and accessibility polish

## AI usage (granular, honest)

**Where AI assisted**
- Setup & Tooling: Guidance for resolving virtualenv / PEP 668 and installing matplotlib.
- Code review & suggestions:
  - Proposed the idea of a JSON-driven room and a small runner (engine/config_room.py).
  - Suggested a telemetry structure (CSV + mood timeline plot) and a simple print_staggered helper pattern.
  - Pointed out minor bug fixes (typos, wrong return value, len(letters) typo).

**What I implemented myself**
- Core gameplay flow and room logic (Rooms 1–3), hint behavior, and mood integration.
- Integration of inventory, autosave/resume, and telemetry into the main loop.
- Adapting/rewriting suggested snippets to fit my codebase; testing and fixing edge cases.
- Writing/curating all final room texts and pacing (staggered intros).

**Verification**
- I ran and tested the game locally in a virtual environment.
- I verified telemetry artifacts (reports/session_timeline.csv, reports/mood_timeline.png) after each run.
- I removed/changed any suggested code that didn’t meet my requirements or style.





