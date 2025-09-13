# room1.py
import time

def print_staggered(block: str, line_delay: float = 3.0):
    for line in block.splitlines():
        print(line)
        time.sleep(line_delay)

def enter_room1(mood_engine=None, telemetry=None, inventory=None):
    """Runs Room 1 puzzle. Returns True if the player escapes, else False."""
    print("\n[ Room 1 ]")
    print_staggered(
        "You wake up in a narrow, musty cave. The air is damp; a thin, clammy film clings to your skin.\n"
        "As your eyes adjust, you grope along the rock. You find a piece of paper and a pencil on the ground.\n"
        "On the wall, a message reads:\n"
        "  \"I speak without a mouth and hear without ears, I mostly come to life in caves and tunnels and I repeat everything you say.\"\n"
        "What am I?"
    )

    # Accept common variants of the correct answer
    correct_answers = {"echo", "an echo"}

    wrong_attempts = 0
    started = time.time()

    def maybe_hint():
        # Always show at least one hint when the player asks for it
        if mood_engine:
            _, strength = mood_engine.hint_policy()
            if strength == "strong":
                print("HINT (strong): A sound that bounces back to you in caves and mountains your own words returning.")
            elif strength == "soft":
                print("HINT (soft): It repeats your words.")
            else:
                # 'normal' → still give a clear base hint
                if wrong_attempts >= 2:
                    print("HINT: You often notice it in caves or canyons.")
                else:
                    print("HINT: Think of a sound that repeats what you say.")
        else:
            # Progressive hints without mood engine
            if wrong_attempts >= 3:
                print("HINT: It repeats your words.")
            elif wrong_attempts == 2:
                print("HINT: You often notice it in caves or canyons.")
            else:
                print("HINT: Think of a sound that comes back to you.")

    while True:
        # Normalize input: trim spaces, lower-case, strip quotes so 'hint' or "hint" work
        raw = input("\nEnter your answer (or type 'hint'): ")
        user_input = raw.strip().lower().strip("'\"")

        if user_input == "hint":
            if telemetry:
                telemetry.log(room="room1", event="hint")
            maybe_hint()
            continue

        is_correct = user_input in correct_answers

        if mood_engine is not None:
            elapsed = time.time() - started
            # NEU: Score abfangen und als mood_tick loggen
            score = mood_engine.observe(
                text=user_input,
                seconds=elapsed,
                correct=is_correct,
                wrong_attempts=wrong_attempts
            )
            if telemetry:
                telemetry.log(
                    room="room1",
                    event="mood_tick",
                    mood_score=score,
                    mood_state=mood_engine.mood_state()
                )

        # NEW: log the answer event
        if telemetry:
            telemetry.log(room="room1", event="answer", input=user_input, correct=is_correct)

        if is_correct:
            # NEW: give a simple item for later rooms
            if inventory:
                inventory.add("paper (echo sketch)")
                if telemetry:
                    telemetry.log(room="room1", event="item_gain", item="paper (echo sketch)")

            print(
                "The letters flare brighter. The cave throws your voice back at you...an echo!\n"
                "With a grinding rumble, one of the walls collapses, revealing a passage onward."
            )
            return True

        wrong_attempts += 1
        print("Nothing happens. That's not it.")

        if mood_engine is not None:
            state = mood_engine.mood_state()
            if state == "stressed":
                print("You seem tense. Type 'hint' for a stronger clue.")
            elif state == "focused":
                print("Close! Stay on it! You can ask for a 'hint' if needed.")
            elif state in ("calm", "excited"):
                print("Keep going! You're on the right track (think about sounds).")
        else:
            if wrong_attempts == 1:
                print("Tip: You can type 'hint' for help.")
