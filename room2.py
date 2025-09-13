# room2.py
import time

def print_staggered(block: str, line_delay: float = 3.0):
    for line in block.splitlines():
        print(line)
        time.sleep(line_delay)

def enter_room2(mood_engine=None, telemetry=None, inventory=None):
    """Runs Room 2: a hard logic vault puzzle. Returns True if the player escapes, else False."""
    print("\n[ Room 2 ]")
    print_staggered(
        "You step into a vault lined with cold steel. A wall-safe has four rotating dials.\n"
        "Seven lines are etched beside it:\n"
        "  1) The first digit is the third smallest prime number.\n"
        "  2) The second digit is an odd number that turns into a 12 when you multiply it with 4.\n"
        "  3) The third digit is the number that comes before your first and after your second digit.\n"
        "  4) The last digit equals the sum of the first two.\n"
        "Turn the dials to form the correct 4-digit code and press ENTER."
    )

    correct_codes = {"5348", "5 3 4 8"}
    wrong_attempts = 0
    started = time.time()

    def give_hint(strength: str):
        if strength == "strong":
            print("HINT (strong): Try first 5 and second 3 so the last becomes 8. ")
        elif strength == "soft":
            print("HINT (soft): Prime numbers are whole numbers greater than 1 which cannot be exactly divided by any whole number other than itself and 1.")
        else:
            # normal
            print("HINT: The last digit is the sum of the first two and must be a single digit (0–9). ")

    while True:
        user_input = input("\nEnter the 4-digit code (you can type spaces, or 'hint'): ").strip()

        # Handle hints
        if user_input.lower() == "hint":
            if telemetry:
                telemetry.log(room="room2", event="hint")
            if mood_engine:
                _, strength = mood_engine.hint_policy()
                give_hint(strength)
            else:
                # progressive hints without mood
                if wrong_attempts >= 3:
                    give_hint("strong")
                elif wrong_attempts == 2:
                    give_hint("normal")
                else:
                    give_hint("soft")
            continue

        # Normalize (remove spaces) and check
        normalized = user_input.replace(" ", "")
        is_correct = normalized in {c.replace(" ", "") for c in correct_codes}

        # Observe mood + log mood_tick
        if mood_engine:
            elapsed = time.time() - started
            score = mood_engine.observe(
                text=user_input,
                seconds=elapsed,
                correct=is_correct,
                wrong_attempts=wrong_attempts
            )
            if telemetry:
                telemetry.log(room="room2", event="mood_tick",
                              mood_score=score, mood_state=mood_engine.mood_state())

        # Log the answer
        if telemetry:
            telemetry.log(room="room2", event="answer", input=normalized, correct=is_correct)

        if is_correct:
            # give an item for later logic
            if inventory:
                inventory.add("code5196")
                if telemetry:
                    telemetry.log(room="room2", event="item_gain", item="code5196")
            print("A deep click echoes through the chamber. The vault door slides aside. You’ve escaped Room 2!")
            return True

        # Wrong answer flow
        wrong_attempts += 1
        print("The safe buzzes. The dials reset. That's not the right combination.")

        # ★ NEW: special message on the SECOND wrong attempt
        if wrong_attempts == 2:
            print("New clue: Recheck rule number 4 the last digit must equal the sum of the first two (and be a single digit).")
            # Optional: skip mood message this time for clarity
            continue

        # Otherwise, show mood-based guidance (or tip)
        if mood_engine:
            state = mood_engine.mood_state()
            if state == "stressed":
                print("You seem tense. Type 'hint' for a stronger clue.")
            elif state == "focused":
                print("You're close...use the structure of the clues. Type 'hint' if needed.")
            elif state in ("calm", "excited"):
                print("Stay methodical: check parity, perfect squares, and the sum relation.")
        else:
            if wrong_attempts == 1:
                print("Tip: You can type 'hint' for help.")
