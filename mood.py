# mood.py
import math
import re
from collections import deque

class MoodEngine:
    """
    Infers player mood passively from gameplay signals:
    - response time per prompt
    - number of wrong attempts
    - text intensity (ALL CAPS, exclamation)
    - sentiment lexicon matches
    Returns states like: 'calm', 'neutral' 'excited', 'stressed'
    """

    POSITIVE_WORDS = {
        "nice", "great", "good", "fun", "cool", "love", "yay", "awesome", "solved", "got it", "easy", "ok", "okey", "perfect", "finally"
    }
    NEGATIVE_WORDS = {
        "stuck", "hard", "dumb", "annoying", "hate", "bad", "stressed", "help", "idk", "not sure", "no idea", "frustrating", "angry", "mad", "bored"
    }

    def __init__(self, history_size: int =6):
        #Keep a rolling window of recent scores
       self.scores = deque (maxlen=history_size)

    def _lexicon_score(self, text: str) -> float:
        t = text.lower()
        pos = sum(1 for w in self.POSITIVE_WORDS if w in t)
        neg = sum(1 for w in self.NEGATIVE_WORDS if w in t)
        base = (pos - neg)

        #Heuristics: exclamations and ALL CAPS amplify negativity/urgency
        exclaims = t.count("!")
        caps_ratio = self._caps_ratio(text)

        #scale: exclaims push negative if many and content is negative
        exclaim_effect = -0.2 * min(exclaims, 5)
        caps_effect = -0.8 * caps_ratio # mostly signals tension/urgency

        return base + exclaim_effect + caps_effect

    @staticmethod
    def _caps_ratio(text: str) -> float:
        letters = re.findall(r"[A-Za-z]", text)
        if not letters:
            return 0.0
        caps = sum(1 for ch in letters if ch.isupper())
        ratio = caps / len(letters)
        #Only count if yelling (threshold)
        return ratio if (len(letters) >= 6 and ratio > 0.6) else 0.0

    def observe(self, *, text: str, seconds: float, correct: bool, wrong_attempts: int):
        """
        Combine multiple signals into a single mood score.
        Positive score ~ calm&positive; negative score ~ stressed/frustrated.
        """
        # 1) Time pressure: long time without success tend to be negative.
        # Normalize: 0..30s -> 0..-1.5  (cap at 45s)
        t = max(0.0, min(seconds, 45.0))
        time_penalty = -1.5 * (t / 30.0)

        # 2) Wrong attempts penalty (cap at 3)
        wa = max(0, min(wrong_attempts, 3))
        wrong_penalty = -0.8 * wa

        # 3) Correctness bonus
        correct_bonus = 1.0 if correct else 0.0

        # 4) Text sentiment/urgency
        lex = self._lexicon_score(text)

        # Sum and squash into [-2.5, +2.5]
        raw = time_penalty + wrong_penalty + correct_bonus + lex
        raw= max(-2.5, min(raw, 2.5))

        self.scores.append(raw)
        return raw

    def mood_state(self) -> str:
        """
        Map averaged score to discrete mood states.
        """
        if not self.scores:
            return "neutral"
        avg = sum(self.scores) / len(self.scores)
        if avg <= -1.2:
            return "stressed"
        if avg <= -0.2:
            return "focused"  # slightly tense but productive
        if avg >= 1.2:
            return "excited"
        if avg >= 0.2:
            return "calm"
        return "neutral"

    def hint_policy(self):
        """
        Returns a tuple (give_hint: bool, hint_strength: 'soft'|'normal'|'strong')
        based on current mood.
        """
        state = self.mood_state()
        if state in ("stressed",):
            return True, "strong"
        if state in ("focused", "neutral"):
            return False, "normal"
        if state in ("calm", "excited"):
            return False, "soft"
        return False, "normal"