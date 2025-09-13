# engine/config_room.py
import time

def run_config_room(room_cfg, mood_engine=None, telemetry=None, inventory=None):
    print(f"\n[ {room_cfg.get('title', 'Room (Config)')} ]")
    print(room_cfg.get("intro", ""))

    correct_set = {a.strip().lower() for a in room_cfg.get("answers", [])}
    wrong_attempts = 0
    started = time.time()

    def give_hint(strength: str):
        h = room_cfg.get("hints", {})
        if strength == "strong":
            print("HINT (strong): " + h.get("strong", "Look closely at the riddle."))
        elif strength == "soft":
            print("HINT (soft): " + h.get("soft", "Focus on a daylight companion."))
        else:
            print("HINT: " + h.get("normal", "Think about light and the sun."))

    while True:
        raw = input("\n" + room_cfg.get("prompt", "Your answer: "))
        user_input = raw.strip().lower().strip("'\"")

        if user_input == "hint":
            if telemetry:
                telemetry.log(room=room_cfg.get("id", "config"), event="hint")
            if mood_engine:
                _, strength = mood_engine.hint_policy()
                give_hint(strength)
            else:
                give_hint("normal")
            continue

        is_correct = user_input in correct_set

        # mood observe
        if mood_engine:
            elapsed = time.time() - started
            score = mood_engine.observe(
                text=user_input,
                seconds=elapsed,
                correct=is_correct,
                wrong_attempts=wrong_attempts
            )
            if telemetry:
                telemetry.log(room=room_cfg.get("id", "config"), event="mood_tick",
                              mood_score=score, mood_state=mood_engine.mood_state())

        # answer log
        if telemetry:
            telemetry.log(room=room_cfg.get("id", "config"),
                          event="answer", input=user_input, correct=is_correct)

        if is_correct:
            print(room_cfg.get("success_text", "You solved it!"))
            return True

        wrong_attempts += 1
        print(room_cfg.get("fail_text", "Not it."))

        # mood-based guidance
        if mood_engine:
            state = mood_engine.mood_state()
            if state == "stressed":
                print("Breathe. Type 'hint' for a stronger clue.")
            elif state == "focused":
                print("Stay methodical. You can type 'hint'.")
            elif state in ("calm", "excited"):
                print("You're close—think daylight companion.")
        else:
            if wrong_attempts == 1:
                print("Tip: Type 'hint' for help.")
