# main.py
from room1 import enter_room1
from room2 import enter_room2
from room3 import enter_room3
from mood import MoodEngine
from engine.inventory import Inventory
from engine.telemetry import Telemetry
from engine.persistence import save_state, load_state
import json, os
from engine.config_room import run_config_room

def start_game():
    print("Welcome to MindMaze!")
    mood_engine = MoodEngine()
    inventory = Inventory()
    telemetry = Telemetry()

    telemetry.log(room="meta", event="game_start")

    start_idx = 0
    state = load_state("saves/slot1.json")
    if state.get("next_room") is not None:
        ans = input("Found a save. Continue? (y/n): ").strip().lower()
        if ans.startswith("y"):
            try:
                start_idx = int(state.get("next_room", 0))
            except Exception:
                start_idx = 0
            for item in state.get("inventory", []):
                inventory.add(item)
            print(f"Loaded save. Resuming at Room {start_idx+1} with items: {', '.join(inventory.list()) or 'none'}")
            telemetry.log(room="meta", event="load", next_room=start_idx+1, items=";".join(inventory.list()))

    rooms = [enter_room1, enter_room2, enter_room3]

    try:
        with open(os.path.join("data", "rooms.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)
        cfg_rooms = cfg.get("rooms", [])
        if cfg_rooms:
            for rcfg in cfg_rooms:
                def make_runner(c=rcfg):
                    return lambda me, telemetry=None, inventory=None: run_config_room(
                        c, mood_engine=me, telemetry=telemetry, inventory=inventory
                    )
                rooms.append(make_runner())
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"(Config rooms skipped: {e})")

    for i in range(start_idx, len(rooms)):
        ok = rooms[i](mood_engine, telemetry=telemetry, inventory=inventory)
        if not ok:
            telemetry.log(room="meta", event="game_over", at=f"room{i+1}")
            telemetry.export_csv("reports/session_timeline.csv")
            telemetry.export_mood_plot("reports/mood_timeline.png")
            print("Saved: reports/session_timeline.csv")
            print("Saved: reports/mood_timeline.png")
            print("Game Over.")
            return

        # autosave progress to next room
        next_room = i + 1
        save_state(
            {"next_room": next_room, "inventory": inventory.list()},
            path="saves/slot1.json",
        )
        telemetry.log(room="meta", event="autosave", next_room=next_room, items=";".join(inventory.list()))

    # escaped!
    telemetry.log(room="meta", event="escaped")
    telemetry.export_csv("reports/session_timeline.csv")
    telemetry.export_mood_plot("reports/mood_timeline.png")
    print("Saved: reports/session_timeline.csv")
    print("Saved: reports/mood_timeline.png")
    print("Congratulations! You've escaped MindMaze!")

if __name__ == "__main__":
    start_game()
