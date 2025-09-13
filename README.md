# MindMaze: A Mood-Adaptive Escape Room (Python)

MindMaze is a short escape-room game played in the terminal. Your inputs, reaction time, and wrong attempts are condensed into a “mood,” which determines how strong the hints are and how the game flow feels. Rooms 1–3 are implemented in the traditional way, while **Room 4** is **loaded from a JSON file** (expandable without additional code).
 
> ![Escape Room Meme](media/escape_room_meme.jpg)





---

## Installation

The project uses an external library (Matplotlib). Install the dependencies:

~~~bash
pip install -r requirements.txt
~~~
## Features
- Mood-adaptive hints (calm / focused / stressed)
- Staggered room intros (line-by-line reveal)
- Autosave after each room + resume on next launch
- Config-driven Room 4 (JSON; extend without code)
- Telemetry: CSV log + mood timeline plot (PNG)

## Usage

Run the game from the project root in your terminal.

### macOS / Linux
~~~bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
~~~

### Windows (PowerShell)
~~~powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
~~~


