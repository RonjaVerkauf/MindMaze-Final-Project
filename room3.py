# room3.py
import time

def print_staggered(block: str, line_delay: float = 3.0):
    for line in block.splitlines():
        print(line)
        time.sleep(line_delay)

def enter_room3(mood_engine=None, telemetry=None, inventory=None):
    """Runs Room 3: a Caesar-cipher door. Returns True if the player escapes, else False"""
    print("\n[ Room 3 ]")
    print_staggered(
        "Still excited by your successful escape from the second room you are walking into the third room. You see a big riveted door."
        "A rusted wheel above the lock shows the numbers: 5 3 4 8.\n"
        "Under it there is a sentence scratched into the door.'\n"
        "The word that these six letters form will help you escape:T O P L R A\n"
        "Type in the 6 letter password:"
    )

    answer = {"portal"}      # plaintext after shifting back by 6
    wrong_attempts = 0
    started = time.time()

    def give_hint(strength: str):
        if strength == "strong":
            print("HINT (strong): P is the first letter")
        elif strength == "soft":
            print("HINT (soft): The word describes a type of entrance or exit.")
        else:
            print("HINT: The last three letters are T A L")

    while True:
        user_input = input("\nEnter the password (or type 'hint'): ").strip().lower()

        if user_input == "hint":
            if telemetry:
                telemetry.log(room="room3", event="hint")
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

        is_correct = user_input in answer

        if mood_engine:
            elapsed = time.time() - started
            score = mood_engine.observe(
               text=user_input,
               seconds=elapsed,
               correct=is_correct,
               wrong_attempts=wrong_attempts
            )
            if telemetry:
                telemetry.log(room="room3", event="mood_tick",
                              mood_score=score, mood_state=mood_engine.mood_state())

        # log the answer event
        if telemetry:
            telemetry.log(room="room3", event="answer", input=user_input, correct=is_correct)

        if is_correct:
            print("The door opens...you made it! You've escaped MindMaze! You step out of the cave and find yourself on an empty beach. Where are you? You start walking and after some time you hear voices. Is this a rescue team searching for you? Or is the real escape just starting? ")
            return True

        wrong_attempts += 1
        print("The lock stays cold. That's not the password.")
        if mood_engine:
            state = mood_engine.mood_state()
            if state == "stressed":
                print("Breathe. Type 'hint' for a stronger clue")
            elif state == "focused":
                print("Use the vault's first two digits to set your shift. Type 'hint' if you need another clue.")
            elif state in ("calm", "excited"):
                print("Method: sum -> shift -> shift letters backward. Try again.")
        else:
            if wrong_attempts == 1:
                print("Tip: You can type 'hint' for help.")
